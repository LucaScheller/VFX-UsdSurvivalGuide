# Loading & Traversing Data

# Table of contents
1. [Traversing & Loading Data In-A-Nutshell](#summary)
1. [What should I use it for?](#usage)
1. [Resources](#resources)
1. [Overview](#overview)
1. [Loading Mechanisms](#loadingMechanisms)
    1. [Layer Muting](#loadingMechanismsLayerMuting)
    1. [Prim Path Loading (USD speak: Prim Population)](#loadingMechanismsLayerPrimPopulation)
    1. [Payload Loading](#loadingMechanismsLayerPayloadLoading)
1. [Traversing Data](#traverseData)
    1. [Traversing Stages](#traverseDataStage)
    1. [Traversing Layers](#traverseDataLayer)

## TL;DR - Traversing & Loading Data In-A-Nutshell <a name="summary"></a>
- Main points to know

## What should I use it for? <a name="usage"></a>
~~~admonish tip
Summarize actual production relevance.
~~~

## Resources <a name="resources"></a>
- [API Docs]()

## Loading Mechanisms <a name="loadingMechanisms"></a>
Let's look at load mechanisms that USD offers to make the loading of our hierarchies faster.

Before we proceed, it is important to note, that USD is highly performant in loading hierarchies. When USD loads .usd/.usdc binary crate files, it sparsely loads the content: It can read in the hierarchy without loading in the attributes. This allows it to, instead of loading terabytes of data, to only read the important bits in the file and lazy load on demand the heavy data when requested by API queries or a hydra delegate. 

When loading stages/layers per code only, we often therefore don't need to resort to using these mechanisms.

There are three ways to influence the data load, from lowest to highest granularity .
- **Layer Muting**: This controls what layers are allowed to contribute to the composition result.
- **Prim Population**: This controls what prim paths to consider for loading at all.
- **Payload Loading**: This controls what prim paths, that have payloads, to load.

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
{{#include ../../../../code/core/elements.py:loadingMechanismsLayerMuting}}
```
~~~

~~~admonish tip title="Pro Tip | Layer Muting"
We use layer muting in production for two things:
- Artists can opt-in to load layers that are relevant to them. For example in a shot, a animator doesn't have to load the background set or fx layers.
- Pipeline-wise we have to ensure that artists add shot layers in a specific order (For example: lighting > fx > animation > layout >). For example, when a layout artist is working in a shot, we only want to display the layout and camera layers. All the other layers can (should) be muted, because A. performance, B. there might be edits in higher layers, that the layout artist is not interested in seeing yet. If we were to display them, some of these edits might block ours, because they are higher in the layer stack.
~~~

Here is an example of global layer muting:

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="layerMutingGlobal.mp4" type="video/mp4" alt="Houdini Layer Muting Global">
</video>

We have to re-cook the node for it to take effect, due to how Houdini caches stages.

### Prim Path Loading (USD speak: Prim Population) <a name="loadingMechanismsLayerPrimPopulation"></a>

'GetPopulationMask', 'SetPopulationMask',  'OpenMasked', 'ExpandPopulationMask', 



### Payload Loading <a name="loadingMechanismsLayerPayloadLoading"></a>
'Unload', 'LoadAndUnload', 'LoadNone',  'Load', 'LoadAll', 'InitialLoadSet',
'GetLoadRules', 'SetLoadRules','GetLoadSet',  'FindLoadable',  


## Traversing Data <a name="traverseData"></a>

### Traversing Stages <a name="traverseDataStage"></a>

### Traversing Layers <a name="traverseDataLayer"></a>





Purpose/Visibility/Activation/Population

Stages are the controller of how our [Prim Cache Population (PCP)](../composition/pcp.md) cache loads our composed layers. We cover this in detail in our [Traversing/Loading Data (Purpose/Visibility/Activation/Population)](./loading_mechanisms.md) section. (Technically it just exposes the PCP cache in a nice API, that forwards its requests to the stages's pcp cache `stage._GetPcpCache()`, similar hour all `Usd` ops are wrappers around `Sdf` calls.)




When traversing we commonly use these filter methods:
- Stage:
    - Layer m
- Prim:
    - Activation (Metadata)
    - Specifier (Metadata)
    - Kind (Metadata)
    - Purpose (Attribute)
    - Visiblity (Attribute)

