#// ANCHOR: compositionListEditableOpsBasics
from pxr import Sdf
# Sdf.ReferenceListOp, Sdf.PayloadListOp, Sdf.PathListOp,
path_list_op = Sdf.PathListOp()
# There are multiple sub-lists, which are just normal Python lists.
# 'prependedItems', 'appendedItems', 'deletedItems', 'explicitItems',
# Legacy sub-lists (do not use these anymore): 'addedItems', 'orderedItems'
# Currently the way these are exposed to Python, you have to re-assign the list, instead of editing it in place.
# So this won't work:
path_list_op.prependedItems.append(Sdf.Path("/cube"))
path_list_op.appendedItems.append(Sdf.Path("/sphere"))
# Instead do this:
path_list_op.prependedItems = [Sdf.Path("/cube")]
path_list_op.appendedItems = [Sdf.Path("/sphere")]
# To clear the list op:
print(path_list_op) # Returns: SdfPathListOp(Prepended Items: [/cube], Appended Items: [/sphere])
path_list_op.Clear()
print(path_list_op) # Returns: SdfPathListOp()
# Repopulate via constructor
path_list_op = Sdf.PathListOp.Create(prependedItems = [Sdf.Path("/cube")], appendedItems = [Sdf.Path("/sphere")])
print(path_list_op) # Returns: SdfPathListOp(Prepended Items: [/cube], Appended Items: [/sphere])
# Add remove items
path_list_op.deletedItems = [Sdf.Path("/sphere")]
print(path_list_op) # Returns: SdfPathListOp(Deleted Items: [/sphere], Prepended Items: [/cube], Appended Items: [/sphere])
# Notice how it just stores lists, it doesn't actually apply them. We'll have a look at that next.

# In the high level API, all the function signatures that work on list-editable ops
# usually take a position kwarg which corresponds to what list to edit and the position (front/back)
Usd.ListPositionFrontOfAppendList
Usd.ListPositionBackOfAppendList
Usd.ListPositionFrontOfPrependList
Usd.ListPositionBackOfPrependList
# We cover how to use this is our 'Composition Arcs' section.
#// ANCHOR_END: compositionListEditableOpsBasics

#// ANCHOR: compositionListEditableOpsMerging
from pxr import Sdf
### Merging basics ###
path_list_op_layer_top = Sdf.PathListOp.Create(deletedItems = [Sdf.Path("/cube")])
path_list_op_layer_middle = Sdf.PathListOp.Create(prependedItems = [Sdf.Path("/disc"), Sdf.Path("/cone")])
path_list_op_layer_bottom = Sdf.PathListOp.Create(prependedItems = [Sdf.Path("/cube")], appendedItems = [Sdf.Path("/cone"),Sdf.Path("/sphere")])

result = Sdf.PathListOp()
result = result.ApplyOperations(path_list_op_layer_top)
result = result.ApplyOperations(path_list_op_layer_middle)
result = result.ApplyOperations(path_list_op_layer_bottom)
# Notice how on merge it makes sure that each sublist does not have the values of the other sublists, just like a Python set()
print(result) # Returns: SdfPathListOp(Deleted Items: [/cube], Prepended Items: [/disc, /cone], Appended Items: [/sphere])
# Get the flattened result. This does not apply the deleteItems, only ApplyOperations does that. 
print(result.GetAddedOrExplicitItems()) # Returns: [Sdf.Path('/disc'), Sdf.Path('/cone'), Sdf.Path('/sphere')]

### Deleted and added items ###
path_list_op_layer_top = Sdf.PathListOp.Create(appendedItems=[Sdf.Path("/disc"), Sdf.Path("/cube")])
path_list_op_layer_middle = Sdf.PathListOp.Create(deletedItems = [Sdf.Path("/cube")])
path_list_op_layer_bottom = Sdf.PathListOp.Create(prependedItems = [Sdf.Path("/cube")], appendedItems = [Sdf.Path("/sphere")])

result = Sdf.PathListOp()
result = result.ApplyOperations(path_list_op_layer_top)
result = result.ApplyOperations(path_list_op_layer_middle)
result = result.ApplyOperations(path_list_op_layer_bottom)
print(result) # Returns: SdfPathListOp(Appended Items: [/sphere, /disc, /cube])
# Since it now was in the explicit list, it got removed.

### Explicit mode ###
# There is also an "explicit" mode. This clears all previous values on merge and marks the list as explicit.
# Once explicit and can't be un-explicited. An explicit list is like a reset, it 
# doesn't know anything about the previous values anymore. All lists that are merged
# after combine the result to be explicit.
path_list_op_layer_top = Sdf.PathListOp.Create(deletedItems = [Sdf.Path("/cube")])
path_list_op_layer_middle = Sdf.PathListOp.CreateExplicit([Sdf.Path("/disc")])
path_list_op_layer_bottom = Sdf.PathListOp.Create(prependedItems = [Sdf.Path("/cube")], appendedItems = [Sdf.Path("/sphere")])

result = Sdf.PathListOp()
result = result.ApplyOperations(path_list_op_layer_top)
result = result.ApplyOperations(path_list_op_layer_middle)
result = result.ApplyOperations(path_list_op_layer_bottom)
print(result, result.isExplicit) # Returns: SdfPathListOp(Explicit Items: [/disc]), True
# Notice how the deletedItems had no effect, as "/cube" is not in the explicit list.

