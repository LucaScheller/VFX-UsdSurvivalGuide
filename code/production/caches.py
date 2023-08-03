#// ANCHOR: stageQueryAttribute
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
prim = stage.DefinePrim(Sdf.Path("/cube"), "Cube")

size_attr = prim.GetAttribute("size")
for frame in range(10000):
    size_attr.Set(frame, frame)

attr_query = Usd.AttributeQuery(prim, "size")
print(attr_query.Get(1001)) # Returns 2.0

from pxr import Tf
# Attribute
sw = Tf.Stopwatch()
sw.Start()
for frame in range(10000):
    size_attr.Get(frame)
sw.Stop()
print(sw.milliseconds) # Returns: 14
sw.Reset()
# Attribute Query
sw = Tf.Stopwatch()
sw.Start()
for frame in range(10000):
    attr_query.Get(frame)
sw.Stop()
print(sw.milliseconds) # Returns: 7
sw.Reset()
#// ANCHOR_END: stageQueryAttribute

#// ANCHOR: stageQueryInheritedPrimvars
from pxr import Sdf, Usd, UsdGeom
stage = Usd.Stage.CreateInMemory()
bicycle_prim = stage.DefinePrim(Sdf.Path("/set/garage/bicycle"), "Cube")
car_prim = stage.DefinePrim(Sdf.Path("/set/garage/car"), "Cube")
set_prim = stage.GetPrimAtPath("/set")
garage_prim = stage.GetPrimAtPath("/set/garage")
tractor_prim = stage.DefinePrim(Sdf.Path("/set/yard/tractor"), "Cube")
"""Hierarchy
/set
/set/garage
/set/garage/bicycle
/set/garage/car
/set/yard
/set/yard/tractor
"""

# Setup hierarchy primvars
primvar_api = UsdGeom.PrimvarsAPI(set_prim)
size_primvar = primvar_api.CreatePrimvar("size", Sdf.ValueTypeNames.Float)
size_primvar.Set(10)
primvar_api = UsdGeom.PrimvarsAPI(garage_prim)
size_primvar = primvar_api.CreatePrimvar("size", Sdf.ValueTypeNames.Float)
size_primvar.Set(5)
size_primvar = primvar_api.CreatePrimvar("point_scale", Sdf.ValueTypeNames.Float)
size_primvar.Set(9000)
primvar_api = UsdGeom.PrimvarsAPI(bicycle_prim)
size_primvar = primvar_api.CreatePrimvar("size", Sdf.ValueTypeNames.Float)
size_primvar.Set(2.5)

# High performance primvar check with our own cache
primvar_stack = [{}]
iterator = iter(Usd.PrimRange.PreAndPostVisit(stage.GetPseudoRoot()))
for prim in iterator:
    primvar_api = UsdGeom.PrimvarsAPI(prim)
    if not iterator.IsPostVisit():
        before_hash = hex(id(primvar_stack[-1]))
        parent_primvars = primvar_stack[-1]
        authored_primvars = {p.GetPrimvarName(): p for p in primvar_api.GetPrimvarsWithAuthoredValues()} 
        if authored_primvars and parent_primvars:
            combined_primvars = {name: p for name, p in parent_primvars.items()}
            combined_primvars.update(authored_primvars)
            primvar_stack.append(combined_primvars)
        elif authored_primvars:
            primvar_stack.append(authored_primvars)
        else:
            primvar_stack.append(parent_primvars)
        after_hash = hex(id(primvar_stack[-1]))
        print(before_hash, after_hash, prim.GetPath(), [p.GetAttr().GetPath().pathString for p in primvar_stack[-1].values()], len(primvar_stack))
    else:
        primvar_stack.pop(-1)
