#// ANCHOR: houdiniCompositionInheritInstanceable
from pxr import Gf, Sdf, Usd
node = hou.pwd()
stage = node.editableStage()
pig_a_prim = stage.GetPrimAtPath(Sdf.Path("/pig_A"))
# Inspect prototype and collect what to override
prototype = pig_a_prim.GetPrototype()
# Create overrides
class_prim = stage.CreateClassPrim(Sdf.Path("/__CLASS__/pig"))
edit_prim = stage.DefinePrim(class_prim.GetPath().AppendPath("geo/shape"))
xform = Gf.Matrix4d()
xform.SetTranslate([0, 2, 0])
edit_prim.CreateAttribute("xformOpOrder", Sdf.ValueTypeNames.TokenArray).Set(["xformOp:transform:transform"])
edit_prim.CreateAttribute("xformOp:transform:transform", Sdf.ValueTypeNames.Matrix4d).Set(xform)
# Add inherits
instance_prims = prototype.GetInstances()
for instance_prim in instance_prims:
    inherits_api = instance_prim.GetInherits()
    # if instance_prim.GetName() == "pig_B":
    #     continue
    inherits_api.AddInherit(class_prim.GetPath(), position=Usd.ListPositionFrontOfAppendList)    
#// ANCHOR_END: houdiniCompositionInheritInstanceable

#// ANCHOR: houdiniTimeDependency
def GetValueMightBeTimeVarying(attribute, checkVariability=False):
    """Check if an attribute has time samples.
    Args:
        attribute (Usd.Attribute): The attribute to check.
        checkVariability (bool): Preflight check if the time variability metadata is uniform,
                                 if yes return False and don't check the value
    Returns:
        bool: The state if the attribute has time samples
    """
    if checkVariability and attribute.GetVariability() == pxr.Sdf.VariabilityUniform:
        return False
    # Get the layer stack without value clips
    property_stack = attribute.GetPropertyStack(pxr.Usd.TimeCode.Default())
    if property_stack[0].layer.anonymous:
        # It is fast to lookup data that is in memory
        return attribute.GetNumTimeSamples() > 0
    # Otherwise fallback to the default behaviour as this inspects only max two timeSamples
    return attribute.ValueMightBeTimeVarying()
#// ANCHOR_END: houdiniTimeDependency

#// ANCHOR: houdiniFrustumCulling
import numpy as np
from pxr import Gf, Sdf, Usd, UsdGeom

stage_file_path = "/path/to/your/stage"
stage = Usd.Open(stage_file_path)
# Or
import hou
stage = hou.pwd().editableStage()

camera_prim_path = Sdf.Path("/cameras/camera")
camera_prim = stage.GetPrimAtPath(camera_prim_path)
prim_paths = [Sdf.Path("/set/toys/instancer")]
time_samples = list(range(1001, 1101))

# Mode
mode = "average" # "frame" or "average"
data = {}

