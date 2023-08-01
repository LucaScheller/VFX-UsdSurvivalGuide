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
""" This works :)
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