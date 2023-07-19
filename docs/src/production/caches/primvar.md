# Primvar Queries
As mentioned in our [properties](../../core/elements/property.md#reading-inherited-primvars) section, we couldn't get the native `FindIncrementallyInheritablePrimvars` primvars API method to work correctly. That's why we implemented it ourselves here, which should be nearly as fast, as we are not doing any calls into parent prims and tracking the inheritance ourselves.

It's also a great example of when to use `.PreAndPostVisit()` prim range iterators.

~~~admonish info title=""
```python
{{#include ../../../../code/production/caches.py:stageQueryInheritedPrimvars}}
```
~~~