# Composition Query
Next let's look at prim composition queries. Instead of having to filter the prim index ourselves, we can use the `Usd.PrimCompositionQuery` to do it for us. For more info check out our [Inspecting Composition](../../core/composition/pcp.md) section.

The query works by specifying a filter and then calling `GetCompositionArcs`.

USD provides these convenience filters, it returns a new `Usd.PrimCompositionQuery` instance with the filter applied:
- `Usd.PrimCompositionQuery.GetDirectInherits(prim)`: Returns all non ancestral inherit arcs
- `Usd.PrimCompositionQuery.GetDirectReferences(prim)`: Returns all non ancestral reference arcs
- `Usd.PrimCompositionQuery.GetDirectRootLayerArcs(prim)`: Returns arcs that were defined in the active layer stack.

These are the sub-filters that can be set. We can only set a single token value per filter:
- **ArcTypeFilter**: Filter based on different arc(s).
- **DependencyTypeFilter**: Filter based on if the arc was introduced on a parent prim or on the prim itself.
- **ArcIntroducedFilter**: Filter based on where the arc was introduced.
- **HasSpecsFilter**: Filter based if the arc has any specs (For example an inherit might not find any in the active layer stack)

~~~admonish tip title=""
```python
{{#include ../../../../code/core/composition.py:pcpPrimCompositionQuery}}
```
~~~

The returned filtered `Usd.CompositionArc` objects, allow us to inspect various things about the arc. You can find more info in the [API docs](https://openusd.org/dev/api/class_usd_prim_composition_query_arc.html)
