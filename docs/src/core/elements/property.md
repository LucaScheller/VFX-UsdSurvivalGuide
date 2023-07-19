# Properties
For an overview and summary please see the parent [Data Containers](./data_container.md) section.

Here is an overview of the API structure, in the high level API it looks as follows:
```mermaid
flowchart TD
    property([Usd.Property])
    property --> attribute([Usd.Attribute])
    property --> relationship([Usd.Relationship])
```
In the low level API:
```mermaid
flowchart TD
    property([Sdf.PropertySpec])
    property --> attribute([Sdf.AttributeSpec])
    property --> relationship([Sdf.RelationshipSpec])
```

# Table of contents
1. [Properties](#propertyOverview)
2. [Attributes](#attributeOverview)
    1. [Attribute Types (Detail/Prim/Vertex/Point) (USD Speak: **Interpolation**)](#attributeInterpolation)
    2. [Attribute Data Types & Roles](#attributeDataTypeRole)
    3. [Static (Default) Values vs Time Samples vs Value Blocking](#attributeAnimation)
        1. [Re-writing a range of values from a different layer](#attributeReauthor)
    4. [Attribute To Attribute Connections (Node Graph Encoding)](#attributeConnections)
    5. [The **primvars** (primvars:<AttributeName>) namespace](#attributePrimvars)
        1. [Reading inherited primvars](#attributePrimvarsInherited)
        2. [Indexed Primvars](#attributePrimvarsIndexed)
    1. [Common Attribtes](#attributeCommon):
        1. [Purpose]
        1. [Proxy Prim]
        1. [Visiblity]
        1. [Extents Hint vs Extent]
        1. [Xform Ops]
1. [Relationships](#primProperties)
    1. [Collections](#relationshipCollections)
    1. [Relationships Forwarding](#relationshipForwarding)
1. [Common Schemas]

## Resources
- [Usd.Property](https://openusd.org/dev/api/class_usd_property.html)
- [Usd.Attribute](https://openusd.org/dev/api/class_usd_attribute.html)
- [Usd.Relationship](https://openusd.org/dev/api/stitch_clips_8h.html#details)
- [Usd.GeomPrimvar](https://openusd.org/release/api/class_usd_geom_primvar.html)
- [Usd.GeomPrimvarsAPI](https://openusd.org/dev/api/class_usd_geom_primvars_a_p_i.html)

## Properties <a name="propertyOverview"></a>
Let's first have a look at the shared base class `Usd.Property`. This inherits most its functionality from `Usd.Object`, which mainly exposes metadata data editing. We won't cover how metadata editing works for properties here, as it is extensively covered in our [metadata](./metadata.md#metadataSpecialProperty) section.

So let's inspect what else the class offers:
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:propertyOverview}}
```
~~~

As you can see, the `.GetProperty`/`.GetAttribute`/`.GetRelationship` methods return an object instead of just returning `None`. This way we can still check for `.IsDefined()`. We can also use them  as "truthy"/"falsy" objects, e.g. `if not attr` which makes it nicely readable.

For a practical of the `.GetPropertyStack()` method see our [Houdini](../../dcc/houdini/hda/timedependency.md) section, where we use it to debug if time varying data actually exists. We also cover it in more detail in our [composition](../composition/pcp.md) section.

## Attributes <a name="attributeOverview"></a>
Attributes in USD are the main data containers to hold all of you geometry related data. They are the only element in USD that can be [animateable](./animation.md).


### Attribute Types (Detail/Prim/Vertex/Point) (USD Speak: **Interpolation**) <a name="attributeInterpolation"></a>
To determine on what geo prim element an attribute applies to, attributes are marked with `interpolation` metadata.
We'll use Houdini's naming conventions as a frame of reference here:

You can read up more info in the [Usd.GeomPrimvar](https://openusd.org/release/api/class_usd_geom_primvar.html#Usd_InterpolationVals) docs page.

- `UsdGeom.Tokens.constant` (Same as Houdini's `detail`attributes): Global attributes (per prim in the hierarchy).
- `UsdGeom.Tokens.uniform` (Same as Houdini's `prim` attributes): Per prim attributes (e.g. groups of polygons).
- `UsdGeom.Tokens.faceVarying` (Same as Houdini's `vertex` attributes): Per vertex attributes (e.g. UVs).
- `UsdGeom.Tokens.varying` (Same as Houdini's `vertex` attributes): This the same as face varying, except for nurbs surfaces.
- `UsdGeom.Tokens.vertex` (Same as Houdini's `point` attributes): Per point attributes (e.g. point positions).

To summarize:

| Usd Name                  | Houdini Name |
|---------------------------|--------------|
|UsdGeom.Tokens.constant    | detail       |
|UsdGeom.Tokens.uniform     | prim         |
|UsdGeom.Tokens.faceVarying | vertex       |
|UsdGeom.Tokens.vertex      | point        |

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:attributeInterpolation}}
```
~~~

~~~admonish tip
For attributes that don't need to be accessed by Hydra (USD's render abstraction interface), we don't need to set the interpolation. In order for an attribute, that does not derive from a schema, to be accessible for the Hydra, we need to namespace it with `primvars:`, more info below at [primvars](#attributePrimvars). If the attribute element count for non detail (constant) attributes doesn't match the corresponding prim/vertex/point count, it will be ignored by the renderer (or crash it).

When we set schema attributes, we don't need to set the interpolation, as it is provided from the [schema](./schemas.md).
~~~

### Attribute Data Types & Roles <a name="attributeDataTypeRole"></a>
We cover how to work with data classes in detail in our [data types/roles](./data_type.md) section. For array attributes, USD has implemented the buffer protocol, so we can easily convert from numpy arrays to USD Vt arrays and vice versa. This allows us to write high performance attribute modifications directly in Python. See our [Houdini Particles](../../dcc/houdini/fx/particles.md) section for a practical example.

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:attributeDataTypeRole}}
```
~~~

The role specifies the intent of the data, e.g. `points`, `normals`, `color` and will affect how renderers/DCCs handle the attribute. This is not a concept only for USD, it is there in all DCCs. For example a color vector doesn't need to be influenced by transform operations where as normals and points do.

Here is a comparison to when we create an attribute a float3 normal attribute in Houdini.
![](./attributesDataRole.jpg#center)

### Static (Default) Values vs Time Samples vs Value Blocking <a name="attributeAnimation"></a>
We talk about how animation works in our [animation](./animation.md) section.

~~~admonish important
Attributes are the only part of USD than can encode time varying data.
~~~

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:animationOverview}}
```
~~~

We can set an attribute with a static value (USD speak `default`) or with time samples (or both, checkout the animation section on how to handle this edge case). We can also block it, so that USD sees it as if no value was written. For attributes from schemas with default values, this will make it fallback to the default value.

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:animationDefaultTimeSampleBlock}}
```
For more examples (also for the lower level API) check out the [animation](./animation.md) section.
~~~

#### Re-writing a range of values from a different layer <a name="attributeReauthor"></a>

~~~admonish danger
An important thing to note is that when we want to re-write the data of an attribute from a different layer, we have to get all the existing data first and then write the data, as otherwise we are changing the value source. To understand better why this happens, check out our [composition](../composition/overview.md) section.
~~~

Let's demonstrate this:
~~~admonish info title="Change existing values | Click to expand code" collapsible=true
```python
{{#include ../../../../code/core/elements.py:attributeReauthor}}
```
~~~

For heavy data it would be impossible to load everything into memory to offset it. USD's solution for that problem is [Layer Offsets](./animation.md#layer-offset-a-non-animateable-time-offsetscale-for-composition-arcs). 

What if we don't want to offset the values, but instead edit them like in the example above? 

In a production pipeline you usually do this via a DCC that imports the data, edits it and then re-exports it (often per frame and loads it via value clips). So we mitigate the problem by distributing the write to a new file(s) on multiple machines/app instances. Sometimes though we actually have to edit the samples in an existing file, for example when post processing data. In our [point instancer](../../dcc/houdini/fx/pointinstancers.md) section we showcase a practical example of when this is needed.

To edit the time samples directly, we can open the layer as a stage or edit the layer directly. To find the layers you can inspect the layer stack or value clips, but most of the time you know the layers, as you just wrote to them:
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:attributeReauthorPerLayer}}
```
~~~

#### The **primvars** (primvars:<AttributeName>) namespace <a name="attributePrimvars"></a>
Attributes in the `primvars` namespace `:` are USD's way of marking attributes to be exported for rendering. These can then be used by materials and AOVs. Primvars can be written per attribute type (detail/prim/vertex/point), it is up to the render delegate to correctly access them.

Primvars that are written as `detail` (UsdGeom.Tokens.constant interpolation) attributes, get inherited down the hierarchy. This makes them ideal transport mechanism of assigning render geometry properties, like dicing settings or render ray visibility.

~~~admonish important
- An attribute with the `primvars:` can be accessed at render time by your render delegate for things like settings, materials and AOVs
- `detail` (UsdGeom.Tokens.constant interpolation) primvars are inherited down the hierarchy, ideal to apply a constant value per USD prim, e.g. for render geometry settings or instance variation.
~~~
~~~admonish danger
- The term `inherited` in conjunction with `primvars` refers to a constant interpolation primvar being passed down to its children. It is not to be confused with `inherit` composition arcs.
~~~

To deal with primvars, the high level API has the `UsdGeom.PrimvarsAPI` [(API Docs)](https://openusd.org/dev/api/class_usd_geom_primvars_a_p_i.html). In the low level, we need to do everything ourselves. This create `UsdGeom.Primvar` [(API Docs)](https://openusd.org/dev/api/class_usd_geom_primvar.html) objects, that are similar `Usd.Attribute` objects, but with methods to edit primvars. To get the attribute call `primvar.GetAttr()`.

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:attributePrimvarAPI}}
```
~~~

##### Reading inherited primvars <a name="attributePrimvarsInherited"></a>
To speed up the lookup of inherited primvars see this guide [API Docs](https://openusd.org/dev/api/class_usd_geom_primvars_a_p_i.html#usdGeom_PrimvarFetchingAPI). Below is an example how to self implement a high performant lookup, as we couldn't get the `.FindIncrementallyInheritablePrimvars` to work with Python as expected.

~~~admonish danger title="High performance primvars inheritance calulation | Click to expand code" collapsible=true
```python
{{#include ../../../../code/core/elements.py:attributePrimvarInherited}}
```
~~~

##### Indexed primvars <a name="attributePrimvarsIndexed"></a>
Primvars can optionally be encoded via an index table. Let's explain via an example:

Here we store it without an index table, as you can see we have a lot of duplicates in our string list. 
This increases the file size when saving the attribute to disk.
```python
...
        string[] primvars:test = ["test_0", "test_0", "test_0", "test_0",
                                  "test_1", "test_1", "test_1", "test_1",
                                  "test_2", "test_2", "test_2", "test_2",
                                  "test_3", "test_3", "test_3", "test_3"] (
            interpolation = "uniform"
        )
        int[] primvars:test:indices = None
...
```
Instead we can encode it as a indexed primvar:
```python
...
        string[] primvars:test = ["test_0", "test_1", "test_2", "test_3"] (interpolation = "uniform")
        int[] primvars:test:indices = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3] ()
...
```
We can also flatten the index, when looking up the values. It should be preferred to keep the index, if you intend on updating the primvar.

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:attributePrimvarIndexed}}
```
~~~

If you are a Houdini user you might know this method, as this is how Houdini's internals also store string attributes.
You can find more info in the [USD Docs](https://openusd.org/release/api/class_usd_geom_primvar.html)


