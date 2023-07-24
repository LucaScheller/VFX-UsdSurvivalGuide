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
To summarize: Composition (the process of calculating the value sources) is cached, value resolution is not, to allow random access to data.
~~~

For a detailed explanation, checkout the [Value Resolution](https://openusd.org/release/glossary.html#usdglossary-valueresolution) docs page.

# Table of contents
1. [Prim Cache Population (PCP) In-A-Nutshell](#summary)
1. [What should I use it for?](#usage)
1. [Resources](#resources)
1. [Overview](#overview)
1. [Inspecting Composition Internals](#pcpInspect)

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
- [Value Resolution](https://openusd.org/release/glossary.html#usdglossary-valueresolution)
- [USD binary crate file format](https://openusd.org/release/glossary.html#crate-file-format)

## Overview <a name="overview"></a>
This page currently focuses on the practical usage of the `Pcp` module, it doesn't aim to explain how the composition engine works under the hood. (As the author(s) of this guide also don't know 😉, if you know more in-depth knowledge, please feel free to share!)

There is a really cool plugin for the [UsdView](../elements/standalone_utilities.md) by [chrizzftd](https://github.com/chrizzFTD) called [The Grill](https://grill.readthedocs.io/en/latest/views.html), that renders out the dot graph representation interactively based on the selected prim.

In the examples below, we'll look at how to do this ourselves via Python.

## Inspecting Composition Internals <a name="pcpInspect"></a>
To query data about composition, we have to go through the high level Usd API first, as the Sdf low level API is not aware of composition related data.
The high level Usd API then queries into the low level Pcp (Prim cache population) API, which tracks all composition related data and builds a value source index called **prim index**. 
In simple terms: A stack of layers per prim (and therefore also property) that knows about all the value sources (layers) a value can come from. Once a value is requested, the highest layer in the stack wins and returns the value for attributes. For metadata and relationships the value resolution can consult multiple layers, depending on how it was authored (see [list editable ops](../composition/listeditableops.md)).

Let's go through some examples in Houdini with Houdini's standard pig test asset.


```python
from pxr import Sdf, Usd
# Create stage with two different layers
stage = Usd.Stage.CreateInMemory()
root_layer = stage.GetRootLayer()
layer_top = Sdf.Layer.CreateAnonymous("exampleTopLayer")
layer_bottom = Sdf.Layer.CreateAnonymous("exampleBottomLayer")
root_layer.subLayerPaths.append(layer_top.identifier)
root_layer.subLayerPaths.append(layer_bottom.identifier)
# Define specs in two different layers
prim_path = Sdf.Path("/cube")
stage.SetEditTarget(layer_top)
prim = stage.DefinePrim(prim_path, "Xform")
prim.SetTypeName("Cube")
stage.SetEditTarget(layer_bottom)
prim = stage.DefinePrim(prim_path, "Xform")
prim.SetTypeName("Cube")
# Print the stack (set of layers that contribute data to this prim)
print(prim.GetPrimStack()) # Returns: [Sdf.Find('anon:0x7f6e590dc300:exampleTopLayer', '/cube'), Sdf.Find('anon:0x7f6e590dc580:exampleBottomLayer', '/cube')]
print(prim.GetPrimIndex()) # More on this in our [Pcp section]()
print(prim.ComputeExpandedPrimIndex()) # More on this in our [Pcp section](). you'll always want to use the expanded version, otherwise you might miss some data sources!
```




from subprocess import call

print("-----")

prim = stage.GetPrimAtPath("/workspace/asset")
#print(prim.GetPrimStack())

#print(dir(prim))
#print(prim.GetPrimTypeInfo())
#print(prim.GetPrimDefinition())


prim_index = prim.GetPrimIndex()

prim_index = prim.ComputeExpandedPrimIndex()
print("Pcp Prim Index", dir(prim_index))
# print(prim_index.DumpToString())
graph_file_path = "/mnt/data/WORKSPACE/test.txt"
graph_viz_png_file_path = graph_file_path.replace(".txt", ".png")
graph_viz_svg_file_path = graph_file_path.replace(".txt", ".svg")
prim_index.DumpToDotGraph(graph_file_path, includeMaps=False)
call(["dot", "-Tpng", graph_file_path, "-o", graph_viz_png_file_path])
call(["dot", "-Tsvg", graph_file_path, "-o", graph_viz_svg_file_path])
#dot -Tpng test.txt -o test.png

def iterater_child_nodes(root_node):
    yield root_node
    for child_node in root_node.children:
        for child_child_node in iterater_child_nodes(child_node):
            yield child_child_node

def iterater_parent_nodes(root_node):
    iter_node = root_node
    while iter_node:
        yield iter_node
        iter_node = iter_node.parent
            
print("Pcp Node Ref", dir(prim_index.rootNode))
#print(prim_index.primStack)
print("Children")

for child in list(iterater_child_nodes(prim_index.rootNode))[::1]:
    print(child, child.arcType, child.path, child.mapToRoot.MapSourceToTarget(child.path))