# Returns:
"""
0x7fea12b349c0 0x7fea12b349c0 / [] 2
0x7fea12b349c0 0x7fea12b349c0 /HoudiniLayerInfo [] 3
0x7fea12b349c0 0x7fea12bfe980 /set ['/set.primvars:size'] 3
0x7fea12bfe980 0x7fea12a89600 /set/garage ['/set/garage.primvars:size', '/set/garage.primvars:point_scale'] 4
0x7fea12a89600 0x7fea367b87c0 /set/garage/bicycle ['/set/garage/bicycle.primvars:size', '/set/garage.primvars:point_scale'] 5
0x7fea12a89600 0x7fea12a89600 /set/garage/car ['/set/garage.primvars:size', '/set/garage.primvars:point_scale'] 5
0x7fea12bfe980 0x7fea12bfe980 /set/yard ['/set.primvars:size'] 4
0x7fea12bfe980 0x7fea12bfe980 /set/yard/tractor ['/set.primvars:size'] 5
"""
#// ANCHOR_END: stageQueryInheritedPrimvars

#// ANCHOR: stageQueryMaterialBinding
from pxr import Sdf, Usd, UsdGeom, UsdShade
stage = Usd.Stage.CreateInMemory()
# Leaf prims
cube_prim = stage.DefinePrim(Sdf.Path("/root/RENDER/pointy/cube"), "Cube")
sphere_prim = stage.DefinePrim(Sdf.Path("/root/RENDER/round_grp/sphere"), "Sphere")
cylinder_prim = stage.DefinePrim(Sdf.Path("/root/RENDER/round_grp/cylinder"), "Cylinder")
round_grp_prim = sphere_prim.GetParent()
material_prim = stage.DefinePrim(Sdf.Path("/root/MATERIALS/example_material"), "Material")
# Parent prims
for prim in stage.Traverse():
    if prim.GetName() not in ("cube", "sphere", "cylinder", "example_material"):
        prim.SetTypeName("Xform")

# Bind materials via direct binding
material = UsdShade.Material(material_prim)
# Bind parent group
mat_bind_api = UsdShade.MaterialBindingAPI.Apply(round_grp_prim)
mat_bind_api.Bind(material)
# Bind leaf prim
mat_bind_api = UsdShade.MaterialBindingAPI.Apply(cube_prim)
mat_bind_api.Bind(material)

# Query material bindings
materials, relationships = UsdShade.MaterialBindingAPI.ComputeBoundMaterials([cube_prim, sphere_prim, cylinder_prim])
for material, relationship in zip(materials, relationships):
    print(material.GetPath(), relationship.GetPath())
"""Returns
/root/MATERIALS/example_material /root/RENDER/pointy/cube.material:binding
/root/MATERIALS/example_material /root/RENDER/round_grp.material:binding
/root/MATERIALS/example_material /root/RENDER/round_grp.material:binding
"""
#// ANCHOR_END: stageQueryMaterialBinding


#// ANCHOR: stageQueryTransform
import math
from pxr import Gf,  Sdf, Usd, UsdGeom
stage = Usd.Stage.CreateInMemory()
root_prim_path = Sdf.Path("/root")
root_prim = stage.DefinePrim(root_prim_path, "Xform")
cone_prim_path = Sdf.Path("/root/cone")
cone_prim = stage.DefinePrim(cone_prim_path, "Cone")
# Set local transform of leaf prim
cone_xformable = UsdGeom.Xformable(cone_prim)
cone_translate_op = cone_xformable.AddTranslateOp(opSuffix="upAndDown")
for frame in range(1, 100):
    cone_translate_op.Set(Gf.Vec3h([5, math.sin(frame * 0.1) * 3, 0]), frame)
# A transform is combined with its parent prims' transforms
root_xformable = UsdGeom.Xformable(root_prim)
root_rotate_op = root_xformable.AddRotateZOp(opSuffix= "spinMeRound")
for frame in range(1, 100):
    root_rotate_op.Set(frame * 15, frame)
# For single queries we can use the xformable API
print(cone_xformable.ComputeLocalToWorldTransform(Usd.TimeCode(15)))
    