path_list_op_layer_top = Sdf.PathListOp.Create(deletedItems = [Sdf.Path("/cube")])
path_list_op_layer_middle = Sdf.PathListOp.CreateExplicit([Sdf.Path("/disc"), Sdf.Path("/cube")])
path_list_op_layer_bottom = Sdf.PathListOp.Create(prependedItems = [Sdf.Path("/cube")], appendedItems = [Sdf.Path("/sphere")])

result = Sdf.PathListOp()
result = result.ApplyOperations(path_list_op_layer_top)
result = result.ApplyOperations(path_list_op_layer_middle)
result = result.ApplyOperations(path_list_op_layer_bottom)
print(result, result.isExplicit) # Returns: SdfPathListOp(Explicit Items: [/disc]), True
# Since it now was in the explicit list, it got removed.
#// ANCHOR_END: compositionListEditableOpsMerging


#// ANCHOR: compositionArcSublayer
# For sublayering we modify the .subLayerPaths attribute on a layer.
# This is the same for both the high and low level API.
### High Level & Low Level ###
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
# Layer onto root layer
layer_a = Sdf.Layer.CreateAnonymous()
layer_b = Sdf.Layer.CreateAnonymous()
root_layer = stage.GetRootLayer()
# Here we pass in the file paths (=layer identifiers).
root_layer.subLayerPaths.append(layer_a.identifier)
root_layer.subLayerPaths.append(layer_b.identifier)
# Once we have added the sublayers, we can also access their layer offsets:
print(root_layer.subLayerOffsets) # Returns: [Sdf.LayerOffset(), Sdf.LayerOffset()]
# Since layer offsets are ready only copies, we need to assign a newly created 
# layer offset if we want to modify them. We also can't replace the whole list, as
# it needs to keep a pointer to the array.
layer_offset_a = root_layer.subLayerOffsets[0]
root_layer.subLayerOffsets[0] = Sdf.LayerOffset(offset=layer_offset_a.offset + 10, 
                                                scale=layer_offset_a.scale * 2)
layer_offset_b = root_layer.subLayerOffsets[1]
root_layer.subLayerOffsets[1] = Sdf.LayerOffset(offset=layer_offset_b.offset - 10, 
                                                scale=layer_offset_b.scale * 0.5)
print(root_layer.subLayerOffsets) # Returns: [Sdf.LayerOffset(10, 2), Sdf.LayerOffset(-10, 0.5)]

# If we want to sublayer on the active layer, we just add it there.
layer_c = Sdf.Layer.CreateAnonymous()
active_layer = stage.GetEditTarget().GetLayer()
root_layer.subLayerPaths.append(layer_c.identifier)
#// ANCHOR_END: compositionArcSublayer


#// ANCHOR: compositionArcSublayerHoudini
### High Level & Low Level ###
import loputils
from pxr import Sdf
# Hou LOP Node https://www.sidefx.com/docs/houdini/hom/hou/LopNode.html
# See $HFS/houdini/python3.9libs/loputils.py
"""
def createPythonLayer(node, savepath=None):
    # Tag the layer as "LOP" so we know it was created by LOPs.
    layer = Sdf.Layer.CreateAnonymous('LOP')
    # Add a Houdini Layer Info prim where we can put the save path.
    p = Sdf.CreatePrimInLayer(layer, '/HoudiniLayerInfo')
    p.specifier = Sdf.SpecifierDef
    p.typeName = 'HoudiniLayerInfo'/stage/list_editable_ops/pythonscript6
    if savepath:
        p.customData['HoudiniSavePath'] = hou.text.expandString(savepath)
        p.customData['HoudiniSaveControl'] = 'Explicit'
    # Let everyone know what node created this layer.
    p.customData['HoudiniCreatorNode'] = node.sessionId()
    p.customData['HoudiniEditorNodes'] = Vt.IntArray([node.sessionId()])
    node.addHeldLayer(layer.identifier)
    return layer
"""
# Sublayer onto root layer via Python LOP node
node = hou.pwd()
stage = node.editableStage()
layer = loputils.createPythonLayer(node, '$HIP/myfile.usda')
node.addSubLayer(layer.identifier)
# This doesn't seem to work at the moment, as Houdini does some custom root layer handeling
# print(root_layer.subLayerPaths) # Our added layer does not show up. So we have to use the `sublayer` node.
# root_layer = stage.GetRootLayer()
# root_layer.subLayerOffsets[0] = Sdf.LayerOffset(offset=10, scale=1)

# Sublayer onto active layer via Python LOP node, here we can do the usual.
node = hou.pwd()
layer = node.editableLayer()
layer_a = loputils.createPythonLayer(node, '$HIP/myfile.usda')
layer.subLayerPaths.append(layer_a.identifier)
layer.subLayerOffsets[0] = Sdf.LayerOffset(offset=10, scale=1)

# Since layers are automatically garbage collected once they go out of scope,
# we can tag them to keep them persistently in memory for the active session.
layer_b = Sdf.Layer.CreateAnonymous()
node.addHeldLayer(layer_b.identifier)
# This can then be re-used via the standard anywhere in Houdini.
layer_b = Sdf.Layer.FindOrOpen(layer_b.identifier)
#// ANCHOR_END: compositionArcSublayerHoudini


