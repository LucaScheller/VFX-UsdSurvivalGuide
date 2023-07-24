# Creating efficient LOPs .Hdas
- [Dealing with time dependencies](./dcc/houdini/hda/timedependency.md)
- [Order of operations](./dcc/houdini/hda/order_of_operations.md)
- [Layer Size](./dcc/houdini/hda/layers.md)
- [Copying Data & Traversal of Hierarchies](./dcc/houdini/hda/data_modify.md)


- [Solaris Performance](https://www.sidefx.com/docs/houdini/solaris/performance.html)

# Table of contents
1. [LOP Hdas - In-A-Nutshell](#summary)
1. [What should I use it for?](#usage)
1. [Resources](#resources)
1. [Performance](#overview)
    1. [Write full time sample ranges](#) 
    1. [Layer Content Size](#layerContentSize)
    1. [Layer Count](#layerCount)

## Layer Content Size <a name="layerContentSize"></a>
In Houdini the size of the active layer can impact performance.

To quote from the docs:
~~~admonish tip
As LOP layers have more and more opinions and values added, there can be slow-downs in the viewport. If you notice simple transforms are very slow in the viewport, try using a Configure Layer to start a new layer above where you're working, and see if that improves interactivity.
~~~
Let's build a test setup, where we provoke the problem on purpose:

~~~admonish tip title=""
```python
from pxr import Sdf
node = hou.pwd()
layer = node.editableLayer()
with Sdf.ChangeBlock():
    root_grp_prim_path = Sdf.Path(f"/root_grp")
    root_grp_prim_spec = Sdf.CreatePrimInLayer(layer, root_grp_prim_path)
    root_grp_prim_spec.typeName = "Xform"
    root_grp_prim_spec.specifier = Sdf.SpecifierDef
    
    prim_count = 1000 * 100
    for idx in range(prim_count):
        prim_path = Sdf.Path(f"/root_grp/prim_{idx}")
        prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
        prim_spec.typeName = "Xform"
        prim_spec.specifier = Sdf.SpecifierDef
        attr_spec = Sdf.AttributeSpec(prim_spec, "debug", Sdf.ValueTypeNames.Float)
        attr_spec.default = float(idx)
```
~~~

~~~admonish danger
Now if we add an edit property node and tweak the "debug" attribute on prim "/root_grp/prim_0", it will take around 600 milliseconds!
~~~

The simple solution as stated above is to simply add a "Configure Layer" LOP node and enable "Start New Layer". Now all edits are fast again.

So why is this slow? It is actually due to how Houdini makes node based editing of layers possible. Houdini tries to efficiently cache only the active layer, where all the edits go, per node (if a node did write operations). The active layer in Houdini speak is the same as the stage's edit target layer. This means every node creates a duplicate of the active layer, so that we can jump around the network and display different nodes, without recalculating everything all the time. The down side is the copying of the data, which is causing the performance hit we are seeing.

The solution is simple: Just start a new layer and then everything is fast again (as it doesn't have to copy all the content). Houdini colors codes its nodes every time they start a new (active) layer, so you'll also see a visual indicator that the nodes after the "Configure Layer" LOP are on a new layer.

~~~admonish tip title="Pro Tip | Layer size in Hdas"
What does this mean for our .hda setups? The answer is simple: As there is no downside to having a large layer count (unless we start going into the thousands), each .hda can simply start of and end with creating a new layer. That way all the edits in the .hda are guaranteed to not be impacted by this caching issue.
~~~

Here is a comparison video:

![Layer Content Size](layerContentSize.gif)

## Layer Count <a name="layerCount"></a>
Now as mentioned in the [layer content size](#layerContentSize) section, there is no down side to having thousands of layers. Houdini will merge these to a single (or multiple, depending on how you configured your save paths) layers on USD rop render. Since this is done on write, the described active layer stashing mechanism doesn't kick in and therefore it stays fast.

Does that mean we should write everything on a new layer? No, the sweet spot is somewhere in between. For example when grafting (moving a certain part of the hierarchy somewhere else) we also have to flatten the layer on purpose (Houdini's "Scene Restructure"/"Graft" nodes do this for us). At some layer count, you will encounter longer layer merging times, so don't over do it! This can be easily seen with the LOPs for loop.

~~~admonish tip title="Pro Tip | Layer count"
So as a rule of thumb: Encapsulate heavy layer edits with newly started layers, that way the next node downstream will run with optimal performance. Everything else is usually fine to be on the active input layer.
~~~

In LOPs we also often work with the principle of having a "main" node stream (the stream, where your shot layers are loaded from). A good workflow would be to always put anything you merge into the main node stream into a new layer, as often these "side" streams create heavy data.