## Xform Cache
# For batched queries, we should always use the xform cache, to avoid recomputing parent xforms.
# Get: 'GetTime', 'ComputeRelativeTransform', 'GetLocalToWorldTransform', 'GetLocalTransformation', 'GetParentToWorldTransform'
# Set: 'SetTime'
# Clear: 'Clear'
xform_cache = UsdGeom.XformCache(Usd.TimeCode(1))
for prim in stage.Traverse():
    print("Worldspace Transform", xform_cache.GetLocalToWorldTransform(prim))
    print("Localspace Transform", xform_cache.GetLocalTransformation(prim))
#// ANCHOR_END: stageQueryTransform


#// ANCHOR: stageQueryBBox
from pxr import Gf,  Sdf, Usd, UsdGeom, Vt
stage = Usd.Stage.CreateInMemory()
# Setup scene
root_prim_path = Sdf.Path("/root")
root_prim = stage.DefinePrim(root_prim_path, "Xform")
cone_prim_path = Sdf.Path("/root/cone")
cone_prim = stage.DefinePrim(cone_prim_path, "Cone")

root_xformable = UsdGeom.Xformable(root_prim)
root_translate_op = root_xformable.AddTranslateOp()
root_translate_op.Set(Gf.Vec3h([50, 30, 10]))
root_rotate_op = root_xformable.AddRotateZOp()
root_rotate_op.Set(45)

cone_xformable = UsdGeom.Xformable(cone_prim)
cone_translate_op = cone_xformable.AddTranslateOp()
cone_rotate_op = cone_xformable.AddRotateXYZOp()

## UsdGeom.BBoxCache()
# Get: 'GetTime', 'GetIncludedPurposes',  'GetUseExtentsHint',
# Set: 'SetTime', 'SetIncludedPurposes',
# Clear: 'Clear'

# Compute: 'ComputeWorldBound', 'ComputeLocalBound', 'ComputeRelativeBound', 'ComputeUntransformedBound', 
# Compute Instances: 'ComputePointInstanceWorldBound', 'ComputePointInstanceWorldBounds',
#                    'ComputePointInstanceLocalBound',  'ComputePointInstanceLocalBounds',
#                    'ComputePointInstanceRelativeBound', 'ComputePointInstanceRelativeBounds',
#                    'ComputePointInstanceUntransformedBounds', 'ComputePointInstanceUntransformedBound'
time_code = Usd.TimeCode(1) # Determine frame to lookup
bbox_cache = UsdGeom.BBoxCache(time_code, [UsdGeom.Tokens.default_, UsdGeom.Tokens.render],
                               useExtentsHint=False, ignoreVisibility=False)
# Useful for intersection testing:
bbox = bbox_cache.ComputeWorldBound(cone_prim)
print(bbox) # Returns: [([(-1, -1, -1)...(1, 1, 1)]) (( (0.7071067811865475, 0.7071067811865476, 0, 0), (-0.7071067811865476, 0.7071067811865475, 0, 0), (0, 0, 1, 0), (50, 30, 10, 1) )) false]
# When payloading prims, we want to write an extentsHint attribute to give a bbox hint
# We can either query it via UsdGeom.BBoxCache or for individual prims via UsdGeom.Xformable.ComputeExtentsHint
root_geom_model_API = UsdGeom.ModelAPI.Apply(root_prim)
extentsHint = root_geom_model_API.ComputeExtentsHint(bbox_cache)
root_geom_model_API.SetExtentsHint(extentsHint, time_code)
# Or
bbox = bbox_cache.ComputeUntransformedBound(root_prim)
aligned_range = bbox.ComputeAlignedRange()
extentsHint = Vt.Vec3hArray([Gf.Vec3h(list(aligned_range.GetMin())), Gf.Vec3h(list(aligned_range.GetMax()))])
root_geom_model_API.SetExtentsHint(extentsHint, time_code)
#// ANCHOR_END: stageQueryBBox