#// ANCHOR: compositionArcInherit
### High Level ###
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
bicycle_prim_path = Sdf.Path("/bicycle")
bicycle_prim = stage.DefinePrim(bicycle_prim_path)
cube_prim_path = Sdf.Path("/cube")
cube_prim = stage.DefinePrim(cube_prim_path, "Cube")
inherits_api = bicycle_prim.GetInherits()
inherits_api.AddInherit(cube_prim_path, position=Usd.ListPositionFrontOfAppendList)
# inherits_api.SetInherits() # Clears the list editable ops and authors an Sdf.PathListOp.CreateExplicit([])
# inherits_api.RemoveInherit(cube_prim_path)
# inherits_api.ClearInherits() # Sdf.PathListOp.Clear()
# inherits_api.GetAllDirectInherits() # Returns all inherits generated in the active layer stack
### Low Level ###
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
bicycle_prim_path = Sdf.Path("/bicycle")
bicycle_prim_spec = Sdf.CreatePrimInLayer(layer, bicycle_prim_path)
bicycle_prim_spec.specifier = Sdf.SpecifierDef
cube_prim_path = Sdf.Path("/cube")
cube_prim_spec = Sdf.CreatePrimInLayer(layer, cube_prim_path)
cube_prim_spec.specifier = Sdf.SpecifierDef
cube_prim_spec.typeName = "Cube"
bicycle_prim_spec.inheritPathList.appendedItems = [cube_prim_path]
#// ANCHOR_END: compositionArcInherit

#// ANCHOR: compositionArcVariant
### High Level ###
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()

bicycle_prim_path = Sdf.Path("/bicycle")
bicycle_prim = stage.DefinePrim(bicycle_prim_path, "Xform")
## Methods of Usd.VariantSets
# Has: 'HasVariantSet'
# Get: 'GetNames', 'GetVariantSet', 'GetVariantSelection', 'GetAllVariantSelections'
# Set: 'AddVariantSet', 'SetSelection'
variant_sets_api = bicycle_prim.GetVariantSets()
## Methods of Usd.VariantSet
# Has: 'HasAuthoredVariant', 'HasAuthoredVariantSelection'
# Get: 'GetName', 'GetVariantNames', 'GetVariantSelection', 'GetVariantEditContext', 'GetVariantEditTarget'
# Set: 'AddVariant', 'SetVariantSelection'
# Clear: 'BlockVariantSelection', 'ClearVariantSelection'
variant_set_api = variant_sets_api.AddVariantSet("color", position=Usd.ListPositionBackOfPrependList)
variant_set_api.AddVariant("colorA")
# If we want to author on the selected variant, we have to select it first
variant_set_api.SetVariantSelection("colorA")
with variant_set_api.GetVariantEditContext():
    # Anything we write in the context, goes into the variant (prims and properties)
    cube_prim_path = bicycle_prim_path.AppendChild("cube")
    cube_prim = stage.DefinePrim(cube_prim_path, "Cube")
# We can also generate the edit target ourselves, but we still need to set the
# variant selection, seems like a bug. Changing variants is a heavy op ...
variant_set_api.AddVariant("colorB")
variant_set_api.SetVariantSelection("colorB")
variant_prim_path = bicycle_prim_path.AppendVariantSelection("color", "colorB") 
layer = stage.GetEditTarget().GetLayer()
edit_target = Usd.EditTarget.ForLocalDirectVariant(layer, variant_prim_path)
# Or
edit_target = variant_set_api.GetVariantEditTarget()
edit_context = Usd.EditContext(stage, edit_target) 
with edit_context as ctx:
    sphere_prim_path = bicycle_prim_path.AppendChild("sphere")
    sphere_prim = stage.DefinePrim("/bicycle/sphere", "Sphere")
### Low Level ###
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
bicycle_prim_path = Sdf.Path("/bicycle")
bicycle_prim_spec = Sdf.CreatePrimInLayer(layer, bicycle_prim_path)
bicycle_prim_spec.specifier = Sdf.SpecifierDef
bicycle_prim_spec.typeName = "Xform"
# Variants
cube_prim_path = bicycle_prim_path.AppendVariantSelection("color", "colorA").AppendChild("cube")
cube_prim_spec = Sdf.CreatePrimInLayer(layer, cube_prim_path)
cube_prim_spec.specifier = Sdf.SpecifierDef
cube_prim_spec.typeName = "Cube"
sphere_prim_path = bicycle_prim_path.AppendVariantSelection("color", "colorB").AppendChild("sphere")
sphere_prim_spec = Sdf.CreatePrimInLayer(layer, sphere_prim_path)
sphere_prim_spec.specifier = Sdf.SpecifierDef
sphere_prim_spec.typeName = "Sphere"
# Variant Selection
bicycle_prim_spec.variantSelections["color"] = "colorA"

# We can also author the variants via variant specs
layer = Sdf.Layer.CreateAnonymous()
car_prim_path = Sdf.Path("/car")
car_prim_spec = Sdf.CreatePrimInLayer(layer, car_prim_path)
car_prim_spec.specifier = Sdf.SpecifierDef
car_prim_spec.typeName = "Xform"
# Variants
variant_set_spec = Sdf.VariantSetSpec(car_prim_spec, "color")
variant_spec = Sdf.VariantSpec(variant_set_spec, "colorA")
cube_prim_spec = Sdf.PrimSpec(variant_spec.primSpec, "cube", Sdf.SpecifierDef)
cube_prim_spec.typeName = "Cube"
variant_spec = Sdf.VariantSpec(variant_set_spec, "colorB")
cube_prim_spec = Sdf.PrimSpec(variant_spec.primSpec, "sphere", Sdf.SpecifierDef)
cube_prim_spec.typeName = "Sphere"
# Ironically this does not setup the variant set names metadata, so we have to author it ourselves.
car_prim_spec.SetInfo("variantSetNames", Sdf.StringListOp.Create(prependedItems=["color"]))
# Variant Selection
car_prim_spec.variantSelections["color"] = "colorA"
#// ANCHOR_END: compositionArcVariant

