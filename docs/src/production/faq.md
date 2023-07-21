# FAQ (Frequently Asked Questions)

# Table of contents
1. [How is "Frames Per Second" (FPS) handled in USD?](#faqFPS)
1. [How is the scene scale unit handled in USD?](#faqFPS)


## How is "frames per second" (FPS) handled in USD?
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

## How is the scene scale unit and up axis handled in USD?
We can supply an up axis and scene scale hint in the layer metadata, but this does not seem to be used by most DCCs or in fact Hydra itself when rendering the geo. So if you have a mixed values, you'll have to counter correct via transforms yourself.

The default scene `metersPerUnit` value is centimeters (0.01) and the default `upAxis` is `Y`.

You can find more details about how to set these metrics see our [layer metadata section](../core/elements/metadata.md#readingwriting-stage-and-layer-metrics-fpsscene-unit-scaleup-axis-highlow-level-api).