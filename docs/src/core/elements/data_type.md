# Data Types/Roles
~~~admonish question title="Still under construction!"
This sub-section is still under development, it is subject to change and needs extra validation.
~~~

# Table of contents
1. [Data Types/Roles In-A-Nutshell](#summary)
1. [What should I use it for?](#usage)
1. [Resources](#resources)
1. [Overview](#overview)
    1. [Data Types](#dataTypes)
    1. [Data Roles](#dataRoles)

## TL;DR - Metadata In-A-Nutshell <a name="summary"></a>
- Main points to know

## What should I use it for? <a name="usage"></a>
~~~admonish tip
Summarize actual production relevance.
~~~

## Resources <a name="resources"></a>
- [USD API Data Type Docs](https://openusd.org/dev/api/_usd__page__datatypes.html)
- [NVidia USD Data Types Docs](https://docs.omniverse.nvidia.com/dev-guide/latest/dev_usd/quick-start/usd-types.html)

## Overview <a name="overview"></a>
When reading and writing data in USD, all data is of a specific data type. USD extends the standard base types (`float`, `int`) with computer graphics related classes (`Gf.Matrix3d`, `Gf.Vec3h`) that make it easy to perform common 3d math operations. To give a hint about how a data type should be used, we have the concept of data roles.

### Data Types <a name="dataTypes"></a>
Let's first talk about data types. These are the base data classes all data is USD is stored in.

To access the base data classes there are three modules:
- `Sdf`(Scene Description Foundations): Here you'll 99% of the time only be using `Sdf.AssetPath`, `Sdf.AssetPathArray` and the [list editable ops](../composition/listeditableops.md) that have the naming convention `<Type>ListOp` e.g. `Sdf.PathListOp`, `Sdf.ReferenceListOp`, `Sdf.ReferenceListOp`, `PayloadListOp`, `StringListOp`, `TokenListOp`
- `Gf`(Graphics Foundations): The `Gf` module is basically USD's math module. Here we have all the math related data classes that are made up of the base types (base types being `float`, `int`, `double`, etc.). Commonly used classes/types are `Gf.Matrix4d`, `Gf.Quath`(Quaternions), `Gf.Vec2f`, `Gf.Vec3f`, `Gf.Vec4f`. Most classes are available in different precisions, noted by the suffix `h`(half),`f`(float), `d`(double).
- `Vt` (Value Types): Here we can find all the `Array` (list) classes that capture the base classes from the `Gf` module in arrays. For example `Vt.Matrix4dArray`. The `Vt` arrays implement the [buffer protocol](https://docs.python.org/3/c-api/buffer.html), so we can convert to Numpy/Python without data duplication. This allows for some very efficient array editing via Python. Checkout our [Houdini Particles](../../dcc/houdini/fx/particles.md) section for a practical example. The value types module also houses wrapped base types (`Float`, `Int`, etc.), we don't use these though, as with Python everything is auto converted for us.

### Data Roles <a name="dataRoles"></a>
Next let's explain what data roles are. Data roles extend the base data types by adding an hint about how the data should be interpreted. For example `Color3h`is just `Vec3h` but with the `role` that it should be treated as a color, in other words it should not be transformed by xforms ops, unlike `Point3h`, which is also `Vec3h`. Having roles is not something USD invented you can find something similar in any 3d application.


### Working with data classes in Python 
You can find all values types in the `pxr.Sdf.ValueTypeNames` module, this is where USD keeps the value type registry.

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataTypeRoleOverview}}
```
~~~
