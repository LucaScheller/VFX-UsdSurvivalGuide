# Advanced Concepts

# Table of contents
1. [Edit Targets](#editTargets)
1. [Utility functions in the Usd.Utils module](#usdUtils)
1. [Utility functions in the Sdf module](#sdf)
    1. [Moving/Renaming/Removing prim specs with Sdf.BatchNamespaceEdit()](#sdfBatchNamespaceEdit)
    1. [Copying data in the low level API with Sdf.CopySpec](#sdfCopySpec)
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

### Moving/Renaming/Removing prim specs with Sdf.BatchNamespaceEdit() <a name="sdfBatchNamespaceEdit"></a>

### Sdf.CopySpec <a name="sdfCopySpec"></a>

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
from pxr import Sdf, Tf, Usd
def callback(notice, sender):
    print("Changed Paths", notice.GetResyncedPaths())
stage = Usd.Stage.CreateInMemory()
# Add
listener = Tf.Notice.Register(Usd.Notice.ObjectsChanged, callback, stage)
# Edit
layer = stage.GetEditTarget().GetLayer()
for idx in range(5):
    Sdf.CreatePrimInLayer(layer, Sdf.Path(f"/test_{idx}"))
# Remove
listener.Revoke()
# Returns:
"""
Changed Paths [Sdf.Path('/test_0')]
Changed Paths [Sdf.Path('/test_1')]
Changed Paths [Sdf.Path('/test_2')]
Changed Paths [Sdf.Path('/test_3')]
Changed Paths [Sdf.Path('/test_4')]
"""
stage = Usd.Stage.CreateInMemory()
# Add
listener = Tf.Notice.Register(Usd.Notice.ObjectsChanged, callback, stage)
with Sdf.ChangeBlock():
    # Edit
    layer = stage.GetEditTarget().GetLayer()
    for idx in range(5):
        Sdf.CreatePrimInLayer(layer, Sdf.Path(f"/test_{idx}"))
# Remove
listener.Revoke()
# Returns:
# Changed Paths [Sdf.Path('/test_0'), Sdf.Path('/test_1'), Sdf.Path('/test_2'), Sdf.Path('/test_3'), Sdf.Path('/test_4')]
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