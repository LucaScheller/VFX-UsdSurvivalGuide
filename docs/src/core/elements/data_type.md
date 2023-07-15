# Data Types



import pxr

### Value Type Names (pxr.Sdf.ValueTypeNames) ###
# Point3f
value_type_name = pxr.Sdf.ValueTypeNames.Point3fArray
## Aliases and cpp names
value_type_name.aliasesAsStrings
value_type_name.cppTypeName
value_type_name.role              # Role name like 'Color', 'Normal' 
## Array vs Scalar (Single Value)
value_type_name.isArray, value_type_name.isScalar
### Convert type between Scalar <-> Array
array_type_name = value_type_name.arrayType  # (Same as type_name in this case)
scale_type_name = value_type_name.scalarType
## Type (Actual type definiton, holds data about
# container format like 'pxr.Gf.Vec3f' (for arrays of single element))
value_type = value_type_name.type
### Get the Python Class (or default value)
cls = value_type.pythonClass
# Or
default_value = value_type_name.defaultValue
cls = default_value.__class__
### pxr.Vt.Type Registry ###
# All registered types (Wraps type objects like float, int, bool, GfVec3d
# for type_def in pxr.Tf.Type.GetRoot().derivedTypes:
#    print(type_def)
type_def = pxr.Tf.Type.FindByName(value_type_name.cppTypeName)
type_def.typeName # The same as value_type_name.cppTypeName
# Root/Base/Derived Types
type_def.GetRoot(), type_def.baseTypes, type_def.derivedTypes
# For Python usage, you will only use the array types, as they handle the auto conversion
# form buffer protocol arrays like numpy arrays, the rest is auto converted and you don't need
# to worry about it.
### pxr.Gf Graphics Foundations  ###
# Hold base types like 
pxr.Gf.Vec2f, pxr.Gf.Matrix4d