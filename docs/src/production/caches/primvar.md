# Primvar Queries
As mentioned in our [properties](../../core/elements/property.md#reading-inherited-primvars) section, we couldn't get the native `FindIncrementallyInheritablePrimvars` primvars API method to work correctly, we here is a self implemented (should be nearly as fast) method. 

It's also a great example of when to use `.PreAndPostVisit()` prim range iterators.

~~~admonish info title=""
```python
{{#include ../../../../code/production/caches.py:stageQueryInheritedPrimvars}}
```
~~~