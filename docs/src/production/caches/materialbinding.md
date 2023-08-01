# Material Binding <a name="materialBinding"></a>
~~~admonish question title="Still under construction!"
This sub-section is still under development, we'll add more advanced binding lookups in the near future!
~~~

Looking up material bindings is as simple as running `materials, relationships = UsdShade.MaterialBindingAPI.ComputeBoundMaterials([<list of prims>]`.
This gives us the bound material as a `UsdShade.Material` object and the relationship that bound it.
That means if the binding came from a parent prim, we'll get the `material:binding` relationship from the parent.

~~~admonish info title=""
```python
{{#include ../../../../code/production/caches.py:stageQueryMaterialBinding}}
```
~~~