for time_sample in time_samples:
    time_code = Usd.TimeCode(time_sample)
    # Get frustum
    camera_type_API = UsdGeom.Camera(camera_prim)
    camera_API = camera_type_API.GetCamera(time_code)
    frustum = camera_API.frustum
    # Manually override clipping planes
    # frustum.SetNearFar(Gf.Range1d(0.01, 100000))
    # Get bbox cache
    bbox_cache = UsdGeom.BBoxCache(
        time_code,
        ["default", "render", "proxy", "guide"],
        useExtentsHint=False,
        ignoreVisibility=False
    )
    for prim_path in prim_paths:
        prim = stage.GetPrimAtPath(prim_path)
        # Skip inactive prims
        if not prim.IsActive():
            continue
        # Skip non boundable prims
        if not prim.IsA(UsdGeom.Boundable):
            conitune
        # Visibility
        imageable_type_API = UsdGeom.Imageable(prim)
        visibility_attr = imageable_type_API.GetVisibilityAttr()
        # Poininstancer Prims
        if prim.IsA(UsdGeom.PointInstancer):
            pointinstancer_type_API = UsdGeom.PointInstancer(prim)
            protoIndices_attr = pointinstancer_type_API.GetProtoIndicesAttr()
            if not protoIndices_attr.HasValue():
                continue
            protoIndices_attr_len = len(protoIndices_attr.Get(time_sample))
            bboxes = bbox_cache.ComputePointInstanceWorldBounds(
                pointinstancer_type_API, list(range(protoIndices_attr_len))
            )
            # Calculate intersections
            invisibleIds_attr_value = np.arange(protoIndices_attr_len)
            for idx, bbox in enumerate(bboxes):
                if frustum.Intersects(bbox):
                    invisibleIds_attr_value[idx] = -1
            # The invisibleIds can be written as a sparse attribute. The array length can differ
            # from the protoIndices count. If an ids attribute exists, then it will use those 
            # indices, other wise it will use the protoIndices element index. Here we don't work
            # with the ids attribute to keep the code example simple.
            invisibleIds_attr_value = invisibleIds_attr_value[invisibleIds_attr_value != -1]
            if len(invisibleIds_attr_value) == protoIndices_attr_len:
                visibility_attr_value = UsdGeom.Tokens.invisible
                invisibleIds_attr_value = []
            else:
                visibility_attr_value = UsdGeom.Tokens.inherited
                invisibleIds_attr_value = invisibleIds_attr_value
            # Apply averaged frame range value
            if mode != "frame":        
                data.setdefault(prim_path, {"visibility": [], "invisibleIds": [], "invisibleIdsCount": []})
                data[prim_path]["visibility"].append(visibility_attr_value == UsdGeom.Tokens.inherited)
                data[prim_path]["invisibleIds"].append(invisibleIds_attr_value)
                data[prim_path]["invisibleIdsCount"].append(protoIndices_attr_len)
                continue
            # Apply value per frame
            visibility_attr.Set(UsdGeom.Tokens.inherited, time_code)
            invisibleIds_attr = pointinstancer_type_API.GetInvisibleIdsAttr()
            invisibleIds_attr.Set(invisibleIds_attr_value, time_code)
        else:
            # Boundable Prims
            bbox = bbox_cache.ComputeWorldBound(prim)
            intersects = frustum.Intersects(bbox)
            # Apply averaged frame range value
            if mode != "frame":        
                data.setdefault(prim_path, {"visibility": [], "invisibleIds": []})
                data[prim_path]["visibility"].append(visibility_attr_value == UsdGeom.Tokens.inherited)
                data[prim_path]["invisibleIds"].append(invisibleIds_attr_value)
                continue
            # Apply value per frame
            visibility_attr.Set(UsdGeom.Tokens.inherited
                                if intersects else UsdGeom.Tokens.invisible, time_code)
                                
# Apply averaged result
# This won't work with changing point counts! If we want to implement this, we
# have to map the indices to the 'ids' attribute value per frame.
if mode == "average" and data:
    for prim_path, visibility_data in data.items():
        prim = stage.GetPrimAtPath(prim_path)
        imageable_type_API = UsdGeom.Imageable(prim)#
        visibility_attr = imageable_type_API.GetVisibilityAttr()
        visibility_attr.Block()
        # Pointinstancer Prims
        if visibility_data.get("invisibleIds"):
            pointinstancer_type_API = UsdGeom.PointInstancer(prim)
            invisibleIds_average = set(np.arange(max(visibility_data['invisibleIdsCount'])))
            for invisibleIds in visibility_data.get("invisibleIds"):
                invisibleIds_average = invisibleIds_average.intersection(invisibleIds)
            invisibleIds_attr = pointinstancer_type_API.GetInvisibleIdsAttr()
            invisibleIds_attr.Set(np.array(sorted(invisibleIds_average)), time_code)
            continue
        # Boundable Prims
        prim = stage.GetPrimAtPath(prim_path)
        imageable_type_API = UsdGeom.Imageable(prim)
        visibility_attr = imageable_type_API.GetVisibilityAttr()
        visibility_attr.Block()
        visibility_attr.Set(UsdGeom.Tokens.inherited if any(visibility_data["visibility"]) else UsdGeom.Tokens.invisible)
