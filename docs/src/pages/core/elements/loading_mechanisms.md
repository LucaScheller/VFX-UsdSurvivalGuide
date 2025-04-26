# Loading & Traversing Data

# Table of Contents
1. [Traversing & Loading Data In-A-Nutshell](#summary)
1. [What should I use it for?](#usage)
1. [Resources](#resources)
1. [Overview](#overview)
1. [Loading Mechanisms](#loadingMechanisms)
    1. [Layer Muting](#loadingMechanismsLayerMuting)
    1. [Prim Path Loading (USD speak: Prim Population Mask)](#loadingMechanismsLayerPrimPopulationMask)
    1. [Payload Loading](#loadingMechanismsLayerPayloadLoading)
    1. [GeomModelAPI->Draw Mode](#loadingMechanismsGeomModelAPIDrawMode)
1. [Traversing Data](#traverseData)
    1. [Traversing Stages](#traverseDataStage)
    1. [Traversing Layers](#traverseDataLayer)
    1. [Traverse Sample Data/Profiling](#traverseDataProfiling)

## TL;DR - Loading & Traversing Data In-A-Nutshell <a name="summary"></a>
#### Loading Mechanisms
When loading large scenes, we can selectively disabling loading via the following loading mechanisms:
There are three ways to influence the data load, from lowest to highest granularity .
- **Layer Muting**: This controls what layers are allowed to contribute to the composition result.
- **Prim Population Mask**: This controls what prim paths to consider for loading at all.
- **Payload Loading**: This controls what prim paths, that have payloads, to load.
- **GeomModelAPI->Draw Mode**: This controls per prim how it should be drawn by delegates. It can be one of "Full Geometry"/"Origin Axes"/"Bounding Box"/"Texture Cards". It requires the kind to be set on the prim and all its ancestors. Therefore it is "limited" to (asset-) root prims and ancestors.
- **Activation**: Control per prim whether load itself and its child hierarchy. This is more an artist facing mechanism, as we end up writing the data to the stage, which we don't do with the other methods.

#### Traversing/Iterating over our stage/layer
To inspect our stage, we can iterate (traverse) over it:

When traversing, we try to pre-filter our prims as much as we can, via our prim metadata and USD core features(metadata), before inspecting their properties. This keeps our traversals fast even with hierarchies with millions of prims. We recommend first filtering based on metadata, as this is a lot faster than trying to access attributes and their values.

We also have a thing called [predicate](https://openusd.org/dev/api/prim_flags_8h.html#Usd_PrimFlags), which just defines what core metadata to consult for pre-filtering the result.

Another important feature is stopping traversal into child hierarchies. This can be done by calling `ìterator.PruneChildren()

~~~admonish tip title="Stage/Prim Traversal"
```python
{{#include ../../../../../code/core/elements.py:traverseDataStageTemplate}}
```
~~~

Layer traversal is a bit different. Instead of iterating, we provide a function, that gets called with each `Sdf.Path` representable object in the active layer. So we also see all properties, relationship targets and variants.

~~~admonish tip title="Layer Traversal"
```python
{{#include ../../../../../code/core/elements.py:traverseDataLayerTemplate}}
```
~~~

## What should I use it for? <a name="usage"></a>
~~~admonish tip
We'll be using loading mechanisms to optimize loading only what is relevant for the current task at hand.
~~~

## Resources <a name="resources"></a>
- [Prim Cache Population (Pcp)](https://openusd.org/dev/api/pcp_page_front.html)
- [Stage Payload Loading](https://openusd.org/dev/api/class_usd_stage.html#Usd_workingSetManagement)
- [Pcp.Cache](https://openusd.org/dev/api/class_pcp_cache.html)
- [Usd.StagePopulationMask](https://openusd.org/dev/api/class_usd_stage_population_mask.html)
- [Usd.StageLoadRules](https://openusd.org/dev/api/class_usd_stage_load_rules.html)

## Loading Mechanisms <a name="loadingMechanisms"></a>
Let's look at load mechanisms that USD offers to make the loading of our hierarchies faster.

Before we proceed, it is important to note, that USD is highly performant in loading hierarchies. When USD loads .usd/.usdc binary crate files, it sparsely loads the content: It can read in the hierarchy without loading in the attributes. This allows it to, instead of loading terabytes of data, to only read the important bits in the file and lazy load on demand the heavy data when requested by API queries or a hydra delegate. 

When loading stages/layers per code only, we often therefore don't need to resort to using these mechanisms.

There are three ways to influence the data load, from lowest to highest granularity .
- **Layer Muting**: This controls what layers are allowed to contribute to the composition result.
- **Prim Population Mask**: This controls what prim paths to consider for loading at all.
- **Payload Loading**: This controls what prim paths, that have payloads, to load.
- **GeomModelAPI->Draw Mode**: This controls per prim how it should be drawn by delegates. It can be one of "Full Geometry"/"Origin Axes"/"Bounding Box"/"Texture Cards". It requires the kind to be set on the prim and all its ancestors. Therefore it is "limited" to (asset-) root prims and ancestors.
- **Activation**: Control per prim whether load itself and its child hierarchy. This is more an artist facing mechanism, as we end up writing the data to the stage, which we don't do with the other methods.

Stages are the controller of how our [Prim Cache Population (PCP)](../composition/pcp.md) cache loads our composed layers. Technically the stage just exposes the PCP cache in a nice API, that forwards its requests to its PCP cache `stage._GetPcpCache()`, similar how all `Usd` ops are wrappers around `Sdf` calls.


Houdini exposes all three in two different ways:
- **Configue Stage** LOP node: This is the same as setting it per code via the stage.
- **Scene Graph Tree** panel: In Houdini, that stage that gets rendered, is actually not the stage of your node (at least what we gather from reverse engineering). Instead it is a duplicate, that has overrides in the session layer and loading mechanisms listed above.

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="../../../media/core/elements/houdiniLoadingMechanisms.mp4" type="video/mp4" alt="Houdini Configure Stage Node">
</video>

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="../../../media/core/elements/houdiniSceneGraphTreePanel.mp4" type="video/mp4" alt="Houdini Scene Graph Tree Panel">
</video>

More Houdini specific information can be found in our [Houdini - Performance Optimizations](../../dcc/houdini/performance/overview.md#loadingMechanisms) section.

### Layer Muting <a name="loadingMechanismsLayerMuting"></a>
We can "mute" (disable) layers either globally or per stage.

Globally muting layers is done via the singleton, this mutes it on all stages that use the layer.
~~~admonish tip title=""
```python
from pxr import Sdf
layer = Sdf.Layer.FindOrOpen("/my/layer/identifier")
Sdf.Layer.AddToMutedLayers(layer.identifier)
Sdf.Layer.RemoveFromMutedLayers(layer.identifier)
```
~~~

Muting layers per stage is done via the `Usd.Stage` object, all function signatures work with the layer identifier string. If the layer is muted globally, the stage will not override the muting and it stays muted.
~~~admonish tip title=""
```python
{{#include ../../../../../code/core/elements.py:loadingMechanismsLayerMuting}}
```
~~~

~~~admonish tip title="Pro Tip | Layer Muting"
We use layer muting in production for two things:
- Artists can opt-in to load layers that are relevant to them. For example in a shot, a animator doesn't have to load the background set or fx layers.
- Pipeline-wise we have to ensure that artists add shot layers in a specific order (For example: lighting > fx > animation > layout >). Let's say a layout artist is working in a shot, we only want to display the layout and camera layers. All the other layers can (should) be muted, because A. performance, B. there might be edits in higher layers, that the layout artist is not interested in seeing yet. If we were to display them, some of these edits might block ours, because they are higher in the layer stack.
~~~

Here is an example of global layer muting:

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="../../../media/core/elements/layerMutingGlobal.mp4" type="video/mp4" alt="Houdini Layer Muting Global">
</video>

We have to re-cook the node for it to take effect, due to how Houdini caches stages.

### Prim Path Loading Mask (USD speak: Prim Population Mask) <a name="loadingMechanismsLayerPrimPopulationMask"></a>

~~~admonish tip title="Pro Tip | Prim Population Mask"
Similar to prim activation, the prim population mask controls what prims (and their child prims) are even considered for being loaded into the stage. Unlike activation, the prim population mask does not get stored in a USD layer. It is therefore a pre-filtering mechanism, rather than an artist facing "what do I want to hide from my scene" mechanism.
~~~

One difference to activation is that not only the child hierarchy is stripped away for traversing, but also the prim itself, if it is not included in the mask.

The population mask is managed via the `Usd.StagePopulationMask` class.


~~~admonish tip title=""
```python
{{#include ../../../../../code/core/elements.py:loadingMechanismsLayerPrimPopulationMask}}
```
~~~

What's also really cool, is that we can populate the mask by relationships/attribute connections.

~~~admonish tip title=""
```python
stage.ExpandPopulationMask(relationshipPredicate=lambda r: r.GetName() == 'material:binding',
                           attributePredicate=lambda a: False)
```
~~~

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="../../../media/core/elements/houdiniPopulationMaskExpand.mp4" type="video/mp4" alt="Houdini Population Mask Expand">
</video>

### Payload Loading <a name="loadingMechanismsLayerPayloadLoading"></a>
~~~admonish tip title="Pro Tip | Payload Loading"
Payloads are USD's mechanism of disabling the load of heavy data and instead leaving us with a bounding box representation (or texture card representation, if you set it up). We can configure our stages to not load payloads at all or to only load payloads at specific prims.
~~~

What might be confusing here is the naming convention: USD refers to this as "loading", which sounds pretty generic. Whenever we are looking at stages and talking about loading, know that we are talking about payloads.

You can find more details in the [API docs](https://openusd.org/dev/api/class_usd_stage.html#Usd_workingSetManagement).

~~~admonish tip title=""
```python
{{#include ../../../../../code/core/elements.py:loadingMechanismsLayerPayloadLoading}}
```
~~~

### GeomModelAPI->Draw Mode <a name="loadingMechanismsGeomModelAPIDrawMode"></a>
~~~admonish tip title="Pro Tip | Draw Mode"
The draw mode can be used to tell our Hydra render delegates to not render a prim and its child hierarchy. Instead it will only display a preview representation.

The preview representation can be one of:
- Full Geometry
- Origin Axes
- Bounding Box
- Texture Cards

Like visibility, the draw mode is inherited downwards to its child prims. We can also set a draw mode color, to better differentiate the non full geometry draw modes, this is not inherited though and must be set per prim.
~~~

~~~admonish danger title="Important | Draw Mode Requires Kind"
In order for the draw mode to work, the prim and all its ancestors, must have a [kind](../plugins/kind.md) defined. Therefore it is "limited" to (asset-)root prims and its ancestors.
See the [official docs](https://openusd.org/dev/api/class_usd_geom_model_a_p_i.html) for more info.
~~~

Here is how we can set it via Python, it is part of the `UsdGeomModelAPI`:

~~~admonish tip title=""
```python
{{#include ../../../../../code/core/elements.py:loadingMechanismsGeomModelAPIDrawMode}}
```
~~~

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="../../../media/core/elements/houdiniLoadingMechanismsDrawMode.mp4" type="video/mp4" alt="Houdini Draw Mode">
</video>


## Traversing Data <a name="traverseData"></a>
When traversing (iterating) through our hierarchy, we commonly use these metadata and property entries on prims to pre-filter what we want to access:
- .IsA Typed Schemas (Metadata)
- Type Name (Metadata)
- Specifier (Metadata)
- Activation (Metadata)
- Kind (Metadata)
- Purpose (Attribute)
- Visibility (Attribute)

~~~admonish tip title="Pro Tip | High Performance Traversals"
When traversing, using the above "filters" to narrow down your selection well help keep your traversals fast, even with hierarchies with millions of prims. We recommend first filtering based on metadata, as this is a lot faster than trying to access attributes and their values.

Another important feature is stopping traversal into child hierarchies. This can be done by calling `ìterator.PruneChildren()`:
```python
from pxr import Sdf, UsdShade
root_prim = stage.GetPseudoRoot()
# We have to cast it as an iterator to gain access to the .PruneChildren() method.
iterator = iter(Usd.PrimRange(root_prim))
for prim in iterator:
    if prim.IsA(UsdShade.Material):
        # Don't traverse into the shader network prims
        iterator.PruneChildren()
```
~~~

### Traversing Stages <a name="traverseDataStage"></a>
Traversing stages works via the `Usd.PrimRange` class. The `stage.Traverse`/`stage.TraverseAll`/`prim.GetFilteredChildren` methods all use this as the base class, so let's checkout how it works:

We have two traversal modes:
- Default: Iterate over child prims
- PreAndPostVisit: Iterate over the hierarchy and visit each prim twice, once when first encountering it, and then again when "exiting" the child hierarchy. See our [primvars query](../../production/caches/attribute.md#primvars) section for a hands-on example why this can be useful.

We also have a thing called "predicate"([Predicate Overview](https://openusd.org/dev/api/prim_flags_8h.html#Usd_PrimFlags)), which just defines what core metadata to consult for pre-filtering the result:
- Usd.PrimIsActive: Usd.Prim.IsActive() - If the "active" metadata is True
- Usd.PrimIsLoaded: Usd.Prim.IsLoaded() - If the (ancestor) payload is loaded
- Usd.PrimIsModel: Usd.Prim.IsModel() - If the kind is a sub kind of `Kind.Tokens.model`
- Usd.PrimIsGroup: Usd.Prim.IsGroup() - If the kind is `Kind.Tokens.group`
- Usd.PrimIsAbstract: Usd.Prim.IsAbstract() - If the prim specifier is `Sdf.SpecifierClass`
- Usd.PrimIsDefined: Usd.Prim.IsDefined() - If the prim specifier is `Sdf.SpecifierDef`
- Usd.PrimIsInstance: Usd.Prim.IsInstance() - If prim is an instance root (This is false for prims in instances)

Presets:
- Usd.PrimDefaultPredicate: `Usd.PrimIsActive & Usd.PrimIsDefined & Usd.PrimIsLoaded & ~Usd.PrimIsAbstract`
- Usd.PrimAllPrimsPredicate: Shortcut for selecting all filters (basically ignoring the prefilter).

By default the Usd.PrimDefaultPredicate is used, if we don't specify one.

~~~admonish tip title="Pro Tip | Usd Prim Range"
Here is the most common syntax you'll be using:
```python
{{#include ../../../../../code/core/elements.py:traverseDataStageTemplate}}
```
~~~

The default traversal also doesn't go into [instanceable prims](../composition/livrps.md#compositionInstance).
To enable it we can either run `pxr.Usd.TraverseInstanceProxies(<existingPredicate>)` or `predicate.TraverseInstanceProxies(True)`

Within instances we can get the prototype as follows, for more info see our [instanceable section](../composition/livrps.md#compositionInstance):
~~~admonish tip title=""
```python
{{#include ../../../../../code/core/composition.py:compositionInstanceable}}
```
~~~

Let's look at some traversal examples:

~~~admonish tip title="Stage/Prim Traversal | Click to expand" collapsible=true
```python
{{#include ../../../../../code/core/elements.py:traverseDataStage}}
```
~~~

### Traversing Layers <a name="traverseDataLayer"></a>
Layer traversal is different, it only looks at the active layer and traverses everything that is representable via an `Sdf.Path` object.
This means, it ignores activation and it traverses into variants and relationship targets. This can be quite useful, when we need to rename something or check for data in the active layer.

We cover it in detail with examples over in our [layer and stages](./layer.md#layerTravesal) section.

~~~admonish tip title="Pro Tip | Layer Traverse"
The traversal for layers works differently. Instead of an iterator, we have to provide a
"kernel" like function, that gets an `Sdf.Path` as an input.
Here is the most common syntax you'll be using:
```python
{{#include ../../../../../code/core/elements.py:traverseDataLayerTemplate}}
```
~~~

### Traverse Sample Data/Profiling <a name="traverseDataProfiling"></a>
To test profiling, we can setup a example hierarchy. The below code spawns a nested prim hierarchy.
You can adjust the `create_hierarchy(layer, prim_path, <level>)`, be aware this is exponential, so a value of 10 and higher will already generate huge hierarchies.

The output will be something like this:

![Houdini Traversal Profiling Hierarchy](../../../media/core/composition/traversalProfilingHierarchy.jpg)

~~~admonish tip title=""
```python
{{#include ../../../../../code/core/elements.py:traverseSampleData}}
```
~~~

Here is how we can run profiling (this is kept very simple, check out our [profiling](../profiling/overview.md) section how to properly trace the stats) on the sample data:
~~~admonish tip title=""
```python
{{#include ../../../../../code/core/elements.py:traverseSampleDataProfiling}}
```
~~~

Here is a sample output, we recommend running each traversal multiple times and then averaging the results.
As we can see running attribute checks against attributes can be twice as expensive than checking metadata or the type name. (Surprisingly kind checks take a long time, even though it is also a metadata check) 
~~~admonish tip title=""
```python
0.17678 Seconds | IsA(Boundable) | Match 38166
0.17222 Seconds | GetTypeName | Match 44294
0.42160 Seconds | Kind | Match 93298
0.38575 Seconds | IsLeaf AssetInfo  | Match 44294
0.27142 Seconds | IsLeaf Attribute Has | Match 44294
0.38036 Seconds | IsLeaf Attribute  | Match 44294
0.37459 Seconds | IsLeaf Attribute (Validation) | Match 44294
```
~~~

