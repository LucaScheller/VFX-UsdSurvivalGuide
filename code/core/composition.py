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
