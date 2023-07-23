# Prim Cache Population (PCP) - Cache for value resolution








#### Composition Internals
To query data about composition, we have to go through the high level Usd API first, as the Sdf low level API is not aware of composition related data.
The high level Usd API then queries into the low level Pcp (Prim cache population) API, which tracks all composition related data and builds a value resolution index, 
in simple terms: A stack of layers per spec (prim/property) that knows about all the value sources (layers) a value can come from. Once a value is requested, the highest layer in the stack wins and returns the value.
We cover more about this topic in our [Pcp]() section and our query cache sections.


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


```python


#### Composition Instancing/Instanceable prims
We cover instancing in our [Instancing] section.
##### Instanceable Prims
# Has: IsInstanceable', HasAuthoredInstanceable',
# Get: 'GetInstances'
# Set: 'SetInstanceable'
# Clear: 'ClearInstanceable'

To check if our prim in a prototype (Usd speak for 'hiearchy that gets duplicated')

##### Prototypes
# Has: 'IsInPrototype', 'IsPathInPrototype',  'IsPrototype',  'IsInstance',  'IsInstanceProxy', 'IsPrototypePath'
# Get: 'GetPrimInPrototype', 'GetPrototype'
```








----------------------------
Scratch space



Now if you read through the USD docs/glossary, you'll notice a recurring sentence, when it comes to composition:
 


So far so good? Now let's bring layers/a layer stack into the mix. 



~~~admonish danger title="List-Editable Ops | Combined Value"
When multiple list editable ops from different layers get combined, each individual sub-list in each list editable op gets combined based on the layer order. It does not get "applied" in the sense that it flattens out the list to a single 

It is very important to know, that list editable ops only store lists these sublists, and don't actually 

~~~



~~~admonish tip title=""
```python

# No you m


# To get only added/explicit items (This does not make use of the deleteItems remove list!):
print(path_list_op.GetAddedOrExplicitItems()) # Returns: [Sdf.Path('/cube'), Sdf.Path('/sphere')]
print(path_list_op.GetAddedOrExplicitItems()) # Returns: [Sdf.Path('/cube'), Sdf.Path('/sphere')]

# We can also mark it as "explicit", this means that any other values from la

['ApplyOperations', 'Clear', 'ClearAndMakeExplicit', 'Create', 'CreateExplicit', 'GetAddedOrExplicitItems', 
'HasItem', 'isExplicit',

# Setup scene
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
layer_top = Sdf.Layer.CreateAnonymous()
layer_middle = Sdf.Layer.CreateAnonymous()
layer_bottom = Sdf.Layer.CreateAnonymous()
layers = [layer_top, layer_middle, layer_bottom]
stage.GetRootLayer().subLayerPaths = [l.identifier for l in layers]
prim_path = Sdf.Path("/cube")
for layer in layers:
    prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
    prim_spec.specifier = Sdf.SpecifierDef
    prim_spec.typeName = "Cube"
top_prim_spec = layer_top.GetPrimAtPath(prim_path)
middle_prim_spec = layer_middle.GetPrimAtPath(prim_path)
bottom_prim_spec = layer_bottom.GetPrimAtPath(prim_path)
# Write list editable ops for inherits

```
~~~

