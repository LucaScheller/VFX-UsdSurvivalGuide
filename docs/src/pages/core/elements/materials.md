# Materials
Materials in USD are exposed via the [UsdShade](https://openusd.org/dev/api/usd_shade_page_front.html) module.

Shader networks are encoded via the [UsdShade.ConnectableAPI](https://openusd.org/dev/api/class_usd_shade_connectable_a_p_i.html). So we have full access to the node graph as it is fully represented as USD prims. This allows for flexible editing, as it is as simple as editing attributes and connections on your individual material node prims.

USD has support for encoding [MaterialX](https://materialx.org/) node graphs, which allows for render engine agnostic shader creation.

# Table of Contents
1. [Materials In-A-Nutshell](#summary)
1. [What should I use it for?](#usage)
1. [Resources](#resources)
1. [Overview](#overview)
    1. [Material Binding](#materialBinding)
    1. [Node graph encoding via attribute to attribute connections](#materialNodeGraph)

## TL;DR - Metadata In-A-Nutshell <a name="summary"></a>
- USD can encode material node graphs as prims. It supports writing [MaterialX](https://materialx.org/) node graphs, which are renderer agnostic material descriptions.
- We can bind materials either directly or via [collections](./collection.md).

## What should I use it for? <a name="usage"></a>
~~~admonish tip
Materials themselves are usually generated by the DCC you are working in, so we usually don't have to create them ourselves. What we do use the `UsdShade` module for is editing material bindings and overriding individual nodes and their connections in a material node graph.
~~~

## Resources <a name="resources"></a>
- [UsdShade](https://openusd.org/dev/api/usd_shade_page_front.html)
- [UsdShade.Material](https://openusd.org/dev/api/class_usd_shade_material.html)
- [UsdShade.MaterialBindingAPI](https://openusd.org/dev/api/class_usd_shade_material_binding_a_p_i.html)
- [UsdShade.ConnectableAPI](https://openusd.org/dev/api/class_usd_shade_connectable_a_p_i.html)

## Overview <a name="overview"></a>
~~~admonish question title="Still under construction!"
This section still needs some more love, we'll likely expand it more in the near future.
~~~

### Material binding <a name="materialBinding">
One of the most common use cases of relationships is encoding the material binding. Here we simply link from any imageable (renderable) prim to a `UsdShade.Material` (`Material`) prim.

~~~admonish important
Material bindings are a special kind of relationship. Here are a few important things to know:
- When looking up material bindings, USD also looks at parent prims if it can't find a written binding on the prim directly. This means you can create the binding on any parent prim and just as with primvars, it will be inherited downwards to its children.
- The "binding strength" can be adjusted, so that a child prim assignment can also be override from a binding higher up the hierarchy.
- Material bindings can also be written per purpose, if not then they bind to all purposes. (Technically it is not called purpose, the token names are `UsdShade.MaterialBindingAPI.GetMaterialPurposes() -> ['', 'preview', 'full']`). The 'preview' is usually bound to the 'UsdGeom.Tokens.proxy' purpose, the 'full' to the 'UsdGeom.Tokens.render' purpose.
- The material binding can be written in two ways:
    - Direct Binding: A relationship that points directly to a material prim
    - Collection Based Binding: A relationship that points to another collection, that then stores the actual binding paths) and to a material prim to bind.
~~~

Here is an example of a direct binding:
```python
over "asset"
{
    over "GEO"(
        prepend apiSchemas = ["MaterialBindingAPI"]
    )
    {
        rel material:binding = </materials/metal>
        over "plastic_mesh" (
            prepend apiSchemas = ["MaterialBindingAPI"]
        )
        {
            rel material:binding = </asset/materials/plastic>
        }
    }
}
```

And here is an example of a collection based binding. As you can see it is very easy to exclude a certain prim from a single control point, whereas with the direct binding we have to author it on the prim itself.
```python
def "asset" (
    prepend apiSchemas = ["MaterialBindingAPI", "CollectionAPI:material_metal"]
)
{
    rel material:binding:collection:material_metal = [
        </shaderball.collection:material_metal>,
        </materials/metal>,
    ]

    uniform token collection:material_metal:expansionRule = "expandPrims"
    rel collection:material_metal:includes = </asset>
    rel collection:material_metal:excludes = </asset/GEO/plastic_mesh>
}
```

For creating bindings in the high level API, we use the `UsdShade.MaterialBindingAPI` schema.
Here is the link to the official [API docs](https://openusd.org/dev/api/class_usd_shade_material_binding_a_p_i.html).

For more info about the load order (how collection based bindings win over direct bindings), you can read the "Bound Material Resolution" section on the API docs page.

~~~admonish tip title=""
```python
{{#include ../../../../../code/core/elements.py:relationshipMaterialBinding}}
```
~~~


### Node graph encoding via attribute to attribute connections <a name="materialNodeGraph"></a>
Attributes can also encode relationship-like paths to other attributes. These connections are encoded directly on the attribute. It is up to Usd/Hydra to evaluate these "attribute graphs", if you simply connect two attributes, it will not forward attribute value A to connected attribute B (USD does not have a concept for a mechanism like that (yet)).

Here is an example of how a material network is encoded.

~~~admonish important title=""
```python
def Scope "materials"
{
    def Material "karmamtlxsubnet" (
    )
    {
        token outputs:mtlx:surface.connect = </materials/karmamtlxsubnet/mtlxsurface.outputs:out>

        def Shader "mtlxsurface" ()
        {
            uniform token info:id = "ND_surface"
            string inputs:edf.connect = </materials/karmamtlxsubnet/mtlxuniform_edf.outputs:out>
            token outputs:out
        }

        def Shader "mtlxuniform_edf"
        {
            uniform token info:id = "ND_uniform_edf"
            color3f inputs:color.connect = </materials/karmamtlxsubnet/mtlx_constant.outputs:out>
            token outputs:out
        }

        def Shader "mtlx_constant"
        {
            uniform token info:id = "ND_constant_float"
            float outputs:out
        }
    }
}
```
~~~

In our [property](./property.md#attribute-to-attribute-connections-node-graph-encoding) section we cover the basics how to connect different attributes. For material node graphs USD ships with the [UsdShade.ConnectableAPI](https://openusd.org/dev/api/class_usd_shade_connectable_a_p_i.html). It should be used/preferred instead of using the `Usd.Attribute.AddConnection` method, as it does extra validation as well as offer convenience functions for iterating over connections.