#// ANCHOR: compositionArcVariantCopySpec
from pxr import Sdf
# Spawn other layer, this usually comes from other stages, that your DCC creates/owns.
some_other_layer = Sdf.Layer.CreateAnonymous()
root_prim_path = Sdf.Path("/root")
cube_prim_path = Sdf.Path("/root/cube")
cube_prim_spec = Sdf.CreatePrimInLayer(some_other_layer, cube_prim_path)
cube_prim_spec.specifier = Sdf.SpecifierDef
cube_prim_spec.typeName = "Cube"
# Create demo layer
bicycle_prim_path = Sdf.Path("/bicycle")
bicycle_prim_spec = Sdf.CreatePrimInLayer(layer, bicycle_prim_path)
bicycle_prim_spec.specifier = Sdf.SpecifierDef
bicycle_prim_spec.typeName = "Xform"
# Copy content into variant
variant_set_spec = Sdf.VariantSetSpec(bicycle_prim_spec, "color")
variant_spec = Sdf.VariantSpec(variant_set_spec, "colorA")
variant_prim_path = bicycle_prim_path.AppendVariantSelection("color", "colorA")
Sdf.CopySpec(some_other_layer, root_prim_path, layer, variant_prim_path)
# Variant Selection
bicycle_prim_spec.SetInfo("variantSetNames", Sdf.StringListOp.Create(prependedItems=["color"]))
bicycle_prim_spec.variantSelections["color"] = "colorA"
#// ANCHOR_END: compositionArcVariantCopySpec


#// ANCHOR: compositionArcReferenceExternal
### High Level ###
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
# Spawn temp layer
reference_layer = Sdf.Layer.CreateAnonymous("ReferenceExample")
reference_bicycle_prim_path = Sdf.Path("/bicycle")
reference_bicycle_prim_spec = Sdf.CreatePrimInLayer(reference_layer, reference_bicycle_prim_path)
reference_bicycle_prim_spec.specifier = Sdf.SpecifierDef
reference_bicycle_prim_spec.typeName = "Cube"
# Set the default prim to use when we specify no primpath. It can't be a prim path, it must be a root prim.
reference_layer.defaultPrim = reference_bicycle_prim_path.name
# Reference
reference_layer_offset = Sdf.LayerOffset(offset=10, scale=1)
reference = Sdf.Reference(reference_layer.identifier, reference_bicycle_prim_path, reference_layer_offset)
# Or: If we don't specify a prim, the default prim will get used, as set above
reference = Sdf.Reference(reference_layer.identifier, layerOffset=reference_layer_offset)
bicycle_prim_path = Sdf.Path("/bicycle")
bicycle_prim = stage.DefinePrim(bicycle_prim_path)
references_api = bicycle_prim.GetReferences()
references_api.AddReference(reference, position=Usd.ListPositionFrontOfAppendList)
# references_api.SetReferences() # Clears the list editable ops and authors an Sdf.ReferenceListOp.CreateExplicit([])
# references_api.RemoveReference(cube_prim_path)
# references_api.ClearReferences() # Sdf.ReferenceListOp.Clear()
### Low Level ###
from pxr import Sdf
# Spawn temp layer
reference_layer = Sdf.Layer.CreateAnonymous("ReferenceExample")
reference_bicycle_prim_path = Sdf.Path("/bicycle")
reference_bicycle_prim_spec = Sdf.CreatePrimInLayer(reference_layer, reference_bicycle_prim_path)
reference_bicycle_prim_spec.specifier = Sdf.SpecifierDef
reference_bicycle_prim_spec.typeName = "Cube"
reference_layer.defaultPrim = reference_bicycle_prim_path.name
# In Houdini add, otherwise the layer will be garbage collected.
# node.addHeldLayer(reference_layer.identifier)
# Reference
layer = Sdf.Layer.CreateAnonymous()
bicycle_prim_path = Sdf.Path("/bicycle")
bicycle_prim_spec = Sdf.CreatePrimInLayer(layer, bicycle_prim_path)
bicycle_prim_spec.specifier = Sdf.SpecifierDef
reference_layer_offset = Sdf.LayerOffset(offset=10, scale=1)
reference = Sdf.Reference(reference_layer.identifier, reference_bicycle_prim_path, reference_layer_offset)
# Or: If we don't specify a prim, the default prim will get used, as set above
reference = Sdf.Reference(reference_layer.identifier, layerOffset=reference_layer_offset)
bicycle_prim_spec.referenceList.appendedItems = [reference]
#// ANCHOR_END: compositionArcReferenceExternal

#// ANCHOR: compositionArcReferenceClass
from pxr import Sdf
ref = Sdf.Reference("/file/path.usd", "/prim/path", Sdf.LayerOffset(offset=10, scale=1))
# The reference object is a read only instance.
print(ref.assetPath) # Returns: "/file/path.usd"
print(ref.primPath) # Returns: "/prim/path"
print(ref.layerOffset) # Returns: Sdf.LayerOffset(offset=10, scale=1)
try: 
    ref.assetPath = "/some/other/file/path.usd"
except Exception:
    print("Read only Sdf.Reference!")
#// ANCHOR_END: compositionArcReferenceClass

