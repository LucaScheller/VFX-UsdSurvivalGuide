# Composition Deep Dive
~~~admonish question title="Still under construction!"
As composition is USD's most complicated topic, this section will be enhanced with more examples in the future.
If you detect an error or have useful production examples, please [submit a ticket](https://github.com/LucaScheller/VFX-UsdSurvivalGuide/issues/new), so we can improve the guide!
~~~


- Pixar Glossary Examples
- Pixar FAQ Examples
- Production Examples




USD's mechanism of linking different USD files with each other is called `composition`. Let's first clarify some terminology before we start, so that we are all on the same page:
- **`layer`**: A layer is an USD file on disk with [prims](../elements/prim.md) & [properties](../elements/property.md). (Technically it can also be in memory, but for simplicity on this page, let's think of it as a file on disk). More info in our [layer section](../elements/layer.md).
- **`layer stack`**: A stack of layers (Hehe 😉). We'll explain it more in detail below, just remember that composition targets the layer stack, never individual layers.
- **`composition arc`**: A method of linking (pointing to) another layer or another part of the scene hierarchy. USD has several, each with a specific behavior.
- **`prim index`**: Once USD has processed all of our composition arcs, it builds a `prim index` that tracks where values can come from. We can think of the `prim index` as something that outputs an ordered list of `[(<layer (stack)>, <hierarchy path>), (<layer (stack)>, <hierarchy path>)]` ordered by the composition rules.
- **`composed value`**: When looking up a value of a property, USD then checks each location of the `prim index` for a value and moves on to the next one if it can't find one. If no value was found, it uses a schema fallback (if the property came from a schema), other wise it falls back to not having a value (USD speak: not being `authored`).

Composition is "easy" to explain in theory, but hard to master in production. It also a topic that keeps on giving and makes you question if you really understand USD. So don't worry if you don't fully understand the concepts of this page, they can take a long time to master. To be honest, it's one of those topics that you have to read yourself back into every time you plan on making larger changes to your pipeline.

We recommend really playing through as much scenarios as possible before you start using USD in production. Houdini is one of the best tools on the market that let's you easily concept and play around with composition. Therefore we will use it in our examples below.

Now before we talk about individual `composition arcs`, let's first focus on three different principles composition runs on.
These three principles build on each other, so make sure you work through them in order they are listed below.


## List-Editable Operations (Ops)
USD has the concept of list editable operations. Instead of having a "flat" array (`[Sdf.Path("/cube"), Sdf.Path("/sphere")]`) that stores what files/hierarchy paths we want to point to, we have wrapper array class that stores multiple sub-arrays. When flattening the list op, USD removes duplicates, so that the end result is like an ordered Python `set()`.

To make it even more confusing, composition arc list editable ops run on a different logic than "normal" list editable ops when looking at the final `composed value`.

We take a closer look at "normal" list editable ops (and "composition" list editable ops) in our [List Editable Ops section](./listeditableops.md), on this page we'll stay focused on the composition ones.

Alright, let's have a quick primer on how these work. There are three sub-classes for composition related list editable ops:
- `Sdf.ReferenceListOp`: The list op for the `reference` composition arc, stores `Sdf.Reference` objects.
- `Sdf.PayloadListOp`: The list op for the `payload` composition arc, stores `Sdf.Reference` objects.
- `Sdf.PathListOp`: The list op for `inherit` and `specialize` composition arcs, as these arcs target another part of the hierarchy (hence `path`) and not a layer. It stores `Sdf.Path` objects.

These are 100% identical in terms of list ordering functionality, the only difference is what items they can store (as noted above). Let's start of simple with looking at the basics:

~~~admonish tip title=""
```python
{{#include ../../../../code/core/composition.py:compositionListEditableOpsBasics}}
```
~~~

So far so good? Now let's look at how multiple of these list editable ops are combined. If you remember our [layer](../elements/layer.md) section, each layer stores our prim specs and property specs. The composition list editable ops are stored as metadata on the prim specs. When USD composes the stage, it combines these and then starts building the composition based on the composed result of these metadata fields.

Let's mock how USD does this without layers:

~~~admonish tip title=""
```python
{{#include ../../../../code/core/composition.py:compositionListEditableOpsMerging}}
```
~~~

When working with multiple layers, each layer can have list editable ops data in the composition metadata fields. It then gets merged, as mocked above. The result is a single flattened list, without duplicates, that then gets fed to the composition engine.

Here comes the fun part:

~~~admonish danger title="List-Editable Ops | Combined Value"
When looking at the metadata of a prim via UIs (USD View/Houdini) or getting it via the Usd.Prim.GetMetadata() method, you will only see the list editable op of the last layer that edited the metadata, **NOT** the composed result. 

This is probably the most confusing part of USD in my opinion when first starting out. To inspect the full composition result, we actually have to consult the [PCP](pcp.md) cache or run a `Usd.PrimCompositionQuery`. There is a caveat though, as you'll see in the next section: Composition is **encapsulated**. This means our edits to list editable ops only work in the active `layer stack`. More info below!
~~~









So far so good? Now let's bring layers/a layer stack into the mix. 



~~~admonish danger title="List-Editable Ops | Combined Value"
When multiple list editable ops from different layers get combined, each individual sub-list in each list editable op gets combined based on the layer order. It does not get "applied" in the sense that it flattens out the list to a single 

It is very important to know, that list editable ops only store lists these sublists, and don't actually 

~~~



~~~admonish tip title=""
```python

# No you m


# To get only added/explicit items (This does not make use of the deleteItems remove list!):
print(path_list_op.GetAddedOrExplicitItems()) # Returns: [Sdf.Path('/cube'), Sdf.Path('/sphere')]
print(path_list_op.GetAddedOrExplicitItems()) # Returns: [Sdf.Path('/cube'), Sdf.Path('/sphere')]

# We can also mark it as "explicit", this means that any other values from la

['ApplyOperations', 'Clear', 'ClearAndMakeExplicit', 'Create', 'CreateExplicit', 'GetAddedOrExplicitItems', 
'HasItem', 'isExplicit',

# Setup scene
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
layer_top = Sdf.Layer.CreateAnonymous()
layer_middle = Sdf.Layer.CreateAnonymous()
layer_bottom = Sdf.Layer.CreateAnonymous()
layers = [layer_top, layer_middle, layer_bottom]
stage.GetRootLayer().subLayerPaths = [l.identifier for l in layers]
prim_path = Sdf.Path("/cube")
for layer in layers:
    prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
    prim_spec.specifier = Sdf.SpecifierDef
    prim_spec.typeName = "Cube"
top_prim_spec = layer_top.GetPrimAtPath(prim_path)
middle_prim_spec = layer_middle.GetPrimAtPath(prim_path)
bottom_prim_spec = layer_bottom.GetPrimAtPath(prim_path)
# Write list editable ops for inherits

```
~~~

## Encapsulation





## Layer Stack
Now if you read through the USD docs/glossary, you'll notice a recurring sentence, when it comes to composition:
 
~~~admonish important title=""
Composition arcs target the layer stack, not individual layers.
~~~

This is absolutely crucial to understand.











