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
    2. [Layer Offset (A Non-Animateable Time Offset/Scale for Composition Arcs)](#animationLayerOffset)
    3. [Reading & Writing default values, time samples and value blocks](#animationReadWrite)
    4. [Time Metrics (Frames Per Second & Frame Range)](#animationMetadata)
    5. [Stitching/Combining time samples](#animationStitch)
    6. [Value Clips (Loading time samples from multiple files)](#animationValueClips)

## TL;DR - Animation/Time Varying Data In-A-Nutshell <a name="summary"></a>
~~~admonish tip
- Terminology: A single time/value pair is called `time sample`, if an attribute doesn't have time samples, it has `default` value (Which just means it has a single static value).
- Time samples are encoded in a simple {\<time(frame)\>: \<value\>} dict.
- If a frame is requested where no time samples exist, it will be interpolated if the data type allows it and non changing array lengths in neighbour time samples exist. Value queries before/after the first/last time sample will be clamped to these time samples, if you want a cache in a different FPS format to match a certain frame range.
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
- [USD Time Sample Examples](https://openusd.org/release/tut_xforms.html)
- [USD Value Clips](https://openusd.org/dev/api/_usd__page__value_clips.html)
- [USD Value Clips Utils](https://openusd.org/dev/api/stitch_clips_8h.html#details) 

## Overview <a name="overview"></a>
~~~admonish important
 A single frame(time)/value pair is called `time sample`, if an attribute doesn't have time samples, it has `default` value (Which just means it has a single static value). The time value is the active frame where data is being exported on. It is not time/FPS based. This means that depending on `frames per second` set on the stage, different time samples are read. This means if you have a cache that was written in 25 FPS, you'll have to shift/scale the time samples if you want to use the cache in 24 FPS and you want to have the same result. More about this in the examples below.
~~~

~~~admonish danger
Currently USD has no concept of animation curves or multi time value interpolation other than `linear`. This means that in DCCs you'll have to grab the time data around your frame and have the DCCs re-interpolate the data. In Houdini this can be easily done via a `Retime` SOP node.
~~~

The possible stage interpolation types are:
- `Usd.InterpolationTypeLinear` (Interpolate linearly (if array length doesn't change and data type allows it))
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
If we now request the value without a frame, it will return `15`, if we request it with a time, then it will linearly interpolate or given the time sample if it exists on the frame.
```python
...
size_attr.Get() # Returns: 15.0
size_attr.Get(1008) # Returns: 8.0
...

```
Usually we'll only have one or the other, it is quite common to run into this at some point though. So when you query data, you should always use `.Get(<frame>)` as this also works when you don't have time samples. It will then just return the default value. Or you check for time samples, which in some cases can be quite expensive. We'll look at some more examples on this, especially with Houdini and causing node time dependencies in our [Houdini](../../dcc/houdini/hda/timedependency.md) section.
~~~

### Time Code <a name="animationTimeCode"></a>
The `Usd.TimeCode` class is a small wrapper class for handling time encoding. Currently it does nothing more that storing if it is a `default` time code or a `time/frame` time code with a specific frame. In the future it may get the concept of encoding in `time` instead of `frame`, so to future proof your code, you should always use this class instead of setting a time value directly.

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:animationTimeCode}}
```
~~~

### Layer Offset (A Non-Animateable Time Offset/Scale for Composition Arcs) <a name="animationLayerOffset"></a>
The `Sdf.LayerOffset` is used for encoding a time offset and scale for composition arcs. 

~~~admonish warning
The offset and scale cannot be animated.
~~~

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

### Reading & Writing default values, time samples and value blocks <a name="animationReadWrite"></a>

#### Writing data

Here are the high and low level APIs to write data.
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
You can also tell a time sample to block a value. Blocking means that the attribute at that frame will act as if it doesn't have any value written ("Not authored" in USD speak) to stage queries and render delegates.

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:animationSpecialValues}}
```
~~~

### Time Metrics (Frames Per Second & Frame Range) <a name="animationMetadata"></a>
With what FPS the samples are interpreted is defined by the `timeCodesPerSecond`/`framesPerSecond` metadata.

The [loading order of FPS](https://openusd.org/dev/api/class_usd_stage.html#a85092d7455ae894d50224e761dc6e840) is:
1. timeCodesPerSecond from session layer
2. timeCodesPerSecond from root layer
3. framesPerSecond from session layer
4. framesPerSecond from root layer
5. fallback value of 24

When writing layers, we should always write these layer metrics, so that we know what
the original intended FPS were. 

~~~admonish warning
If we want to load a let's say 24 FPS cache in a 25 FPS setup, we will have to apply a `Sdf.LayerOffset` when loading in the layer. This way we can move back the sample to the "correct" frame based times by scaling with a factor of 24/25.
~~~

```python
(
    timeCodesPerSecond = 24
    framesPerSecond = 24
    metersPerUnit = 1
    startTimeCode = 1001
    endTimeCode = 1010
)
```

The `startTimeCode` and `endTimeCode` entries give intent hints on what the (useful) frame range of the USD file is. Applications can use this to automatically set the frame range of the stage when opening a USD file or use it as the scaling pivot when calculating time offsets or creating loop-able caches via value clips.

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:animationFPS}}
```
~~~

### Stitching/Combining time samples<a name="animationStitch"></a>
When working with Usd in DCCs, we often have a large amount of data that needs to be exported per frame. To speed this up, a common practice is to have a render farm, where multiple machines render out different frame ranges of scene. The result then needs to be combined into a single file or loaded via value clips for heavy data (as described in the next section below).

~~~admonish tip
Stitching multiple files to a single file is usually used for small per frame USD files. If you have large (1 GB > ) files per frame, then we recommend using values clips. During stitching all data has to be loaded into memory, so your RAM specs have to be high enough to handle all the files combined.
~~~

A typical production use case we use it for, is rendering out the render USD files per frame and then stitching these, as these are usually a few mb per frame at most.

~~~admonish warning
When working with collections, make sure that they are not to big, by selecting parent prims where possible. Currently USD stitches target path lists a bit inefficiently, which will result in your stitching either not going through at all or taking forever. See our [collections](../composition/relationships.md) section for more details.
~~~

USD ships with a standalone `usdstitch` commandline tool, which is a small Python wrapper around the `UsdUtils.StitchLayers()` function. You can read more it in our [standalone tools](./standalone_utilities.md) section.

In Houdini you can find it in the `$HFS/bin`folder, e.g. `/opt/hfs19.5/bin`.

Here is an excerpt:
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:animationStitchCmdlineTool}}
```
~~~

More about layer stitching/flattening/copying in our [layer](./layer.md) section.

### Value Clips (Loading time samples from multiple files)<a name="animationValueClips"></a>
~~~admonish note
We only cover value clips in a rough overview here, we might extend this a bit more in the future, if there is interest. We recommend checking out the [official docs page](https://openusd.org/dev/api/_usd__page__value_clips.html) as it is well written and worth the read!
~~~

USD [value clips](https://openusd.org/dev/api/_usd__page__value_clips.html) are USD's mechanism of loading in data per frame from different files. It has a special rule set, that we'll go over now below.

~~~admonish important
Composition wise, value clips (or the layer that specifies the value clip metadata) is right under the `local` arc strength and over `inherit` arcs.
~~~

Here are some examples from USD's official docs:

```python
def "Prim" (
    clips = {
        dictionary clip_set_1 = {
            double2[] active = [(101, 0), (102, 1), (103, 2)] 
            asset[] assetPaths = [@./clip1.usda@, @./clip2.usda@, @./clip3.usda@]
            asset manifestAssetPath = @./clipset1.manifest.usda@
            string primPath = "/ClipSet1"
            double2[] times = [(101, 101), (102, 102), (103, 103)]
        }
    }
    clipSets = ["clip_set_1"]
)
{
}
```

There is also the possibility to encode the value clip metadata via a file wild card syntax (The metadata keys start with `template`). We recommend sticking to the the above format as it is more flexible and more explicit.

~~~admonish info title="Click here to expand contents" collapsible=true
```python
def "Prim" (
    clips = {
        dictionary clip_set_2 = {
            string templateAssetPath = "clipset2.#.usd"
            double templateStartTime = 101
            double templateEndTime = 103
            double templateStride = 1
            asset manifestAssetPath = @./clipset2.manifest.usda@
            string primPath = "/ClipSet2"
        }
    }
    clipSets = ["clip_set_2"]
)
{
}
```
~~~

As you can see it is pretty straight forward to implement clips with a few key metadata entries:
- `primPath`: Will substitute the current prim path with this path, when looking in the clipped files. This is similar to how you can specify a path when creating references (when not using the `defaultPrim` metadata set in the layer metadata).
- `manifestAssetPath`: A asset path to a file containing a hierarchy of attributes that have time samples without any default or time sample data.
- `assetPaths`: A list of asset paths that should be used for the clip.
- `active`: A list of (\<stage time\>, \<asset path list index\>) pairs, that specify on what frame what clip is active.
- `times`: A list of (\<stage time\>, \<asset path time\>) pairs, that map how the current time should be mapped into the time that should be looked up in the active asset path file.
- `interpolateMissingClipValues` (Optional): Boolean that activates interpolation of time samples from surrounding clip files, should the active file not have any data on the currently requested time.

~~~admonish warning
The content of individual clip files must be the raw data, in other words anything that is loaded in via composition arcs is ignored.
~~~

The other files that are needed to make clips work are:
- The `manifest` file: A file containing a hierarchy of attributes that have time samples  without any default or time sample data.
- The `topology` file: A file containing all the attributes that only have static `default` data.

Here is how you can generate them:
USD ships with a `usdstitchclips` commandline tool that auto-converts multiple clip (per frame) files to a value clipped main file for you. This works great if you only have a single root prim you want to load clipped data on. 

Unfortunately this is often not the case in production, so this is where the value clip API comes into play. The `usdstitchclips` tool is a small Python wrapper around that API, so you can also check out the Python code there.

Here are the basics, the main modules we will be using are `pxr.Usd.ClipsAPI` and `pxr.UsdUtils`:

~~~admonish tip
Technically you can remove all default attributes from the per frame files after running the topology layer generation. This can save a lot of disk space,but you can't partially re-render specific frames of the cache though. So only do this if you know the cache is "done".
~~~

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:animationStitchClipsUtils}}
```
~~~

Since in production (see the next section), we usually want to put the metadata at the asset roots, we'll usually only want to run 
- `UsdUtils.StitchClipsTopology(topology_layer, time_sample_files)`
- `UsdUtils.StitchClipsManifest(manifest_layer, topology_layer, time_sample_files, clip_prim_path)`

And then create the clip metadata in the cache_layer ourselves:
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:animationStitchClipsAPI}}
```
~~~


#### How will I use it in production?
Value clips are the go-to mechanism when loading heavy data, especially for animation and fx. They are also the only USD mechanism for looping data.

As discussed in more detail in our [composition](../composition/overview.md) section, caches are usually attached to asset root prim. As you can see above, the metadata must always specify a single root prim to load the clip on, this is usually your asset root prim. You could also load it on a prim higher up in the hierarchy, this makes your scene incredibly hard to debug though and is not recommended.

This means that if you are writing an fx cache with a hierarchy that has multiple asset roots, you'll be attaching the metadata to each individual asset root. This way you can have a single value clipped cache, that is loaded in multiple parts of you scene. You can then payload/reference in this main file, with the value clip metadata per asset root prim, per asset root prim, which allows you to partially load/unload your hierarchy as usual.

Your file structure will look as follows:
- Per frame(s) files with time sample data:
    - /cache/value_clips/time_sample.1001.usd
    - /cache/value_clips/time_sample.1002.usd
    - /cache/value_clips/time_sample.1003.usd
- Manifest file (A lightweight Usd file with attributes without values that specifies that these are attributes are with animation in clip files):    
    - /cache/value_clips/manifest.usd 
- Topology file (A USD file that has all attributes with default values):    
    - /cache/value_clips/topology.usd
- Value clipped file (It sublayers the topology.usd file and writes the value clip metadata (per asset root prim)):
    - /cache/cache.usd

Typically your shot or asset layer USD files will then payload or reference in the individual asset root prims from the cache.usd file.

~~~admonish important
Since we attach the value clips to asset root prims, our value clipped caches can't have values above asset root prims.
~~~

If this all sounds a bit confusing don't worry about it for now, we have a hands-on example in our 
[composition](../composition/overview.md) section.

~~~admonish tip title="Value Clips and Instanceable Prims"
For more info on how value clips affect instancing, check out our [composition](../composition/overview.md) section. There you will also find an example with multiple asset roots re-using the same value clipped cache.
~~~


#### How does it affect attribute time samples and queries?
When working with time samples in value clips there are two important things to keep in mind:

##### Subframes
The `active` and `times` metadata entries need to have sub-frames encoded. Let's look at our example:

Three per frame files, with each file having samples around the centered frame:
- /cache/value_clips/time_sample.1001.usd": (1000.75, 1001, 1001.25)
- /cache/value_clips/time_sample.1002.usd": (1001.75, 1002, 1002.25)
- /cache/value_clips/time_sample.1003.usd": (1002.75, 1003, 1003.25)

They must be written as follows in order for subframe time sample to be read.
```python
double2[] active = [(1000.5, 0), (1001.75, 1), (1002.75, 2)] 
double2[] times = [(1000.5, 1000.5), (1001.75, 1001.75), (1002.75, 1003)]
```
As you may have noticed, we don't need to specify the centred or .25 frame, these will be interpolated linearly to the next entry in the list.

##### Queries
When we call attribute.GetTimeSamples(), we will get the interval that is specified with the `times` metadata.
For the example above this would return:
```python
(1000.75, 1001, 1001.25, 1001.75, 1002, 1002.25, 1002.75, 1003, 1003.25)
```

If we would only write the metadata on the main frames:
```python
double2[] active = [(1001, 0), (1002, 1), (1003, 2)] 
double2[] times = [(1001, 1001), (1002, 1002), (1003, 1003)]
```
It will return:
```python
(1001, 1001.25, 1002, 1002.25, 1003, 1003.25)
```
~~~admonish important
With value clips it can be very expensive to call `attribute.GetTimesamples()` as this will open all layers to get the samples in the interval that is specified in the metadata. It does not only read the value clip metadata. If possible use `attribute.GetTimeSamplesInInterval()` as this only opens the layers in the interested interval range.
~~~