#// ANCHOR: compositionArcReferenceInternal
### High Level ###
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
# Spawn hierarchy
cube_prim_path = Sdf.Path("/cube")
cube_prim = stage.DefinePrim(cube_prim_path, "Cube")
bicycle_prim_path = Sdf.Path("/bicycle")
bicycle_prim = stage.DefinePrim(bicycle_prim_path)
# Reference
reference_layer_offset = Sdf.LayerOffset(offset=10, scale=1)
reference = Sdf.Reference("", cube_prim_path, reference_layer_offset)
references_api = bicycle_prim.GetReferences()
references_api.AddReference(reference, position=Usd.ListPositionFrontOfAppendList)
# Or:
references_api.AddInternalReference(cube_prim_path, reference_layer_offset, position=Usd.ListPositionFrontOfAppendList)
### Low Level ###
from pxr import Sdf
# Spawn hierarchy
layer = Sdf.Layer.CreateAnonymous()
cube_prim_path = Sdf.Path("/cube")
cube_prim_spec = Sdf.CreatePrimInLayer(layer, cube_prim_path)
cube_prim_spec.specifier = Sdf.SpecifierDef
cube_prim_spec.typeName = "Cube"
bicycle_prim_path = Sdf.Path("/bicycle")
bicycle_prim_spec = Sdf.CreatePrimInLayer(layer, bicycle_prim_path)
bicycle_prim_spec.specifier = Sdf.SpecifierDef
# Reference
reference_layer_offset = Sdf.LayerOffset(offset=10, scale=1)
reference = Sdf.Reference("", cube_prim_path, reference_layer_offset)
bicycle_prim_spec.referenceList.appendedItems = [reference]
#// ANCHOR_END: compositionArcReferenceInternal

#// ANCHOR: compositionArcPayloadClass
from pxr import Sdf
payload = Sdf.Payload("/file/path.usd", "/prim/path", Sdf.LayerOffset(offset=10, scale=1))
# The reference object is a read only instance.
print(payload.assetPath) # Returns: "/file/path.usd"
print(payload.primPath) # Returns: "/prim/path"
print(payload.layerOffset) # Returns: Sdf.LayerOffset(offset=10, scale=1)
try: 
    payload.assetPath = "/some/other/file/path.usd"
except Exception:
    print("Read only Sdf.Payload!")
#// ANCHOR_END: compositionArcPayloadClass


#// ANCHOR: compositionArcPayload
### High Level ###
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
# Spawn temp layer
payload_layer = Sdf.Layer.CreateAnonymous("PayloadExample")
payload_bicycle_prim_path = Sdf.Path("/bicycle")
payload_bicycle_prim_spec = Sdf.CreatePrimInLayer(payload_layer, payload_bicycle_prim_path)
payload_bicycle_prim_spec.specifier = Sdf.SpecifierDef
payload_bicycle_prim_spec.typeName = "Cube"
# Set the default prim to use when we specify no primpath. It can't be a prim path, it must be a root prim.
payload_layer.defaultPrim = payload_bicycle_prim_path.name
# Payload
payload_layer_offset = Sdf.LayerOffset(offset=10, scale=1)
payload = Sdf.Payload(payload_layer.identifier, payload_bicycle_prim_path, payload_layer_offset)
# Or: If we don't specify a prim, the default prim will get used, as set above
payload = Sdf.Payload(payload_layer.identifier, layerOffset=payload_layer_offset)
bicycle_prim_path = Sdf.Path("/bicycle")
bicycle_prim = stage.DefinePrim(bicycle_prim_path)
payloads_api = bicycle_prim.GetPayloads()
payloads_api.AddPayload(payload, position=Usd.ListPositionFrontOfAppendList)
# payloads_api.SetPayloads() # Clears the list editable ops and authors an Sdf.PayloadListOp.CreateExplicit([])
# payloads_api.RemovePayload(cube_prim_path)
# payloads_api.ClearPayloads() # Sdf.PayloadListOp.Clear()
### Low Level ###
from pxr import Sdf
# Spawn temp layer
payload_layer = Sdf.Layer.CreateAnonymous("PayLoadExample")
payload_bicycle_prim_path = Sdf.Path("/bicycle")
payload_bicycle_prim_spec = Sdf.CreatePrimInLayer(payload_layer, payload_bicycle_prim_path)
payload_bicycle_prim_spec.specifier = Sdf.SpecifierDef
payload_bicycle_prim_spec.typeName = "Cube"
payload_layer.defaultPrim = payload_bicycle_prim_path.name
# In Houdini add, otherwise the layer will be garbage collected.
# node.addHeldLayer(payload_layer.identifier)
# Payload
layer = Sdf.Layer.CreateAnonymous()
bicycle_prim_path = Sdf.Path("/bicycle")
bicycle_prim_spec = Sdf.CreatePrimInLayer(layer, bicycle_prim_path)
bicycle_prim_spec.specifier = Sdf.SpecifierDef
payload_layer_offset = Sdf.LayerOffset(offset=10, scale=1)
payload = Sdf.Payload(payload_layer.identifier, payload_bicycle_prim_path, payload_layer_offset)
# Or: If we don't specify a prim, the default prim will get used, as set above
payload = Sdf.Payload(payload_layer.identifier, layerOffset=payload_layer_offset)
bicycle_prim_spec.payloadList.appendedItems = [payload]
#// ANCHOR_END: compositionArcPayload


