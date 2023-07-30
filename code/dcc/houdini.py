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