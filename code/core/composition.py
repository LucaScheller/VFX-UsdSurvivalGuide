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