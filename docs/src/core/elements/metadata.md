# Metadata
Metadata is the smallest building block in Usd. It is part of the base class from which prims and properties inherit from and posses a slightly different feature set than other parts of Usd.

Here is the class structure for the different API levels:
High Level API
```mermaid
flowchart TD
    usdObject(["Usd.Object (Includes Metadata API)"]) --> usdPrim([Usd.Prim])
    usdObject --> usdProperty([Usd.Property])
    usdProperty --> usdAttribute([Usd.Attribute])
    usdProperty --> usdRelationship([Usd.Relationship])
    usdStage(["Usd.Stage (Includes Metadata API)"])
```

Low Level API
```mermaid
flowchart TD
    sdfSpec(["Sdf.Spec (Includes Metadata API)"]) --> sdfPropertySpec([Sdf.Property])
    sdfSpec --> sdfPrimSpec([Sdf.PrimSpec])
    sdfSpec --> sdfVariantSetSpec([Sdf.VariantSetSpec])
    sdfSpec --> sdfVariantSpec([Sdf.VariantSpec])
    sdfPropertySpec --> sdfAttributeSpec([Sdf.AttributeSpec])
    sdfPropertySpec --> sdfRelationshipSpec([Sdf.RelationshipSpec])
    sdfLayer(["Sdf.Layer (Includes Metadata API)"])

```

Metadata is different in that it:
- Is the smallest building block in Usd (There are no subclasses) and its data is stored vias a dictionary.
- Is extremely fast to access
- Can't be time varying:
    - Composition arcs are written into metadata fields on prims, so you can't animate composition.
    - Metadata stored in value clip files is ignored
- Is strongly typed via schemas, so you need to register a custom schema if you want custom keys. This way we can ensure fallback values/documentation per key/value and avoid random data flying through your pipelines. For example all your mesh attributes have metadata for exactly what type/role they must match.
- There are two special metadata keys:
    - "AssetInfo": Here you should dump asset related data. This is just a predefined standardized location all vendors/companies should adhere to when writing asset data that should be tracked.
    - "customData": Here you can dump any data you want, a kind of scratch space, so you don't need to add you own schema. If you catch yourself misusing it too much, you should probably generate your own schema.


~~~admonish tip
We go into more detail over in the [schema](./schemas.md) section on how to create or lookup registered schemas.
~~~

## TL;DR - Metadata In-A-Nutshell
- Metadata attaches additional non-animatable data to prims/properties/layers via a dictionary
- Composition arcs and core data (specifiers/type names) is added via metadata
- 'AssetInfo' and 'customData' are predefined keys for prim metadata you can track asset/custom data with
- To write to other keys, they must be registered via schemas.

# What should I use it for?
~~~admonish tip
In production, you'll use the 'AssetInfo'/'customData' prim metadata fields to track any production related data.

```python
prim.SetInfo()
```
~~~

## Resources
- [Metadata API Docs](https://openusd.org/release/api/_usd__page__object_model.html#Usd_OM_Metadata)
- [Usd.Object](https://openusd.org/dev/api/class_usd_object.html)
- [Sdf.Spec](https://openusd.org/dev/api/class_sdf_spec.html)

## Composition/Value resolution
Metadata is slightly different when it comes to value resolution. (As a reminder: `value resolution` is just a fancy word for "what layer has the winning value out of all your layers where the data will be loaded from"):
- Nested dictionaries are combined
- Attribute metadata behaves by the same rules as attribute value resolution
- Core metadata (Metadata that affects composition/prim definitions):
    - Composition metadata is composed via Listeditable-Ops. See our section [here](../composition/listeditableops.md) for more details. Be sure to understand these to save your self a lot of head-aches why composition works the way it does.
    - Specific prim metadata has its own rule set (E.g. prim specifiers).
