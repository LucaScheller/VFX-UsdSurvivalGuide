# Composition (Combining layers)
































#### Local
#### Local Value Clips

#### Inherits:
- 'inheritPathList' 
#### Variants
-- 'variantSelections', 'BlockVariantSelection', 'GetVariantNames'
-- 'variantSets', 'variantSetNameList',
#### References
- 'hasReferences', 'referenceList', 'ClearReferenceList'
#### Payloads
- 'hasPayloads', 'payloadList', 'ClearPayloadList'
#### Specialize
- 'specializesList',


## Composition (High Level API)
We

# Has: 'HasAuthoredInherits', 'HasVariantSets', 'HasAuthoredReferences', 'HasPayload', 'HasAuthoredPayloads'
# Get: 'GetInherits', 'GetTypeName', 'GetReferences', 'GetPayloads'
# Set: 'SetPayload', 'SetTypeName', 'GetSpecializes', 'HasAuthoredSpecializes'
# Clear: 'ClearPayload', 'ClearDocumentation'



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
 