#// ANCHOR: compositionArcSpecialize
### High Level ###
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
bicycle_prim_path = Sdf.Path("/bicycle")
bicycle_prim = stage.DefinePrim(bicycle_prim_path)
cube_prim_path = Sdf.Path("/cube")
cube_prim = stage.DefinePrim(cube_prim_path, "Cube")
specializes_api = bicycle_prim.GetSpecializes()
specializes_api.AddSpecialize(cube_prim_path, position=Usd.ListPositionFrontOfAppendList)
# inherits_api.SetSpecializes() # Clears the list editable ops and authors an Sdf.PathListOp.CreateExplicit([])
# inherits_api.RemoveSpecialize(cube_prim_path)
# inherits_api.ClearSpecializes() # Sdf.PathListOp.Clear()
### Low Level ###
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
bicycle_prim_path = Sdf.Path("/bicycle")
bicycle_prim_spec = Sdf.CreatePrimInLayer(layer, bicycle_prim_path)
bicycle_prim_spec.specifier = Sdf.SpecifierDef
cube_prim_path = Sdf.Path("/cube")
cube_prim_spec = Sdf.CreatePrimInLayer(layer, cube_prim_path)
cube_prim_spec.specifier = Sdf.SpecifierDef
cube_prim_spec.typeName = "Cube"
bicycle_prim_spec.specializesList.appendedItems = [cube_prim_path]
#// ANCHOR_END: compositionArcSpecialize

#// ANCHOR: listEditableOpsLowLevelAPI
from pxr import Sdf
path_list_op = Sdf.PathListOp()
# There are multiple sub-lists, which are just normal Python lists.
# 'prependedItems', 'appendedItems', 'deletedItems', 'explicitItems',
# Legacy sub-lists (do not use these anymore): 'addedItems', 'orderedItems'
# Currently the way these are exposed to Python, you have to re-assign the list, instead of editing it in place.
# So this won't work:
path_list_op.prependedItems.append(Sdf.Path("/cube"))
path_list_op.appendedItems.append(Sdf.Path("/sphere"))
# Instead do this:
path_list_op.prependedItems = [Sdf.Path("/cube")]
path_list_op.appendedItems = [Sdf.Path("/sphere")]
# To clear the list op:
print(path_list_op) # Returns: SdfPathListOp(Prepended Items: [/cube], Appended Items: [/sphere])
path_list_op.Clear()
print(path_list_op) # Returns: SdfPathListOp()
# Repopulate via constructor
path_list_op = Sdf.PathListOp.Create(prependedItems = [Sdf.Path("/cube")], appendedItems = [Sdf.Path("/sphere")])
print(path_list_op) # Returns: SdfPathListOp(Prepended Items: [/cube], Appended Items: [/sphere])
# Add remove items
path_list_op.deletedItems = [Sdf.Path("/sphere")]
print(path_list_op) # Returns: SdfPathListOp(Deleted Items: [/sphere], Prepended Items: [/cube], Appended Items: [/sphere])
# Notice how it just stores lists, it doesn't actually apply them. We'll have a look at that next.
#// ANCHOR_END: listEditableOpsLowLevelAPI

#// ANCHOR: listEditableOpsHighLevelAPI
# For example when editing a relationship:
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
yard_prim = stage.DefinePrim("/yard")
car_prim = stage.DefinePrim("/car")
rel = car_prim.CreateRelationship("locationsOfInterest")
rel.AddTarget(yard_prim.GetPath(), position=Usd.ListPositionFrontOfAppendList)
# Result:
"""
def "car"
{
    custom rel locationsOfInterest
    append rel locationsOfInterest = </yard>
}
"""
# The "Set<Function>" signatures write an explicit list:
rel.SetTargets([yard_prim.GetPath()])
# Result:
"""
def "car"
{
    custom rel locationsOfInterest = </yard>
}
"""
#// ANCHOR_END: listEditableOpsHighLevelAPI

#// ANCHOR: listEditableOpsMerging
from pxr import Sdf
### Merging basics ###
path_list_op_layer_top = Sdf.PathListOp.Create(deletedItems = [Sdf.Path("/cube")])
path_list_op_layer_middle = Sdf.PathListOp.Create(prependedItems = [Sdf.Path("/disc"), Sdf.Path("/cone")])
path_list_op_layer_bottom = Sdf.PathListOp.Create(prependedItems = [Sdf.Path("/cube")], appendedItems = [Sdf.Path("/cone"),Sdf.Path("/sphere")])

result = Sdf.PathListOp()
result = result.ApplyOperations(path_list_op_layer_top)
result = result.ApplyOperations(path_list_op_layer_middle)
result = result.ApplyOperations(path_list_op_layer_bottom)
# Notice how on merge it makes sure that each sublist does not have the values of the other sublists, just like a Python set()
print(result) # Returns: SdfPathListOp(Deleted Items: [/cube], Prepended Items: [/disc, /cone], Appended Items: [/sphere])
# Get the flattened result. This does not apply the deleteItems, only ApplyOperations does that. 
print(result.GetAddedOrExplicitItems()) # Returns: [Sdf.Path('/disc'), Sdf.Path('/cone'), Sdf.Path('/sphere')]

### Deleted and added items ###
path_list_op_layer_top = Sdf.PathListOp.Create(appendedItems=[Sdf.Path("/disc"), Sdf.Path("/cube")])
path_list_op_layer_middle = Sdf.PathListOp.Create(deletedItems = [Sdf.Path("/cube")])
path_list_op_layer_bottom = Sdf.PathListOp.Create(prependedItems = [Sdf.Path("/cube")], appendedItems = [Sdf.Path("/sphere")])

result = Sdf.PathListOp()
result = result.ApplyOperations(path_list_op_layer_top)
result = result.ApplyOperations(path_list_op_layer_middle)
result = result.ApplyOperations(path_list_op_layer_bottom)
print(result) # Returns: SdfPathListOp(Appended Items: [/sphere, /disc, /cube])
# Since it now was in the explicit list, it got removed.

