# Data Types/Roles

# Table of contents
1. [Data Types/Roles In-A-Nutshell](#summary)
1. [What should I use it for?](#usage)
1. [Resources](#resources)
1. [Overview](#overview)
    1. [Data Types](#dataTypes)
    1. [Data Roles](#dataRoles)

## TL;DR - Metadata In-A-Nutshell <a name="summary"></a>
When reading and writing data in USD, all data is of a specific data type. USD extends the standard base types (`float`, `int`) with computer graphics related classes (e.g. `Gf.Matrix3d`, `Gf.Vec3h`) that make it easy to perform common 3d math operations and Usd related types (e.g. `Sdf.Asset`). To give a hint about how a data type should be used, we also have the concept of data roles (`Position`, `Normal`, `Color`). All data value type names are stored in the `Sdf.ValueTypeNames` registry, from these we can get the base classes stored in `Gf` (math related classes), `Sdf`(USD related classes) and `Vt` (array classes that carry `Gf` data types).

~~~admonish tip title="Pro Tip | Creating arrays"
The constructors for arrays allow us to input tuples/lists instead of the explicit base classes.
```python
# Explicit
pxr.Vt.Vec3dArray([Gf.Vec3d(1,2,3)])
# Implicit
pxr.Vt.Vec3dArray([(1,2,3)])
```
Instead of searching for the corresponding `Gf` or `Vt` array class, we can get it from the type name and instantiate it:
```python
vec3h_array = Sdf.ValueTypeNames.Point3hArray.type.pythonClass([(0,1,2)])
# Or: Usd.Attribute.GetTypeName().type.pythonClass([(0,1,2)]) / Sdf.AttributeSpec.typeName.type.pythonClass([(0,1,2)])
print(type(vec3h_array)) # Returns: <class 'pxr.Vt.Vec3hArray'>
```
As `Vt.Array` support the buffer protocol, we can map the arrays to numpy without data duplication and perform high performance 
value editing.
```python
from pxr import Vt
import numpy as np
from array import array
# Python Arrays
vt_array = Vt.Vec3hArray.FromBuffer(array("f", [1,2,3])) # Returns: Vt.Vec3hArray(1, (Gf.Vec3h(1.0, 2.0, 3.0),))
# From Numpy Arrays 
Vt.Vec3hArray.FromNumpy(np.ones((10, 3)))
Vt.Vec3hArray.FromBuffer(np.ones((10, 3)))
# To Numpy arrays
np.array(vt_array)
```
~~~

## What should I use it for? <a name="usage"></a>
~~~admonish tip
When creating attributes we always have to specify a `Sdf.ValueTypeName`, which defines the data type & role.
USD ships with great computer graphics related classes in the `Gf` module, which we can use for calculations.
The `Vt.Array` wrapper around the `Gf` data base classes implements the buffer protocol, so we can easily map these arrays to Numpy arrays and perform high performance value edits. This is great for adjusting geometry related attributes.
~~~

## Resources <a name="resources"></a>
- [USD API Data Type Docs](https://openusd.org/dev/api/_usd__page__datatypes.html)
- [Nvidia USD Data Types Docs](https://docs.omniverse.nvidia.com/dev-guide/latest/dev_usd/quick-start/usd-types.html)

## Overview <a name="overview"></a>
When reading and writing data in USD, all data is of a specific data type. USD extends the standard base types (`float`, `int`) with computer graphics related classes (`Gf.Matrix3d`, `Gf.Vec3h`) that make it easy to perform common 3d math operations. To give a hint about how a data type should be used, we also have the concept of data roles.

### Data Types <a name="dataTypes"></a>
Let's first talk about data types. These are the base data classes all data is USD is stored in.

To access the base data classes there are three modules:
- `Sdf`(Scene Description Foundations): Here you'll 99% of the time only be using `Sdf.AssetPath`, `Sdf.AssetPathArray` and the [list editable ops](../composition/listeditableops.md) that have the naming convention `<Type>ListOp` e.g. `Sdf.PathListOp`, `Sdf.ReferenceListOp`, `Sdf.ReferenceListOp`, `PayloadListOp`, `StringListOp`, `TokenListOp`
- `Gf`(Graphics Foundations): The `Gf` module is basically USD's math module. Here we have all the math related data classes that are made up of the base types (base types being `float`, `int`, `double`, etc.). Commonly used classes/types are `Gf.Matrix4d`, `Gf.Quath`(Quaternions), `Gf.Vec2f`, `Gf.Vec3f`, `Gf.Vec4f`. Most classes are available in different precisions, noted by the suffix `h`(half),`f`(float), `d`(double).
- `Vt` (Value Types): Here we can find all the `Array` (list) classes that capture the base classes from the `Gf` module in arrays. For example `Vt.Matrix4dArray`. The `Vt` arrays implement the [buffer protocol](https://docs.python.org/3/c-api/buffer.html), so we can convert to Numpy/Python without data duplication. This allows for some very efficient array editing via Python. Checkout our [Houdini Particles](../../dcc/houdini/fx/particles.md) section for a practical example. The value types module also houses wrapped base types (`Float`, `Int`, etc.), we don't use these though, as with Python everything is auto converted for us.

The `Vt.Type` registry also handles all on run-time registered types, so not only data types, but also custom types like `Sdf.Spec`,`SdfReference`, etc. that is registered by plugins.
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:tfTypeRegistry}}
```
~~~


### Data Roles <a name="dataRoles"></a>
Next let's explain what data roles are. Data roles extend the base data types by adding an hint about how the data should be interpreted. For example `Color3h`is just `Vec3h` but with the `role` that it should be treated as a color, in other words it should not be transformed by xforms ops, unlike `Point3h`, which is also `Vec3h`. Having roles is not something USD invented, you can find something similar in any 3d application.

### Working with data classes in Python 
You can find all values roles (and types) in the `Sdf.ValueTypeNames` module, this is where USD keeps the value type name registry.

The `Sdf.ValueTypeName` class gives us the following properties/methods:
- `aliasesAsStrings`: Any name aliases e.g. `texCoord2f[]`
- `role`: The role (intent hint), e.g. "Color", "Normal", "Point"
- `type`: The actual Tf.Type definition. From the type definition we can retrieve the actual Python data type class e.g. `Gf.Vec3h` and instantiate it.
- `cppTypeName`: The C++ data type class name, e.g `GfVec2f`. This is the same as `Sdf.ValueTypeNames.TexCoord2f.type.typeName`
- `defaultUnit`: The default unit. As USD is unitless (at least per when it comes to storing the data), this is `Sdf.DimensionlessUnitDefault` most of the time.
- `defaultValue`: The default value, e.g. `Gf.Vec2f(0.0, 0.0)`. For arrays this is just an empty Vt.Array. We can use `.scalarType.type.pythonClass` or `.scalarType.defaultValue` to get a valid value for a single element.
- Check/Convert scalar <-> array value type names:
    - `isArray`: Check if the type is an array.
    - `arrayType`: Get the vector type, e.g. `Sdf.ValueTypeNames.AssetArray.arrayType`gives us `Sdf.ValueTypeNames.AssetArray`
    - `isScalar`: Check if the type is scalar.
    - `scalarType`: Get the scalar type, e.g. `Sdf.ValueTypeNames.AssetArray.scalarType`gives us `Sdf.ValueTypeNames.Asset`

We can also search based on the string representation or aliases of the value type name, e.g. `Sdf.ValueTypeNames.Find("normal3h")`.

~~~admonish tip title="Pro Tip | Creating arrays"
The constructors for arrays allow us to input tuples/lists instead of the explicit base classes.
```python
# Explicit
pxr.Vt.Vec3dArray([Gf.Vec3d(1,2,3)])
# Implicit
pxr.Vt.Vec3dArray([(1,2,3)])
```
Instead of searching for the corresponding `Gf` or `Vt` array class, we can get it from the type name:
```python
vec3h_array =  Sdf.ValueTypeNames.Point3hArray.type.pythonClass((0,1,2))
print(type(vec3h_array)) # Returns: <class 'pxr.Vt.Vec3hArray'>
```
~~~


We won't be looking at specific data classes on this page, instead we'll have a look at how to access the data types from value types and vice versa as usually the data is generated by the DCC we use and our job is to validate the data type/role or e.g. create attributes with the same type when copying values.


Let's look at this in practice:
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataTypeRoleOverview}}
```
~~~
