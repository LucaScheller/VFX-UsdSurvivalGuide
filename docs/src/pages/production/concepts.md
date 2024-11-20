# Advanced Concepts

# Table of Contents
1. [Edit Targets](#editTargets)
1. [Utility functions in the Usd.Utils module](#usdUtils)
1. [Utility functions in the Sdf module](#sdf)
    1. [Moving/Renaming/Removing prim/property/variant specs with Sdf.BatchNamespaceEdit()](#sdfBatchNamespaceEdit)
    1. [Copying data with Sdf.CopySpec](#sdfCopySpec)
    1. [Delaying change notifications with the Sdf.ChangeBlock](#sdfChangeBlock)
1. [Relationships](#relationship)
    1. [Special Relationships](#relationshipSpecial)
    1. [Relationship Forwarding (Binding post)](#relationshipForwarding)
    1. [Collections](#relationshipCollection)

## Edit Targets
~~~admonish tip title="Pro Tip | Edit Targets"
A edit target defines, what layer all calls in the high level API should write to.
~~~

An edit target's job is to map from one namespace to another, we mainly use them for writing to layers in the active layer stack (though we could target any layer) and to write variants, as these are written "inline" and therefore need an extra name space injection. 

We cover edit targets in detail in our [composition fundamentals](../core/composition/fundamentals.md#compositionFundamentalsEditTarget) section.

## Utility functions in the Usd.Utils module <a name="utilsUsdUtils"></a>
Usd provides a bunch of utility functions in the `UsdUtils` module ([USD Docs](https://openusd.org/dev/api/flatten_layer_stack_8h.html)):

For retrieving/upating dependencies:
- **UsdUtils.ExtractExternalReferences**: This is similar to `layer.GetCompositionAssetDependencies()`, except that it returns three lists: `[<sublayers>], [<references>], [<payloads>]`. It also consults the assetInfo metadata, so result might be more "inclusive" than `layer.GetCompositionAssetDependencies()`.
- **UsdUtils.ComputeAllDependencies**: This recursively calls `layer.GetCompositionAssetDependencies()` and gives us the aggregated result.
- **UsdUtils.ModifyAssetPaths**: This is similar to Houdini's output processors. We provide a function that gets the input path and returns a (modified) output path.

For animation and value clips stitching:
- Various tools for stitching/creating value clips. We cover these in our [animation section](../core/elements/animation.md#animationValueClips). These are also what the commandline tools that ship with USD use.

For collection authoring/compression:
- We cover these in detail in our [collection section](../core/elements/collection.md#collectionQuery).

## Utility functions in the Sdf module <a name="sdf"></a>

### Moving/Renaming/Removing prim/property/variant specs with Sdf.BatchNamespaceEdit() <a name="sdfBatchNamespaceEdit"></a>
We've actually used this quite a bit in the guide so far, so in this section we'll summarize its most important uses again:

#### Using Sdf.BatchNamespaceEdit() moving/renaming/removing prim/property (specs)
We main usage is to move/rename/delete prims. We can only run the name space edit on a layer, it does not work with stages.
Thats means if we have nested composition, we can't rename prims any more. In production this means we'll only be using this
with the "active" layer, that we are currently creating/editing. All the edits added are run in the order they are added,
we have to be careful what order we add removes/renames if they interfere with each other.

~~~admonish tip title="Sdf.BatchNamespaceEdit | Moving/renaming/removing prim/property specs | Click to expand!" collapsible=true
```python
{{#include ../../../../code/production/production.py:productionConceptsSdfBatchNamespaceMoveRenameDelete}}
```
~~~

#### Using Sdf.BatchNamespaceEdit() for variant creation
We can create variant via the namespace edit, because variants are in-line USD namespaced paths.

~~~admonish tip title="Sdf.BatchNamespaceEdit | Moving prim specs into variants | Click to expand!" collapsible=true
```python
{{#include ../../../../code/production/production.py:productionConceptsSdfBatchNamespaceEditVariant}}
```
~~~

We also cover variants in detail in respect to Houdini in our [Houdini - Tips & Tricks](../dcc/houdini/faq/overview.md) section.

### Copying data with Sdf.CopySpec <a name="sdfCopySpec"></a>
We use the `Sdf.CopySpec` method to copy/duplicate content from layer to layer (or within the same layer).

#### Copying specs (prim and properties) from layer to layer with Sdf.CopySpec()
The `Sdf.CopySpec` can copy anything that is representable via the `Sdf.Path`. This means we can copy prim/property/variant specs.
When copying, the default is to completely replace the target spec. 

We can filter this by passing in filter functions. Another option is to copy the content to a new anonymous layer and then
merge it via `UsdUtils.StitchLayers(<StrongLayer>, <WeakerLayer>)`. This is often more "user friendly" than implementing
a custom merge logic, as we get the "high layer wins" logic for free and this is what we are used to when working with USD.

~~~admonish question title="Still under construction!"
We'll add some examples for custom filtering at a later time.
~~~

~~~admonish tip title="Sdf.CopySpec | Copying prim/property specs | Click to expand!" collapsible=true
```python
{{#include ../../../../code/production/production.py:productionConceptsSdfCopySpecStandard}}
```
~~~

#### Using Sdf.CopySpec() for variant creation
We can also use `Sdf.CopySpec` for copying content into a variant.

~~~admonish tip title="Sdf.CopySpec | Copying prim specs into variants | Click to expand!" collapsible=true
```python
{{#include ../../../../code/production/production.py:productionConceptsSdfCopySpecVariant}}
```
~~~

We also cover variants in detail in respect to Houdini in our [Houdini - Tips & Tricks](../dcc/houdini/faq/overview.md) section.

### Delaying change notifications with the Sdf.ChangeBlock <a name="sdfChangeBlock"></a>
Whenever we edit something in our layers, change notifications get sent to all consumers (stages/hydra delegates) that use the layer. This causes them to recompute and trigger updates.

When performing a large edit, for example creating large hierarchies, we can batch the edit, so that the change notification gets the combined result.

~~~admonish danger title="Pro Tip | When/How to use Sdf.ChangeBlocks"
In theory it is only safe to use the change block with the lower level Sdf API.
We can also use it with the high level API, we just have to make sure that we don't accidentally query an attribute, that we just overwrote or perform ops on deleted properties.

We therefore recommend work with a read/write code pattern:
- We first query all the data via the Usd high level API
- We then write our data via the Sdf low level API

When writing data, we can also write it to a temporary anonymous layer, that is not linked to a stage and then merge the result back in via `UsdUtils.StitchLayers(anon_layer, active_layer)`. This is a great solution when it is to heavy to query all data upfront.
~~~

For more info see the [Sdf.ChangeBlock](https://openusd.org/dev/api/class_sdf_change_block.html) API docs.

~~~admonish tip title=""
```python
{{#include ../../../../code/production/production.py:productionConceptsSdfChangeBlock}}
```
~~~

## Relationships <a name="relationship"></a>

### Special Relationships <a name="relationshipSpecial"></a>
~~~admonish question title="Still under construction!"
This sub-section is still under development, it is subject to change and needs extra validation.
~~~
USD has a few "special" relationships that infer information on our hierarchy. These are:
- `proxyPrim`: This is a relationship from a prim with a render purpose to a prim with a proxy purpose. It can be used by clients to get low-resolution proxy representations (for example for simulations/collision detection etc.). Setting it is optional.

These special relationships have primvar like inheritance from parent to child prims:
- `material:binding`: This controls the material binding.
- `coordSys:<customName>`: Next to collections, this is currently the only other multi-apply API schema that ships natively with USD. It allows us to target an xform prim, whose transform we can then read into our shaders at render time.
- `skel:skeleton`/`skel:animationSource`:
    - `skel:skeleton`: This defines what skeleton prims with the skelton binding api schema should bind to.
    - `skel:animationSource`: This relationship can be defined on mesh prims to target the correct animation, but also on the skeletons themselves to select the skeleton animation prim.

### Relationship Forwarding (Binding post) <a name="relationshipForwarding"></a>
~~~admonish question title="Still under construction!"
This sub-section is still under development, it is subject to change and needs extra validation.
~~~

### Collections <a name="relationshipCollection"></a>
We cover collections in detail in our [collection section](../core/elements/collection.md#collectionQuery) with advanced topics like inverting or compressing collections.