### Explicit mode ###
# There is also an "explicit" mode. This clears all previous values on merge and marks the list as explicit.
# Once explicit and can't be un-explicited. An explicit list is like a reset, it 
# doesn't know anything about the previous values anymore. All lists that are merged
# after combine the result to be explicit.
path_list_op_layer_top = Sdf.PathListOp.Create(deletedItems = [Sdf.Path("/cube")])
path_list_op_layer_middle = Sdf.PathListOp.CreateExplicit([Sdf.Path("/disc")])
path_list_op_layer_bottom = Sdf.PathListOp.Create(prependedItems = [Sdf.Path("/cube")], appendedItems = [Sdf.Path("/sphere")])

result = Sdf.PathListOp()
result = result.ApplyOperations(path_list_op_layer_top)
result = result.ApplyOperations(path_list_op_layer_middle)
result = result.ApplyOperations(path_list_op_layer_bottom)
print(result, result.isExplicit) # Returns: SdfPathListOp(Explicit Items: [/disc]), True
# Notice how the deletedItems had no effect, as "/cube" is not in the explicit list.

path_list_op_layer_top = Sdf.PathListOp.Create(deletedItems = [Sdf.Path("/cube")])
path_list_op_layer_middle = Sdf.PathListOp.CreateExplicit([Sdf.Path("/disc"), Sdf.Path("/cube")])
path_list_op_layer_bottom = Sdf.PathListOp.Create(prependedItems = [Sdf.Path("/cube")], appendedItems = [Sdf.Path("/sphere")])

result = Sdf.PathListOp()
result = result.ApplyOperations(path_list_op_layer_top)
result = result.ApplyOperations(path_list_op_layer_middle)
result = result.ApplyOperations(path_list_op_layer_bottom)
print(result, result.isExplicit) # Returns: SdfPathListOp(Explicit Items: [/disc]), True
# Since it now was in the explicit list, it got removed.
#// ANCHOR_END: listEditableOpsMerging

#// ANCHOR: pcpPrimPropertyStack
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
attr = prim.CreateAttribute("debug", Sdf.ValueTypeNames.Float)
attr.Set(5, 10)
# Print the stack (set of layers that contribute data to this prim)
# For prims this returns all the Sdf.PrimSpec objects that contribute to the prim.
print(prim.GetPrimStack()) # Returns: [Sdf.Find('anon:0x7f6e590dc300:exampleTopLayer', '/cube'), 
                           #           Sdf.Find('anon:0x7f6e590dc580:exampleBottomLayer', '/cube')]
# For attributes this returns all the Sdf.AttributeSpec objects that contribute to the attribute.
# If we pass a non default time code value clips will be included in the result.
# This type of function signature is very unique and can't be found anywhere else in USD.
time_code = Usd.TimeCode.Default()
print(attr.GetPropertyStack(1001)) # Returns: [Sdf.Find('anon:0x7f9eade0ae00:exampleBottomLayer', '/cube.debug')]
print(attr.GetPropertyStack(time_code)) # Returns: [Sdf.Find('anon:0x7f9eade0ae00:exampleBottomLayer', '/cube.debug')]
#// ANCHOR_END: pcpPrimPropertyStack


#// ANCHOR: pcpPrimIndex
import os
from subprocess import call
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
# Spawn temp layer
reference_layer = Sdf.Layer.CreateAnonymous("ReferenceExample")
reference_bicycle_prim_path = Sdf.Path("/bicycle")
reference_bicycle_prim_spec = Sdf.CreatePrimInLayer(reference_layer, reference_bicycle_prim_path)
reference_bicycle_prim_spec.specifier = Sdf.SpecifierDef
reference_bicycle_prim_spec.typeName = "Cube"
reference_layer_offset = Sdf.LayerOffset(offset=10, scale=1)
reference = Sdf.Reference(reference_layer.identifier, reference_bicycle_prim_path, reference_layer_offset)
bicycle_prim_path = Sdf.Path("/red_bicycle")
bicycle_prim = stage.DefinePrim(bicycle_prim_path)
references_api = bicycle_prim.GetReferences()
references_api.AddReference(reference, position=Usd.ListPositionFrontOfAppendList)
# You'll always want to use the expanded method,
# otherwise you might miss some data sources!
# This is also what the UIs use.
prim = bicycle_prim
print(prim.GetPrimIndex()) 
print(prim.ComputeExpandedPrimIndex())
# Dump the index representation to the dot format and render it to a .svg/.png image.
prim_index = prim.ComputeExpandedPrimIndex()
print(prim_index.DumpToString())
graph_file_path = os.path.expanduser("~/Desktop/usdSurvivalGuide_prim_index.txt")
graph_viz_png_file_path = graph_file_path.replace(".txt", ".png")
graph_viz_svg_file_path = graph_file_path.replace(".txt", ".svg")
prim_index.DumpToDotGraph(graph_file_path, includeMaps=False)
call(["dot", "-Tpng", graph_file_path, "-o", graph_viz_png_file_path])
call(["dot", "-Tsvg", graph_file_path, "-o", graph_viz_svg_file_path])

def iterator_child_nodes(root_node):
    yield root_node
    for child_node in root_node.children:
        for child_child_node in iterator_child_nodes(child_node):
            yield child_child_node

def iterator_parent_nodes(root_node):
    iter_node = root_node
    while iter_node:
        yield iter_node
        iter_node = iter_node.parent
            
print("Pcp Node Refs", dir(prim_index.rootNode))
for child in list(iterator_child_nodes(prim_index.rootNode))[::1]:
    print(child, child.arcType, child.path, child.mapToRoot.MapSourceToTarget(child.path))
