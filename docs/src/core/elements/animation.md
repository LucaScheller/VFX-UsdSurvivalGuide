# Animation/Time Varying Data
Usd encodes time related data in a very simple format:
```json
{
    <frame>: <value>
}
```

# Table of contents
1. [Animation/Time Varying Data In-A-Nutshell](#summary)
2. [What should I use it for?](#usage)
3. [Resources](#resources)
4. [Overview](#overview)
    1. [Time Code](#animationTimeCode)
    2. [Layer Offset](#animationLayerOffset)
    3. [Reading & Writing time samples](#animationReadWrite)
    4. [Frames Per Second](#animationMetadata)
    5. [Stitching/Combining time samples](#animationStitch)
    6. [Value Clips](#animationValueClips)

## TL;DR - Animation/Time Varying Data In-A-Nutshell <a name="summary"></a>
~~~admonish tip
- Terminology: A single time/value pair is called `time sample`, if an attribute doesn't have time samples, it has `default` value (Which just means it has a single static value).
- Time samples are encoded in a simple {\<time(frame)\>: \<value\>} dict.
- If a frame is requested where no time samples exist, it will be interpolated if the data type and non changing array lengths in neighbour time samples exist. Value queries before/after the first/last time sample will be clamped to these time samples.
- Time samples are encoded unitless/per frame and not in time units. This means they have to be shifted depending on the current frames per second.
- Only attributes can carry time sample data. (So composition arcs can not be time animated, only offset/scaled (see the LayerOffset section on this page)).

Reading and writing is quite straight forward:
```python
{{#include ../../../../code/core/elements.py:animationOverview}}
```
~~~

## What should I use it for? <a name="usage"></a>
~~~admonish tip
Anything that has time varying data will be written as time samples. Usually DCCs handle the time sample creation for you, but there are situations where we need to write them ourselves. For example if you want to efficiently combine time samples from two different value sources or if we want to turn a time sample into a `default` sampled value (a value without animation).
~~~

## Resources
- [Kind Glossary Definition](https://openusd.org/release/glossary.html#usdglossary-kind)
- [Extending Kinds](https://openusd.org/dev/api/kind_page_front.html#kind_extensions)
- [Kind Registry](https://openusd.org/dev/api/class_kind_registry.html) 

## Overview <a name="overview"></a>
~~~admonish important
 A single frame(time)/value pair is called `time sample`, if an attribute doesn't have time samples, it has `default` value (Which just means it has a single static value). The time value is the active frame where data is being exported on. It is not time/FPS based. This means that depending on `frames per second` set on the stage, different time samples are read. This means if you have a cache that was written in 25 FPS, you'll have to shift/scale the time samples if you want to use the cache in 24 FPS and you want to have the same result. More about this in the examples below.
~~~

~~~admonish danger
Currently USD has no concept of animation curves or multi time value interpolation other than `linear`. This means that in DCCs you'll have to grab the time data around your frame and have the DCCs re-interpolate the data. In Houdini this can be easily done via a `Retime` SOP node.
~~~

The possible stage interpolation types are:
- `Usd.InterpolationTypeLinear` (Interplate linearly (if array length doesn't change and data type allows it))
- `Usd.InterpolationTypeHeld` (Hold until the next time sample)

These can be set via `stage.SetInterpolationType(<Token>)`. Value queries before/after the first/last time sample will be clamped to these time samples.

Render delegates access the time samples within the shutter open close values when motion blur is enabled. When they request a value from Usd and a time sample is not found at the exact time/frame that is requested, it will be linearly interpolated if the array length doesn't change and the data type allows it.

~~~admonish danger
Since value lookups in USD can only have one value source, you cannot combine time samples from different layers at run time, instead you'll have to re-write the combined values across the whole frame range. This may seem unnecessary, but since USD is a cache based format and to keep USD performant, value source lookup is only done once and then querying the data is fast. This is the mechanism what makes USD able to expand and load large hierarchies with ease.
~~~


For example:

```python
# We usually want to write time samples in the shutter open/close range of the camera times the sample count of deform/xform motion blur.
double size.timeSamples = {
    1001: 2,
    1002: 2.274348497390747,
    1003: 3.0096023082733154,
    1004: 4.0740742683410645,
    1005: 5.336076736450195,
    1006: 6.663923263549805,
    1007: 7.9259257316589355,
    1008: 8.990397453308105,
    1009: 9.725651741027832,
    1010: 10,
}
# If we omit time samples, value requests for frames in between will get a linearly interpolated result.
double scale.timeSamples = {
    1001: 2,
    1005: 5.336076736450195,
    1010: 10,
}
```

~~~admonish warning
Since an attribute can only have a single value source, we can't have a `default` value from layer A and time samples from layer B. We can however have default and time samples values from the same value source.

For example:
```python
def Cube "Cube" (
)
{
    double size = 15
    double size.timeSamples = {
        1001: 1,
        1010: 10,
    }
}
```
If we now request the value without a frame, it will return `3`, if we request it with a time, then it will linearly interpolate or given the time sample if it exists on the frame.
```python
...
size_attr.Get() # Returns: 15.0
size_attr.Get(1008) # Returns: 8.0
...

```
Usually we'll only have one or the other, it is quite common to run into this at some point though. So when you query data, you should always use `.Get(\<frame\>)` as this also works when you don't have time samples. It will then just return the default value. Or you check for time samples, which in some cases can be quite expensive. We'll look at some more examples on this, especially with Houdini and causing node time dependencies in our [Houdini](../../dcc/houdini/hda/timedependency.md) section.
~~~

### Time Code <a name="animationTimeCode"></a>
The `Usd.TimeCode` class is a small wrapper class for handling time encoding. Currently it does nothing more that storing if it is a `default` time code or a `time/frame` time code with a specific frame. In the future it may get the concept of encoding in `time` instead of `frame`, so to future proof your code, you should always use this class instead of setting a time value directly.

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:animationTimeCode}}
```
~~~

### Layer Offsets <a name="animationLayerOffset"></a>
The `Sdf.LayerOffset` is used for encoding a time offset and scale for composition arcs. The offset and scale cannot be animated. 

Following composition arcs can use it:
- Sublayers
- Payloads
- References (Internal & file based)

The Python exposed LayerOffsets are always read-only copies, so you can't modify them in-place.
Instead you have to create new ones and re-write the arc/assign the new layer offset.

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:animationLayerOffset}}
```
~~~

If you are interested on how to author composition in the low level API, checkout our [composition](../composition/overview.md) section.

### Reading & Writing time samples <a name="animationReadWrite"></a>

#### Writing data

Here are the high and low level API to write data.
~~~admonish tip
When writing a large amount of samples, you should use the low level API as it is a lot faster.
~~~

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:animationWrite}}
```
~~~

If you are not sure if a schema attribute can have time samples, you can get the variability hint.
This is only a hint, it is up to you to not write time samples. In some parts of Usd things will fail or not work as exepcted if you write time samples for a non varying attribute.
~~~admonish info title=""
```python
attr.GetMetadata("variability") == Sdf.VariabilityVarying
attr.GetMetadata("variability") == Sdf.VariabilityUniform 
```
~~~

#### Reading data

To read data we recommend using the high level API. That way you can also request data from value clipped (per frame loaded Usd) files. The only case where reading directly in the low level API make sense is when you need to open a on disk layer and need to tweak the time samples. Check out our [FX Houdini](../../dcc/houdini/fx/pointinstancers.md) section for a practical example.

~~~admonish tip
If you need to check if an attribute is time sampled, run the following:
```python
{{#include ../../../../code/core/elements.py:animationTimeVarying}}
```
If you know the whole layer is in memory, then running GetNumTimeSamples()
is fine, as it doesn't have t open any files.
~~~

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:animationRead}}
```
~~~

#### Special Values
You can also tell a time sample to block a value. Blocking means that the attribute at that frame will act as if it doesn't have any value written ("Not authored" in USD speak) to scene/render delegates.

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:animationSpecialValues}}
```
~~~

### Frames Per Second <a name="animationMetadata"></a>

### Stitching/Combining time samples<a name="animationStitch"></a>

### Value Clips <a name="animationValueClips"></a>
