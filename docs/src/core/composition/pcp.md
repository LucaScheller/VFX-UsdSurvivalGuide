# Prim Cache Population (PCP) - Cache for value resolution

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