""" The arc type will one one of:
Pcp.ArcTypeRoot
Pcp.ArcTypeInherit
Pcp.ArcTypeVariant
Pcp.ArcTypeReference
Pcp.ArcTypeRelocate
Pcp.ArcTypePayload
Pcp.ArcTypeSpecialize
"""
#// ANCHOR_END: pcpPrimIndex

#// ANCHOR: pcpPrimCompositionQuery
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
prim = stage.DefinePrim("/pig")
refs_API = prim.GetReferences()
refs_API.AddReference("/opt/hfs19.5/houdini/usd/assets/pig/pig.usd")
print("----")
def _repr(arc):
    print(arc.GetArcType(), 
          "| Introducing Prim Path", arc.GetIntroducingPrimPath() or "-",
          "| Introducing Layer", arc.GetIntroducingLayer() or "-",
          "| Is ancestral", arc.IsAncestral(),
          "| In Root Layer Stack", arc.IsIntroducedInRootLayerStack())
print(">-> Direct Root Layer Arcs")
query = Usd.PrimCompositionQuery.GetDirectRootLayerArcs(prim)
for arc in query.GetCompositionArcs():
    _repr(arc)
print(">-> Direct Inherits")
query = Usd.PrimCompositionQuery.GetDirectInherits(prim)
for arc in query.GetCompositionArcs():
    _repr(arc)
print(">-> Direct References")
query = Usd.PrimCompositionQuery.GetDirectReferences(prim)
for arc in query.GetCompositionArcs():
    _repr(arc)
"""Returns:
>-> Direct Root Layer Arcs
Pcp.ArcTypeRoot | Introducing Prim Path - | Introducing Layer - | Is ancestral False | In Root Layer Stack True
Pcp.ArcTypeReference | Introducing Prim Path /pig | Introducing Layer Sdf.Find('anon:0x7f9b60d56b00:tmp.usda') | Is ancestral False | In Root Layer Stack True
>-> Direct Inherits
Pcp.ArcTypeInherit | Introducing Prim Path /pig | Introducing Layer Sdf.Find('/opt/hfs19.5/houdini/usd/assets/pig/pig.usd') | Is ancestral False | In Root Layer Stack False
Pcp.ArcTypeInherit | Introducing Prim Path /pig | Introducing Layer Sdf.Find('/opt/hfs19.5/houdini/usd/assets/pig/pig.usd') | Is ancestral False | In Root Layer Stack False
>-> Direct References
Pcp.ArcTypeReference | Introducing Prim Path /pig | Introducing Layer Sdf.Find('anon:0x7f9b60d56b00:tmp.usda') | Is ancestral False | In Root Layer Stack True
Pcp.ArcTypeReference | Introducing Prim Path /pig | Introducing Layer Sdf.Find('/opt/hfs19.5/houdini/usd/assets/pig/payload.usdc') | Is ancestral False | In Root Layer Stack False
Pcp.ArcTypeReference | Introducing Prim Path /pig{geo=medium} | Introducing Layer Sdf.Find('/opt/hfs19.5/houdini/usd/assets/pig/mtl.usdc') | Is ancestral False | In Root Layer Stack False
Pcp.ArcTypeReference | Introducing Prim Path /ASSET_geo_variant_1/ASSET | Introducing Layer Sdf.Find('/opt/hfs19.5/houdini/usd/assets/pig/mtl.usdc') | Is ancestral False | In Root Layer Stack False
Pcp.ArcTypeReference | Introducing Prim Path /pig | Introducing Layer Sdf.Find('/opt/hfs19.5/houdini/usd/assets/pig/payload.usdc') | Is ancestral False | In Root Layer Stack False
Pcp.ArcTypeReference | Introducing Prim Path /pig | Introducing Layer Sdf.Find('/opt/hfs19.5/houdini/usd/assets/pig/geo.usdc') | Is ancestral False | In Root Layer Stack False
Pcp.ArcTypeReference | Introducing Prim Path /pig | Introducing Layer Sdf.Find('/opt/hfs19.5/houdini/usd/assets/pig/geo.usdc') | Is ancestral False | In Root Layer Stack False
Pcp.ArcTypeReference | Introducing Prim Path /pig | Introducing Layer Sdf.Find('/opt/hfs19.5/houdini/usd/assets/pig/geo.usdc') | Is ancestral False | In Root Layer Stack False
"""
# Custom filter
# For example let's get all direct payloads, that were not introduced in the active root layer stack.
query_filter = Usd.PrimCompositionQuery.Filter()
query_filter.arcTypeFilter = Usd.PrimCompositionQuery.ArcTypeFilter.Payload
query_filter.dependencyTypeFilter = Usd.PrimCompositionQuery.DependencyTypeFilter.Direct
query_filter.arcIntroducedFilter = Usd.PrimCompositionQuery.ArcIntroducedFilter.All
query_filter.hasSpecsFilter = Usd.PrimCompositionQuery.HasSpecsFilter.HasSpecs
print(">-> Custom Query (Direct payloads not in root layer that have specs)")
query = Usd.PrimCompositionQuery(prim)
query.filter = query_filter
for arc in query.GetCompositionArcs():
    _repr(arc)
"""Returns:
>-> Custom Query (Direct payloads not in root layer that have specs)
Pcp.ArcTypePayload | Introducing Prim Path /pig | Introducing Layer Sdf.Find('/opt/hfs19.5/houdini/usd/assets/pig/pig.usd') | Is ancestral False | In Root Layer Stack False
"""
#// ANCHOR_END: pcpPrimCompositionQuery
