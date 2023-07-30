# Particles
Importing particles (points) is the simplest form of geometry import.

Let's see how we can make it complicated 🤪. We'll take a look at these two cases:
- Houdini native point import
- Render overrides via (Numpy) Python wrangles

You can find all the .hip files of our shown examples in our [USD Survival Guide - GitHub Repo](https://github.com/LucaScheller/VFX-UsdSurvivalGuide/tree/main/files/dcc/houdini).

## Houdini Native Import
When importing points, all you need to set is a path attribute on your points (rather than on prims as with polygon meshes), because we don't have any prims on sop level. (Thanks captain obvious).

For an exercise, let's build a simple SOP import ourselves. Should we use this in production: No, Houdini's geo conversion is a lot faster, when it comes to segmenting your input based on the path attribute. Nonetheless it is a fun little demo:

~~~admonish tip title=""
```python
{{#include ../../../../../code/dcc/houdini.py:houdiniPointsNativeStream}}
```
~~~

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="./media/pointsNativeStream.mp4" type="video/mp4" alt="Houdini Python Wrangle">
</video>

Why should we do it ourselves, you might ask? Because there are instances, where we can directly load in the array, because we know we are only editing a single prim. Some of Houdini's nodes actually use this mechanism in a few of the point instancer related nodes.

## Render-Time Overrvides via (Numpy) Python Wrangles
Now you might be thinking, is Python performant enough to actually manipulate geometry?

In the context of points (also point instancers), we answer is yes. As we do not have to do geometry operations, manipulating points is "just" editing arrays. This can be done very efficiently via numpy, if we use it for final tweaking. So don't expect to have the power of vex, the below is a "cheap" solution to adding render time overrides, when you don't have the resources to write your own compiled language (looking at your [DNEG (OpenVDB AX)](https://www.openvdb.org/documentation/doxygen/openvdbax.html)).

To showcase how we manipulate arrays at render time, we've built a "Python Wrangle" .hda. Here is the basic .hda structure:

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="./media/pointsPythonWrangleOverview.mp4" type="video/mp4" alt="Houdini Python Wrangle">
</video>

As discussed in our [Creating efficient LOPs .Hdas](../hda/overview.md) section, we start and end the Hda with a new layer to ensure that we don't "suffer" from the problem of our layer getting to data heavy. Then we have two python nodes: The first one serializes the Hda parms to a json dict and stores it on our point prims, the second one modifies the attributes based on the parm settings. Why do we need to separate the data storage and execution? Because we want to only opt-in into the python code execution at render-time. So that's why we put down a switch node that is driven via a context variable. Context variables are similar to global Houdini variables, the main difference is they are scoped to a section of our node graph or are only set when we trigger a render.

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="./media/pointsPythonWrangleHusk.mp4" type="video/mp4" alt="Houdini Python Wrangle Husk">
</video>

This means that when rendering the USD file to disk, all the points will store is our wrangle code (and the original point data, in production this usually comes from another already cached USD file that was payloaded in). In our pre render scripts, we can then iterate over our stage and execute our code.

Let's talk about performance: The more attributes we manipulate, the slower it will get. To stress test this, let's try building a point replicator with a constant seed. To "upres" from 1 million to 10 million points, it takes around 30 seconds. For this being a "cheap" solution to implement, I'd say that is manageable for interactivity. Now we could also do a similar thing by just using a point instancer prim and upres-ing our prototypes, using this method allows for per point overrides though, which gives us more detail.

Here is a demo of a point replicator:

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="./media/pointsPythonWranglePointReplicate.mp4" type="video/mp4" alt="Houdini Python Wrangle Husk">
</video>

Another cool thing is, that this is actually not limited to points prims (We lied in our intro 😱). Since all attributes are is arrays of data, we can run the python wrangle on any prim. For example if we just wan't to increase our pscale width or multiply our velocities, operating on an array via numpy is incredibly fast, we're talking a few 100 milliseconds at most for a few millions points. As mentioned in our [data types](../../../core/elements/data_type.md) section, USD implements the buffer protocol, so we don't actually duplicate any memory until really needed and mapping `Vt.Array`s to numpy is as straight forward as casting the array to a numpy array.


Now the below code might look long, but the import bits are:
- Getting the data: `np.array(attr.Get(frame)`
- Setting the data: `attr.Set(attr.GetTypeName().type.pythonClass.FromNumpy(output_data[binding.property_name]), frame))`
- Updating the extent hint: `UsdGeom.Boundable.ComputeExtentFromPlugins(boundable_api, frame)`

~~~admonish tip title="Python Wrangle Hda | Summary |  Click to expand!" collapsible=true
```python
    ...
    # Read data
    input_data[binding.property_name] = np.array(attr.Get(frame))
    ...
    # Write data
    for binding in bindings:
        attr = prim.GetAttribute(binding.property_name)
        if len(output_data[binding.property_name]) != output_point_count:
            attr.Set(pxr.Sdf.ValueBlock())
            continue
        attr_class = attr.GetTypeName().type.pythonClass
        attr.Set(attr_class.FromNumpy(output_data[binding.property_name]), frame)
    ...
    # Re-Compute extent hints
    boundable_api = pxr.UsdGeom.Boundable(prim)
    extent_attr = boundable_api.GetExtentAttr()
    extent_value = pxr.UsdGeom.Boundable.ComputeExtentFromPlugins(boundable_api, frame)
    if extent_value:
        extent_attr.Set(extent_value, frame)
```
~~~


The code for our "python kernel" executor:

~~~admonish tip title="Python Wrangle Hda | Python Kernel | Click to expand!" collapsible=true
```python
{{#include ../../../../../files/dcc/houdini/points/pythonWrangle.py}}
```
~~~

The code for our pre render script:

~~~admonish tip title="Python Wrangle Hda | Pre-Render Script | Click to expand!" collapsible=true
```python
{{#include ../../../../../files/dcc/houdini/points/renderPreFrame.py}}
```
~~~