#// ANCHOR_END: houdiniFrustumCulling

#// ANCHOR: houdiniPointsNativeStream
import numpy as np
from pxr import UsdGeom
sop_node = node.parm("spare_input0").evalAsNode()
sop_geo = sop_node.geometry()

frame = hou.frame()

prim = stage.DefinePrim("/points", "Points")
attribute_mapping = {
    "P": "points",
    "id": "ids",
    "pscale": "widths",
    "Cd": "primvars:displayColor",
}
# Import attributes
for sop_attr in sop_geo.pointAttribs():
    attr_name = attribute_mapping.get(sop_attr.name())
    if not attr_name:
        continue
    attr = prim.GetAttribute(attr_name)
    if not attr:
        continue
    attr_type_name = attr.GetTypeName()
    attr_type = attr_type_name.type
    attr_class = attr_type.pythonClass
    # The pointFloatAttribValuesAsString always gives us a float array
    value = np.frombuffer(sop_geo.pointFloatAttribValuesAsString(sop_attr.name()), dtype=np.float32)
    # This casts it back to its correct type
    attr.Set(attr_class.FromNumpy(value), frame)
    # Enforce "vertex" (Houdini speak "Point") interpolation
    attr.SetMetadata("interpolation", "vertex")
# Re-Compute extent hints
boundable_api = UsdGeom.Boundable(prim)
extent_attr = boundable_api.GetExtentAttr()
extent_value = UsdGeom.Boundable.ComputeExtentFromPlugins(boundable_api, frame)
if extent_value:
    extent_attr.Set(extent_value, frame)
#// ANCHOR_END: houdiniPointsNativeStream

#// ANCHOR: houdiniPointInstancerReorderTracker
import pxr
node = hou.pwd()
layer = node.editableLayer()

ref_node = node.parm("spare_input0").evalAsNode()
ref_stage = ref_node.stage()

with pxr.Sdf.ChangeBlock():
    for prim in ref_stage.TraverseAll():
        prim_path = prim.GetPath()
        if prim.IsA(pxr.UsdGeom.PointInstancer):
            prim_spec = layer.GetPrimAtPath(prim_path)
            # Attrs
            prototypes = prim.GetRelationship(pxr.UsdGeom.Tokens.prototypes)
            protoIndices_attr = prim.GetAttribute(pxr.UsdGeom.Tokens.protoIndices)
            if not protoIndices_attr:
                continue
            if not protoIndices_attr.HasValue():
                continue
            protoTracker_attr_spec = pxr.Sdf.AttributeSpec(prim_spec, "protoTracker", pxr.Sdf.ValueTypeNames.StringArray)
            layer.SetTimeSample(protoTracker_attr_spec.path, hou.frame(), [p.pathString for p in prototypes.GetForwardedTargets()])
#// ANCHOR_END: houdiniPointInstancerReorderTracker

#// ANCHOR: houdiniPointInstancerReorderPostProcess
import pxr
import numpy as np
node = hou.pwd()
layer = node.editableLayer()


layers = [layer]

