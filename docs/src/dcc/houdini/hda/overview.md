# Creating efficient LOPs HDAs
As with any other network in Houdini, we can also create HDAs in LOPs.

This page will focus on the most important performance related aspects of LOP HDAs, we will be referencing some of the points mentioned in the [performance optimizations](./performance/overview.md) section with a more practical view.

# Table of contents
1. [Overview](#overview)
1. [HDA Template Setup](#hdaTemplate)
    1. [Order of operations](#hdaOrderOfOperations)
    1. [Dealing with time dependencies](#hdaTimeDependencies)
    1. [Layer Size/Count](#hdaLayerSizeCount)
1. [Composition](#hdaComposition)

## Overview <a name="overview"></a>
When building LOP HDAs with USD, the big question is:

~~~admonish question
What should we do in Python and would should we do with HDAs/nodes that Houdini ships with?
~~~

The answer depends on your knowledge level of USD and the pipeline resources you have.

If you want to go the "expert" route, this is the minimal working set of nodes you'll be using:

![HDA Minimal Working Set Nodes](hdaMinimalNodeWorkingSet.jpg)

Technically we won't be needing more, because everything else can be done in Python. 
(There are also the standard control flow related nodes, we skipped those in the above image).
It is also faster to run operations in Python, because we can batch edits, where as with nodes, Houdini
has to evaluate the node tree.

So does this mean we shouldn't use the Houdini nodes at all? Definitely not! Houdini's LOPs tool set offers a lot of useful nodes, especially when your are prototyping, we definitely recommend using these first. A common workflow for developers is therefore:

~~~admonish tip title=""
Build everything with LOP HDAs first, then rebuild it, where possible, with Python LOPs when we notice performance hits.
~~~

We'll always use the "Material Library" and "SOP Import" nodes as these pull data from non LOP networks.

There are also a lot of UI related nodes, which are simply awesome. We won't be putting these in our HDAs, but they should be used by artists to complement our workflows.

![Houdini UI Custom Panel Nodes](houdiniUICustomPanelNodes.jpg)

## HDA Template Setup <a name="hdaTemplate"></a>
Let's take a look at how we can typically structure HDAs:

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="./hdaTemplateStructure.mp4" type="video/mp4" alt="Houdini Hda Template Structure">
</video>

For parms we can make use of Houdini's internal loputils under the following path:
~~~admonish tip title=""
$HFS/houdini/python3.9libs/loputils.py
~~~
It is not an official API module, so use it with care, it may be subject to change.

You can simply import via `import loputils`. It is a good point of reference for UI related functions, for example action buttons on parms use it at lot.

Here you can find the [loputils.py - Sphinx Docs](https://ikrima.github.io/houdini_additional_python_docs/loputils.html) online.

It gives us common lop related helpers, like selectors etc.

For the structure we recommend:
1. Create a new layer
2. Perform your edits (best-case only a single Python node) or merge in content from other inputs.
3. Create a new layer

Why should we spawn the new layers? See our [layer size and content](#hdaLayerSizeCount) section below for the answer.

When merging other layers via the merge node we recommend first flattening your input layers and then using the "Separate Layers" mode. That way we also avoid the layer size problem and keep our network fast.

### Order of Operations <a name="hdaOrderOfOperations"></a>
The same as within SOPs, we have to pay attention to how we build our node network to have it perform well.

Let's look at a wrong example and how to fix it:

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="./hdaOrderOfOperationSlow.mp4" type="video/mp4" alt="Houdini Order of Operations slow">
</video>

Here is a more optimized result:

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="./hdaOrderOfOperationOptimized.mp4" type="video/mp4" alt="Houdini Order of Operations fast">
</video>

The name of the game is isolating your time dependencies. Now the above is often different how a production setup might look, but the important part is that we try to isolate each individual component that can stand by itself to a separate node stream before combining it into the scene via a merge node.

In our HDAs we can often build a separate network and then merge it into the main node stream, that way not everything has to re-cook, only the merge, if there is an upstream time dependency. 

Now you may have noticed that in the first video we also merged a node stream  with itself.

If Ghostbusters taught us one thing:

~~~admonish danger title="Important | Merging node streams"
Don't cross the streams!*

*(unless you use a layer break).
~~~

The solution is simple, add a layer break (and make sure that your have the "Strip Layers Above Layer Breaks" toggle turned on). We have these "diamond" shaped networks quite a lot, so make sure you always layer break them correctly. For artists it can be convenient to build a HDA that does this for them.

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="./hdaOrderOfOperationsLayerBreak.mp4" type="video/mp4" alt="Houdini Merge Order">
</video>

~~~admonish danger title="Important | Merging a layer stack with itself"
USD is also very "forgiving", if we create content in a layer, that is already there from another layer (or layer stack via a reference or payload). The result is the same (due to composition), but the layer stack is "doubled". This is particularly risky and can lead to strange crashes, e.g. when we start to duplicate references on the same prim.

Now if we do this in the same layer stack, everything is fine as our [list-editable ops](../../../core/composition/fundamentals.md#compositionFundamentalsListEditableOps) are merged in the active layer stack. So you'll only have the reference being loaded once, even though it occurs twice in the same layer stack.

Now if we load a reference that is itself referenced, it is another story due to [encapsulation](../../../core/composition/fundamentals.md#compositionFundamentalsEncapsulation). We now have the layer twice, which gives us the same output visually/hierarchy wise, but our layers that are used by composition now has really doubled.

Check out this video for comparison:

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="./hdaOrderOfOperationsLayerStackDuplication.mp4" type="video/mp4" alt="Houdini Layer Stack Duplication">
</video>

~~~


What also is important, is the merge order. Now in SOPs we can just merge in any order, and our result is still the same (except the point order).

For LOPs this is different: The merge order is the sublayer order and therefore effects composition. As you can see in the video below, if we have an attribute that is the same in both layers (in this case the transform matrix), the order matters.

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="./hdaOrderOfOperationsMergeOrder.mp4" type="video/mp4" alt="Houdini Merge Order">
</video>

### Dealing with time dependencies <a name="hdaTimeDependencies"></a>
As with SOPs, we should also follow the design principle of keeping everything non-time dependent where possible.

When we have time dependencies, we should always isolate them, cache them and then merge them into our "main" node stream.

~~~admonish important title="Pro Tip | Writing Time Samples Via Python"
When writing Python code, we can write time samples for the full range too. See our [animation section](../../../core/elements/animation.md) for more info. We recommend using the lower level API, as it is a lot faster when writing a large time sample count. A typical example would be to write the per image output file or texture sequences via Python, as this is highly performant.
~~~

The very cool thing with USD is that anything that comes from a cached file does not cause a Houdini time dependency, because the time samples are stored in the file/layer itself. This is very different to how SOPs works and can be confusing in the beginning.

Essentially the goal with LOPs is to have no time dependency (at least when not loading live caches).

Starting with H19.5 most LOP nodes can also whole frame range cache their edits. This does mean that a node can cook longer for very long frame ranges, but overall your network will not have a time dependency, which means when writing your node network to disk (for example for rendering), we only have to write a single frame and still have all the animation data. How cool is that! 

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="./hdaTimeDependencyPerNode.mp4" type="video/mp4" alt="Houdini Time Sample Per Node">
</video>

If a node doesn't have that option, we can almost always isolate that part of the network and pre cache it, that way we have the same effect but for a group of nodes.

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="./hdaTimeDependencyCache.mp4" type="video/mp4" alt="Houdini Time Sample Per Node">
</video>

~~~admonish danger title="Important | Previewing Xform/Deformation Motionblur"
If we want to preview xform/deformation motionblur that is not based on the `velocities`/`accelerations` attribute, then we have to pre-cache the time samples in interactive sessions. This is as simple as adding a LOPs cache node as shown above.
~~~

Also check out our [Tips & Tricks section](../faq/overview.md#timeSampleValueMightBeTimeVarying) to see how we can query if an attribute is time sampled or only has a default value. This is a bit different in Houdini than bare-bone USD, because we often only have a single time sample for in session generated data.

### Layer Size/Count <a name="hdaLayerSizeCount"></a>
As mentioned in the [overview](#overview), layer content size can become an issue.

We therefore recommend starting of with a new layer and ending with a new layer. That way our HDA starts of fast, can create any amount of data and not affect downstream nodes.

For a full explanation see our [performance section](../performance/overview.md).

## Composition <a name="hdaComposition"></a>
We strongly recommend reading up on our [composition section](../../../core/composition/overview.md) before getting started in LOPs.

When setting up composition arcs in Houdini, we can either do it via nodes or code. We recommend first doing everything via nodes and then refactoring it to be code based, as it is faster. Our custom HDAs are usually the ones that bring in data, as this is the core task of every pipeline.

In our [Tips & Tricks section](../faq/overview.md), we have provided these common examples:
- [Extracting payloads and references from an existing layer stack with anonymous layers](../faq/overview.md#compositionReferencePayloadLayerStack)
- [Efficiently re-writing existing hierarchies as variants](../faq/overview.md#compositionArcVariantReauthor)
- [Adding overrides via inherits](../faq/overview.md#compositionArcInherit)

These provide entry points of how you can post-process data do you needs, after you have SOP imported it.