# Point Instancers ('Copy To Points')
We have four options for mapping Houdini's packed prims to USD:
- As transforms
- As point instancers
- As deformed geo (baking down the xform to actual geo data)
- As skeletons, more info in our [RBD section](./rbd.md)

~~~admonish tip title="Pro Tip | When to use PointInstancer prims?"
We'll always want to use USD's PointInstancer prims, when representing a "replicate a few unique meshes to many points" scenario.
In SOPs we usually do this via the "Copy To Points" node.
~~~

You can find all the .hip files of our shown examples in our [USD Survival Guide - GitHub Repo](https://github.com/LucaScheller/VFX-UsdSurvivalGuide/tree/main/files/dcc/houdini).

For all options for SOP to LOP importing, check out the official [Houdini docs](https://www.sidefx.com/docs/houdini/solaris/sop_import.html).

In the below examples, we use the `path`/`name` attributes to define the prim path. You can actually configure yourself what attributes Houdini should use for defining our prim paths on the "SOP import node" LOP/"USD Configure" SOP node.

## Houdini Native Import (and making it convenient for artists)
To import our geometry to "PointInstancer" USD prims, we have to have it as packed prims in SOPs. If you have nested packed levels, they will be imported as nested point instancers. We do not recommend doing this, as it can cause some confusing outputs. The best practice is to always have a "flat" packed hierarchy, so only one level of packed prims.

Houdini gives us the following options for importing:
- The `usdinstancerpath` attribute defines the location of our `PointInstancer` prim.
- The `path`/`name` attribute defines the location of the prototype prims. Prototypes are the unique prims that should get instances, they are similar to the left input on your "copy to points" node. 

An important thing to note is, that if your `path`/`name` attribute does not have any `/` slashes or starts with `./`, the prototypes will be imported with the following path: `<usdinstancerpath>/Prototypes/<pathOrName>`. Having the `/Prototypes` prim is just a USD naming convention thing.

To make it easy to use for artists, we recommend mapping the traditional path attribute value to `usdinstancerpath` and making sure that the `name` attribute is relative. 

Another important thing to know about packed prims is, that the `path`/`name` attributes are also used to define the hierarchy within the packed prim content. So before you pack your geometry, it has to have a valid path value.

Good, now that we know the basics, let's have a look at a not so expectable behavior:
If you remember, in our [Basic Building Blocks of Usd](../../../core/elements/overview.md) section, we explained that relationships can't be animated. Here's the fun part:

~~~admonish danger title="PointInstancer | Varying Prototypes | Problem"
The mapping of what point maps to what prototype prim is stored via the `protoIndices` attribute. This maps an index to the prim paths targetd by the `prototypes` relationship. Since relationships can't be animated, the `protoIndices`/`prototypes` properties has to be aware of all prototypes, that ever get instanced across the whole cache.
~~~

This is the reason, why in our LOPs instancer node, we have to predefine all prototypes. The problem is in SOPs, it kind of goes against the usual artist workflow. For example when we have debris instances, we don't want to have the artist managing to always have at least one copy of all unique prims we are trying to instance.


~~~admonish tip title="PointInstancer | Varying Prototypes | Solution"
The artist should only have to ensure a unique `name` attribute value per unique instance and a valid `usdinstancerpath` value.
Making sure the protoIndices don't jump, as prototypes come in and out of existence, is something we can fix on the pipeline side.
~~~

Luckily, we can fix this behavior, by tracking the prototypes ourselves per frame and then re-ordering them as a post process of writing our caches.

Let's take a look at the full implementation:

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="../../../../media/dcc/houdini/fx/pointInstancerPrototypeReorder.mp4" type="video/mp4" alt="Houdini Prototype Re-Order">
</video>

As you can see, all looks good, when we only look at the active frame, because the active frame does not know about the other frames. As soon as we cache it to disk though, it "breaks", because the protoIndices map to the wrong prototype.

All we have to do is create an attribute, that per frame stores the relation ship targets as a string list. After the cache is done, we have to map the wrong prototype index to the write one.

Here is the tracker script:

~~~admonish tip title="PointInstancer | Re-Order Prototypes | Track Prototypes | Click to expand" collapsible=true
```python
{{#include ../../../../../code/dcc/houdini.py:houdiniPointInstancerReorderTracker}}
```
~~~

And here the post processing script. You'll usually want to trigger this after the whole cache is done writing. It also works with value clips, you pass in all the individual clip files into the layers list. This is also another really cool demo, of how numpy can be used to get C++ like performance.

~~~admonish tip title="PointInstancer | Re-Order Prototypes | Track Prototypes | Click to expand" collapsible=true
```python
{{#include ../../../../../code/dcc/houdini.py:houdiniPointInstancerReorderPostProcess}}
```
~~~

Phew, now everything looks alright again!

## Performance Optimizations
You may have noticed, that we always have to create packed prims on SOP level, to import them as PointInstancer prims. If we really want to go all out on the most high performance import, we can actually replicate a "Copy To Points" import. That way we only have to pass in the prototypes and the points, but don't have the overhead of spawning the packed prims in SOPs.

Is this something you need to be doing? No, Houdini's LOPs import as well as the packed prim generation are highly performant, the following solution is really only necessary, if you are really picky about making your export a few hundred milliseconds faster with very large instance counts.

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="../../../../media/dcc/houdini/fx/pointInstancerPerformance.mp4" type="video/mp4" alt="Houdini Prototype Re-Order">
</video>

As you can see we are at a factor 20 (1 seconds : 50 milliseconds). Wow! Now what we don't show is, that we actually have to conform the point instances attributes to what the PointInstancer prim schema expects. So the ratio we just mentioned is the best case scenario, but it can be a bit slower, when we have to map for example `N`/`up` to `orientations`. This is also only this performant because we are importing a single PointInstancer prim, which means we don't have to segment any of the protoIndices.

We also loose the benefit of being able to work with our packed prims in SOP level, for example for collision detection etc.

Let's look at the details:

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="../../../../media/dcc/houdini/fx/pointInstancerPerformanceDetails.mp4" type="video/mp4" alt="Houdini Prototype Re-Order">
</video>

On SOP level:
- We create a "protoIndices" attribute based on all unique values of the "name" attribute
- We create a "protoHash" attribute in the case we have multiple PointInstancer prim paths, so that we can match the prototypes per instancer
- We conform all instancing related attributes to have the correct precision. This is very important, as USD does not allow other precisions types than what is defined in the PointInstancer schema.
- We conform the different instancing attributes Houdini has to the attributes the PointInstancer schema expects. (Actually the setup in the video doesn't do this, but you have to/should, in case you want to use this in production)

On LOP level:
- We import the points as a "Points" prim, so now we have to convert it to a "PointInstancer" prim. For the prim itself, this just means changing the prim type to "PointInstancer" and renaming "points" to "positions".
- We create the "prototypes" relationship property.

~~~admonish tip title="PointInstancer | Custom Import | Click to expand" collapsible=true
```python
{{#include ../../../../../code/dcc/houdini.py:houdiniPointInstancerNativeStream}}
```
~~~