def pointinstancer_prototypes_reorder(layers):
    """Rearrange the prototypes to be the actual value that they were written with
    based on the 'protoTracker' attribute.
    We need to do this because relationship attributes can't be animated,
    which causes instancers with varying prototypes per frame to output wrong
    prototypes once the scene is cached over the whole frame range.
    
    This assumes that the 'protoTracker' attribute has been written with the same
    time sample count as the 'protoIndices' attribute. They will be matched by time
    sample index.

    Args:
        layers (list): A list of pxr.Sdf.Layer objects that should be validated.
                       It is up to the caller to call the layer.Save() command to
                       commit the actual results of this function.
                       
    """
    
    # Constants
    protoTracker_attr_name = "protoTracker"
    
    # Collect all point instancer prototypes
    instancer_prototype_mapping = {}

    def collect_data_layer_traverse(path):
        if not path.IsPrimPropertyPath():
            return
        if path.name != protoTracker_attr_name:
            return
        instancer_prim_path = path.GetPrimPath()
        instancer_prototype_mapping.setdefault(instancer_prim_path, set())
        time_samples = layer.ListTimeSamplesForPath(path)
        if time_samples:
            for timeSample in layer.ListTimeSamplesForPath(path):
                prototype_prim_paths = layer.QueryTimeSample(path, timeSample)
                instancer_prototype_mapping[instancer_prim_path].update(prototype_prim_paths)
    
    for layer in layers:
        layer.Traverse(layer.pseudoRoot.path, collect_data_layer_traverse)
    # Exit if not valid instancers were found
    if not instancer_prototype_mapping:
        return
    # Combine prototype mapping data
    for k, v in instancer_prototype_mapping.items():
        instancer_prototype_mapping[k] = sorted(v)
    # Apply combined targets
    for layer in layers:
        for instancer_prim_path, prototypes_prim_path_strs in instancer_prototype_mapping.items():
            instancer_prim_spec = layer.GetPrimAtPath(instancer_prim_path)
            if not instancer_prim_spec:
                continue
            protoTracker_attr_spec = layer.GetPropertyAtPath(
                instancer_prim_path.AppendProperty(protoTracker_attr_name)
            )
            if not protoTracker_attr_spec:
                continue
            protoIndices_attr_spec = layer.GetPropertyAtPath(
                instancer_prim_path.AppendProperty(pxr.UsdGeom.Tokens.protoIndices)
            )
            if not protoIndices_attr_spec:
                continue
            prototypes_rel_spec = layer.GetRelationshipAtPath(
                instancer_prim_path.AppendProperty(pxr.UsdGeom.Tokens.prototypes)
            )
            if not prototypes_rel_spec:
                continue
            # Update prototypes
            prototypes_prim_paths = [pxr.Sdf.Path(p) for p in prototypes_prim_path_strs]
            prototypes_rel_spec.targetPathList.ClearEdits()
            prototypes_rel_spec.targetPathList.explicitItems = prototypes_prim_paths
            
            # Here we just match the time sample by index, not by actual values
            # as some times there are floating precision errors when time sample keys are written.
            protoIndices_attr_spec_time_samples = layer.ListTimeSamplesForPath(
                protoIndices_attr_spec.path
            )
            # Update protoIndices
            for protoTracker_time_sample_idx, protoTracker_time_sample in enumerate(
                layer.ListTimeSamplesForPath(protoTracker_attr_spec.path)
            ):
                # Reorder protoIndices
                protoTracker_prim_paths = list(
                    layer.QueryTimeSample(
                        protoTracker_attr_spec.path,
                        protoTracker_time_sample,
                    )
                )
                # Skip if order already matches
                if prototypes_prim_paths == protoTracker_prim_paths:
                    continue

                prototype_order_mapping = {}
                for protoTracker_idx, protoTracker_prim_path in enumerate(protoTracker_prim_paths):
                    prototype_order_mapping[protoTracker_idx] = prototypes_prim_paths.index(
                        protoTracker_prim_path
                    )
                # Re-order protoIndices via numpy (Remapping via native Python is slow).
                source_value = np.array(
                    layer.QueryTimeSample(
                        protoIndices_attr_spec.path,
                        protoIndices_attr_spec_time_samples[protoTracker_time_sample_idx],
                    ),
                    dtype=int,
                )
                destination_value = np.copy(source_value)
                for k in sorted(prototype_order_mapping.keys(), reverse=True):
                    destination_value[source_value == k] = prototype_order_mapping[k]
                layer.SetTimeSample(
                    protoIndices_attr_spec.path,
                    protoIndices_attr_spec_time_samples[protoTracker_time_sample_idx],
                    destination_value,
                )
                # Force deallocate
                del source_value
                del destination_value
                # Update protoTracker attribute to reflect changes, allowing
                # this function to be run multiple times.
                layer.SetTimeSample(
                    protoTracker_attr_spec.path,
                    protoTracker_time_sample,
                    pxr.Vt.StringArray(prototypes_prim_path_strs),
                )

