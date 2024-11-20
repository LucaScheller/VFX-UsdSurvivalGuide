# Attribute Queries <a name="attribute"></a>
When we query attribute via `Usd.Attribute.Get()`, the value source resolution is re-evaluated on every call.
This can be cached by using `Usd.AttributeQuery(<prim>, <attributeName>)`. This small change can already bring a big performance boost, when looking up a large time sample count. In our example below, it doubled the speed.

For value clips the speed increase is not as high, as the value source can vary between clips.

The `Usd.AttributeQuery` object has a very similar signature to the `Usd.Attribute`. We can also get the time sample count, bracketing time samples and time samples within an interval.
For more information, check out the [official API docs](https://openusd.org/dev/api/class_usd_attribute_query.html).

~~~admonish info title=""
```python
{{#include ../../../../code/production/caches.py:stageQueryAttribute}}
```
~~~

# Primvars Queries <a name="primvars"></a>
As mentioned in our [properties](../../core/elements/property.md#reading-inherited-primvars) section, we couldn't get the native `FindIncrementallyInheritablePrimvars` primvars API method to work correctly. That's why we implemented it ourselves here, which should be nearly as fast, as we are not doing any calls into parent prims and tracking the inheritance ourselves.

It's also a great example of when to use `.PreAndPostVisit()` prim range iterators.

~~~admonish info title=""
```python
{{#include ../../../../code/production/caches.py:stageQueryInheritedPrimvars}}
```
~~~