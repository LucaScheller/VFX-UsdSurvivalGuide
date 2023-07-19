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
    5. [The **primvars:** namespace](#attributeConnections)
    6. [Common Attribtes](#attributeCommon):
        1. [Purpose]
        1. [Proxy Prim]
        1. [Visiblity]
        1. [Extents Hint vs Extent]
        1. [Xform Ops]
3. [Relationships](#primProperties)
    1. [Collections](#relationshipCollections)
    1. [Relationships Forwarding](#relationshipForwarding)
4. [Common Schemas]

## Resources
- [Usd.Property](https://openusd.org/dev/api/class_usd_property.html)
- [Usd.Attribute](https://openusd.org/dev/api/class_usd_attribute.html)
- [Usd.Relationship](https://openusd.org/dev/api/stitch_clips_8h.html#details)
- [Usd.GeomPrimvar](https://openusd.org/release/api/class_usd_geom_primvar.html)

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
```python
{{#include ../../../../code/core/elements.py:attributeReauthor}}
```

test