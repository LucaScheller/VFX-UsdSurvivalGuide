# Prim Cache Population (PCP) - Composition Cache
~~~admonish question title="Still under construction!"
This section is still under development, it is subject to change and needs extra validation.
~~~

The **Prim Cache Population** module is the backend of what makes USD composition work. You could call it the `composition core`, that builds the prim index.
The prim index is like an ordered list per prim, that defines where values can be loaded from. For example when we call `Usd.Prim.GetPrimStack`, the `pcp` gives us a list of value sources as an ordered list, with the "winning" value source as the first entry.

When USD opens a stage, it builds the prim index, so that it knows for each prim/property where to pull data from.
This is then cached, and super fast to access.

When clients (like hydra delegates or C++/Python attribute queries) request data, only then the data is loaded.
This way hierarchies can load blazingly fast, without actually loading the heavy attribute data.

~~~admonish tip
To summarize: Composition (the process of calculating the value sources) is cached, value resolution is not, to allow random access data loading.
~~~

For a detailed explanation, checkout the [Value Resolution](https://openusd.org/release/glossary.html#usdglossary-valueresolution) docs page.

# Table of contents
1. [Prim Cache Population (PCP) In-A-Nutshell](#summary)
1. [What should I use it for?](#usage)
1. [Resources](#resources)
1. [Overview](#overview)
1. [Inspecting Composition](#pcpInspect)
    1. [Prim/Property Stack](#pcpPrimPropertyStack)
    1. [Prim Index](#pcpPrimPropertyIndex)
    1. [Prim Composition Query](#pcpPrimCompositionQuery)

## TL;DR - <Topic> In-A-Nutshell <a name="summary"></a>
- The **Prim Cache Population** module in USD computes and caches the composition (how different layers are combined) by building an index of value sources per prim called **prim index**.
- This process of calculating the value sources is cached, value resolution is not, to allow random access to data. This makes accessing hierarchies super fast, and allows attribute data to be streamed in only when needed. This is also possible due to USD's [binary crate format](https://openusd.org/release/glossary.html#crate-file-format), which allows sparse "read only what you need" access from USD files.
- The **Prim Cache Population (Pcp)** module is exposed via two ways:
    - **High Level API**: Via the `Usd.PrimCompositionQuery` class.
    - **Low Level API**: Via the`Usd.Prim.GetPrimIndex`/`Usd.Prim.ComputeExpandedPrimIndex` methods.
- Notice how both ways are still accessed via the high level API, as the low level `Sdf` API is not aware of composition.

## What should I use it for? <a name="usage"></a>
~~~admonish tip
We'll be using the prim cache population module for inspecting composition.
This is more of a deep dive topic, but you may at some point run into this in production.

An example scenario might be, that when we want to author a new composition arc, we first need to check if there are existing strong arcs, than the arc we intend on authoring.
For example if a composition query detects a variant, we must also author at least a variant or a higher composition arc in order for our edits to come through.
~~~

## Resources <a name="resources"></a>
- [PrimCache Population (Composition)](https://openusd.org/dev/api/pcp_page_front.html)
- [Prim Index](https://openusd.org/release/glossary.html#usdglossary-index)
- [Pcp.PrimIndex](https://openusd.org/release/api/class_pcp_prim_index.html)
- [Pcp.Cache](https://openusd.org/dev/api/class_pcp_cache.html)
- [Usd.CompositionArc](https://openusd.org/dev/api/class_usd_prim_composition_query_arc.html)
- [Usd.CompositionArcQuery](https://openusd.org/dev/api/class_usd_prim_composition_query.html)
- [Value Resolution](https://openusd.org/release/glossary.html#usdglossary-valueresolution)
- [USD binary crate file format](https://openusd.org/release/glossary.html#crate-file-format)

## Overview <a name="overview"></a>
This page currently focuses on the practical usage of the `Pcp` module, it doesn't aim to explain how the composition engine works under the hood. (As the author(s) of this guide also don't know the details 😉, if you know more in-depth knowledge, please feel free to share!)

There is a really cool plugin for the [UsdView](../elements/standalone_utilities.md) by [chrizzftd](https://github.com/chrizzFTD) called [The Grill](https://grill.readthedocs.io/en/latest/views.html), that renders out the dot graph representation interactively based on the selected prim.

In the examples below, we'll look at how to do this ourselves via Python.

## Inspecting Composition <a name="pcpInspect"></a>
To query data about composition, we have to go through the high level Usd API first, as the `Sdf` low level API is not aware of composition related data.
The high level Usd API then queries into the low level Pcp (Prim cache population) API, which tracks all composition related data and builds a value source index called **prim index**. 

The prim stack in simple terms: A stack of layers per prim (and therefore also properties) that knows about all the value sources (layers) a value can come from. Once a value is requested, the highest layer in the stack wins and returns the value for attributes. For metadata and relationships the value resolution can consult multiple layers, depending on how it was authored (see [list editable ops](../composition/listeditableops.md) as an example for a multiple layer averaged value).

### Prim/Property Stack <a name="pcpPrimPropertyStack"></a>
Let's first have a look at the prim and property stacks with a simple stage with a cubes that has written values in two different layers.
These return us all value sources for a prim or attribute.

~~~admonish tip title=""
```python
{{#include ../../../../code/core/composition.py:pcpPrimPropertyStack}}
```
~~~

In Houdini/USD view we can also view these stacks in the UI.

![Houdini Prim/Property Stack](houdiniPrimPropertyStack.gif)

### Prim Index <a name="pcpPrimIndex"></a>
Next let's look at the prim index.

~~~admonish tip title=""
```python
{{#include ../../../../code/core/composition.py:pcpPrimIndex}}
```
~~~

The prim index class can dump our prim index graph to the *dot* file format. The *dot* commandline tool ships with the most operating systems, we can then use it to visualize our graph as a .svg/.png file.

~~~admonish tip title="Result of: `print(prim_index.DumpToString())` | Click to view content" collapsible=true
```txt
Node 0:
    Parent node:              NONE
    Type:                     root
    DependencyType:           root
    Source path:              </bicycle>
    Source layer stack:       @anon:0x7f9eae9f2400:tmp.usda@,@anon:0x7f9eae9f1000:tmp-session.usda@
    Target path:              <NONE>
    Target layer stack:       NONE
    Map to parent:
        / -> /
    Map to root:
        / -> /
    Namespace depth:          0
    Depth below introduction: 0
    Permission:               Public
    Is restricted:            FALSE
    Is inert:                 FALSE
    Contribute specs:         TRUE
    Has specs:                TRUE
    Has symmetry:             FALSE
    Prim stack:
      </bicycle> anon:0x7f9eae9f2400:tmp.usda - @anon:0x7f9eae9f2400:tmp.usda@
Node 1:
    Parent node:              0
    Type:                     reference
    DependencyType:           non-virtual, purely-direct
    Source path:              </bicycle>
    Source layer stack:       @anon:0x7f9eae9f2b80:ReferenceExample@
    Target path:              </bicycle>
    Target layer stack:       @anon:0x7f9eae9f2400:tmp.usda@,@anon:0x7f9eae9f1000:tmp-session.usda@
    Map to parent:
        SdfLayerOffset(10, 1)
        /bicycle -> /bicycle
    Map to root:
        SdfLayerOffset(10, 1)
        /bicycle -> /bicycle
    Namespace depth:          1
    Depth below introduction: 0
    Permission:               Public
    Is restricted:            FALSE
    Is inert:                 FALSE
    Contribute specs:         TRUE
    Has specs:                TRUE
    Has symmetry:             FALSE
    Prim stack:
      </bicycle> anon:0x7f9eae9f2b80:ReferenceExample - @anon:0x7f9eae9f2b80:ReferenceExample@
```
~~~


~~~admonish tip title="Result of writing the graph to a dot .txt file | Click to view content" collapsible=true
```txt
{{#include pcpPrimIndex.txt}}
```
~~~

For example if we run it on a more advanced composition, in this case Houdini's pig asset:

~~~admonish tip title="Python print output for Houdini's pig asset | Click to view content" collapsible=true
```python
Pcp Node Ref
<pxr.Pcp.NodeRef object at 0x7f9ed3ad19e0> Pcp.ArcTypeRoot /pig /pig
<pxr.Pcp.NodeRef object at 0x7f9ed3ad17b0> Pcp.ArcTypeInherit /__class__/pig /pig
<pxr.Pcp.NodeRef object at 0x7f9ed3ad1cf0> Pcp.ArcTypeReference /pig /pig
<pxr.Pcp.NodeRef object at 0x7f9ed3ad1970> Pcp.ArcTypeInherit /__class__/pig /pig
<pxr.Pcp.NodeRef object at 0x7f9ed3ad1890> Pcp.ArcTypeVariant /pig{geo=medium} /pig{geo=medium}
<pxr.Pcp.NodeRef object at 0x7f9ed3ad1270> Pcp.ArcTypePayload /pig /pig
<pxr.Pcp.NodeRef object at 0x7f9ed3ad1660> Pcp.ArcTypeReference /pig /pig
<pxr.Pcp.NodeRef object at 0x7f9ed3ad1510> Pcp.ArcTypeVariant /pig{geo=medium} /pig{geo=medium}
<pxr.Pcp.NodeRef object at 0x7f9ed3ad13c0> Pcp.ArcTypeReference /ASSET_geo_variant_1/ASSET /pig
<pxr.Pcp.NodeRef object at 0x7f9ed3abbd60> Pcp.ArcTypeVariant /ASSET_geo_variant_1/ASSET{mtl=default} /pig{mtl=default}
<pxr.Pcp.NodeRef object at 0x7f9ed3abb6d0> Pcp.ArcTypeReference /ASSET_geo_variant_1/ASSET_mtl_default /pig
<pxr.Pcp.NodeRef object at 0x7f9ed3ad1a50> Pcp.ArcTypeReference /pig /pig
<pxr.Pcp.NodeRef object at 0x7f9ed3ad15f0> Pcp.ArcTypeReference /ASSET_geo_variant_2/ASSET /pig
<pxr.Pcp.NodeRef object at 0x7f9ed3abbe40> Pcp.ArcTypeVariant /ASSET_geo_variant_2/ASSET{geo=medium} /pig{geo=medium}
<pxr.Pcp.NodeRef object at 0x7f9ed3ad1ac0> Pcp.ArcTypeReference /ASSET_geo_variant_1/ASSET /pig
<pxr.Pcp.NodeRef object at 0x7f9ed3abbf90> Pcp.ArcTypeVariant /ASSET_geo_variant_1/ASSET{geo=medium} /pig{geo=medium}
<pxr.Pcp.NodeRef object at 0x7f9ed3abb430> Pcp.ArcTypeReference /ASSET_geo_variant_0/ASSET /pig
<pxr.Pcp.NodeRef object at 0x7f9ed3abb9e0> Pcp.ArcTypeVariant /ASSET_geo_variant_0/ASSET{geo=medium} /pig{geo=medium}
```
~~~

~~~admonish tip title="Result of writing the graph to a dot .txt file for Houdini's pig asset | Click to view content" collapsible=true
```txt
{{#include pcpPrimIndexPig.txt}}
```
~~~

![Alt text](pcpPrimIndexPig.png)

### Prim Composition Query <a name="pcpPrimCompositionQuery"></a>
Next let's look at prim composition queries. Instead of having to filter the prim index ourselves, we can use the `Usd.PrimCompositionQuery` to do it for us. More info in the [USD API docs](https://openusd.org/dev/api/class_usd_prim_composition_query.html).

The query works by specifying a filter and then calling `GetCompositionArcs`.

USD provides these convenience filters, it returns a new `Usd.PrimCompositionQuery` instance with the filter applied:
- `Usd.PrimCompositionQuery.GetDirectInherits(prim)`: Returns all non ancestral inherit arcs
- `Usd.PrimCompositionQuery.GetDirectReferences(prim)`: Returns all non ancestral reference arcs
- `Usd.PrimCompositionQuery.GetDirectRootLayerArcs(prim)`: Returns arcs that were defined in the active layer stack.

These are the sub-filters that can be set. We can only set a single token value per filter:
- **ArcTypeFilter**: 
    - `Usd.PrimCompositionQuery.ArcTypeFilter.All`
    - `Usd.PrimCompositionQuery.ArcTypeFilter.Inherit`
    - `Usd.PrimCompositionQuery.ArcTypeFilter.Variant`
    - `Usd.PrimCompositionQuery.ArcTypeFilter.NotVariant`
    - `Usd.PrimCompositionQuery.ArcTypeFilter.Reference`
    - `Usd.PrimCompositionQuery.ArcTypeFilter.Payload`
    - `Usd.PrimCompositionQuery.ArcTypeFilter.NotReferenceOrPayload`
    - `Usd.PrimCompositionQuery.ArcTypeFilter.ReferenceOrPayload`
    - `Usd.PrimCompositionQuery.ArcTypeFilter.InheritOrSpecialize` 
    - `Usd.PrimCompositionQuery.ArcTypeFilter.NotInheritOrSpecialize` 
    - `Usd.PrimCompositionQuery.ArcTypeFilter.Specialize`
- **DependencyTypeFilter**: Filter based on if the arc was introduced on a parent prim or on the prim itself.
    - `Usd.PrimCompositionQuery.DependencyTypeFilter.All`
    - `Usd.PrimCompositionQuery.DependencyTypeFilter.Direct`
    - `Usd.PrimCompositionQuery.DependencyTypeFilter.Ancestral`
- **ArcIntroducedFilter**: Filter based on where the arc was introduced.
    - `Usd.PrimCompositionQuery.ArcIntroducedFilter.All`
    - `Usd.PrimCompositionQuery.ArcIntroducedFilter.IntroducedInRootLayerStack`
    - `Usd.PrimCompositionQuery.ArcIntroducedFilter.IntroducedInRootLayerPrimSpec`
- **HasSpecsFilter**: Filter based if the arc has any specs (For example an inherit might not find any in the active layer stack)
    - `Usd.PrimCompositionQuery.HasSpecsFilter.All`
    - `Usd.PrimCompositionQuery.HasSpecsFilter.HasSpecs`
    - `Usd.PrimCompositionQuery.HasSpecsFilter.HasNoSpecs`

~~~admonish tip title=""
```python
{{#include ../../../../code/core/composition.py:pcpPrimCompositionQuery}}
```
~~~

The returned filtered `Usd.CompositionArc` objects, allow us to inspect various things about the arc. You can find more info in the [API docs](https://openusd.org/dev/api/class_usd_prim_composition_query_arc.html)