pointinstancer_prototypes_reorder(layers)
#// ANCHOR_END: houdiniPointInstancerReorderPostProcess

#// ANCHOR: houdiniPointInstancerNativeStream
import pxr
node = hou.pwd()
layer = node.editableLayer()

ref_node = node.parm("spare_input0").evalAsNode()
ref_stage = ref_node.stage()

time_code = pxr.Usd.TimeCode.Default() if not ref_node.isTimeDependent() else pxr.Usd.TimeCode(hou.frame())

with pxr.Sdf.ChangeBlock():
    edit = pxr.Sdf.BatchNamespaceEdit()
    for prim in ref_stage.TraverseAll():
        prim_path = prim.GetPath()
        if prim.IsA(pxr.UsdGeom.Points):
            prim_spec = layer.GetPrimAtPath(prim_path)
            # Prim
            prim_spec.typeName = "PointInstancer"
            purpose_attr_spec = pxr.Sdf.AttributeSpec(prim_spec, pxr.UsdGeom.Tokens.purpose, pxr.Sdf.ValueTypeNames.Token)
            # Rels
            protoTracker_attr = prim.GetAttribute("protoTracker")
            protoHash_attr = prim.GetAttribute("protoHash")
            if protoTracker_attr and protoTracker_attr.HasValue():
                protoTracker_prim_paths = [pxr.Sdf.Path(p) for p in protoTracker_attr.Get(time_code)]
                prototypes_rel_spec = pxr.Sdf.RelationshipSpec(prim_spec, pxr.UsdGeom.Tokens.prototypes)
                prototypes_rel_spec.targetPathList.explicitItems = protoTracker_prim_paths
                # Cleanup
                edit.Add(prim_path.AppendProperty("protoTracker:indices"), pxr.Sdf.Path.emptyPath)
                edit.Add(prim_path.AppendProperty("protoTracker:lengths"), pxr.Sdf.Path.emptyPath)
            elif protoHash_attr and protoHash_attr.HasValue():
                protoHash_pairs = [i.split("|") for i in protoHash_attr.Get(time_code)]
                protoTracker_prim_paths = [pxr.Sdf.Path(v) for k, v in protoHash_pairs if k == prim_path]
                prototypes_rel_spec = pxr.Sdf.RelationshipSpec(prim_spec, pxr.UsdGeom.Tokens.prototypes)
                prototypes_rel_spec.targetPathList.explicitItems = protoTracker_prim_paths
                protoTracker_attr_spec = pxr.Sdf.AttributeSpec(prim_spec, "protoTracker", pxr.Sdf.ValueTypeNames.StringArray)
                layer.SetTimeSample(protoTracker_attr_spec.path, hou.frame(), [p.pathString for p in protoTracker_prim_paths])
                # Cleanup
                edit.Add(prim_path.AppendProperty("protoHash"), pxr.Sdf.Path.emptyPath)
                edit.Add(prim_path.AppendProperty("protoHash:indices"), pxr.Sdf.Path.emptyPath)
                edit.Add(prim_path.AppendProperty("protoHash:lengths"), pxr.Sdf.Path.emptyPath)
            # Children
            Prototypes_prim_spec = pxr.Sdf.CreatePrimInLayer(layer, prim_path.AppendChild("Prototypes"))
            Prototypes_prim_spec.typeName = "Scope"
            Prototypes_prim_spec.specifier = pxr.Sdf.SpecifierDef
            
            # Rename
            edit.Add(prim_path.AppendProperty(pxr.UsdGeom.Tokens.points),
                     prim_path.AppendProperty(pxr.UsdGeom.Tokens.positions))

    if not layer.Apply(edit):
        raise Exception("Failed to modify layer!")
#// ANCHOR: houdiniPointInstancerNativeStream