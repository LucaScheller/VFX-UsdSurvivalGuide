# Advanced Concepts


## Moving/Renaming/Removing prim specs with Sdf.BatchNamespaceEdit()


## Sdf.CopySpec

## Delaying change notifications with the Sdf.ChangeBlock
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



## Relationships
- xform space rel
- proxy prim rel
- material binding rel
- skeleton anim rel

### Edit Targets

### Collections
- Invert collection
- 

### Relationship Forwarding (Binding post)
~~~admonish question title="Still under construction!"
This sub-section is still under development, it is subject to change and needs extra validation.
~~~

## Remapping assets path in current layer stack