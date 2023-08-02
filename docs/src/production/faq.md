# FAQ (Frequently Asked Questions)

# Table of Contents
1. [Should I prefer assets with a lot of prims or prefer combined meshes?](#faqPrimCount)
1. [How is "Frames Per Second" (FPS) handled in USD?](#faqFPS)
1. [How is the scene scale unit handled in USD?](#faqSceneScale)

## Should I prefer assets with a lot of prims or prefer combined meshes? <a name="faqPrimCount"></a>
When working in hierarchy based formats, an important influence factor of performance is the hierarchy size.

~~~admonish important title="Pro Tip | Hierarchy Size"
Basically it boils down to these rules:
Keep hierarchies as small as possible at all times, only start creating separates meshes when:
- your mesh point/prim count starts going into the millions
- you need to assign different render geometry settings
- you need to add different transforms
- you need to hide the prims individually
- you need separate materials (We can also use `UsdGeom.Subset`s, which are face selections per mesh, to assign materials, to workaround this)
~~~

At the end of the day it is a balancing act of **What do I need to be able to access separately in the hierarchy** vs **I have a prim that is super heavy (100 Gbs of data) and takes forever to load**.
A good viewpoint is the one of a lighting/render artist, as they are the ones that need to often work on individual (sub-)hierarchies and can say how it should be segmented.

## How is "frames per second" (FPS) handled in USD? <a name="faqFPS"></a>
Our time samples that are written in the time unit-less `{<frame>: <value> }` format are interpreted based on the `timeCodesPerSecond`/`framesPerSecond` metadata set in the session/root layer.

```python
(
    endTimeCode = 1010
    framesPerSecond = 24
    metersPerUnit = 1
    startTimeCode = 1001
    timeCodesPerSecond = 24
)
```
~~~admonish warning
If we want to load a let's say 24 FPS cache in a 25 FPS setup, we will have to apply a `Sdf.LayerOffset` when loading in the layer. This way we can move back the sample to the "correct" frame based times by scaling with a factor of 24/25.
~~~

You can find more details about the specific metadata priority and how to set the metadata in our [animation section](../core/elements/animation.md#frames-per-second).

## How is the scene scale unit and up axis handled in USD? <a name="faqSceneScale"></a>
We can supply an up axis and scene scale hint in the layer metadata, but this does not seem to be used by most DCCs or in fact Hydra itself when rendering the geo. So if you have a mixed values, you'll have to counter correct via transforms yourself.

The default scene `metersPerUnit` value is centimeters (0.01) and the default `upAxis` is `Y`.

You can find more details about how to set these metrics see our [layer metadata section](../core/elements/metadata.md#readingwriting-stage-and-layer-metrics-fpsscene-unit-scaleup-axis-highlow-level-api).