# Collection Membership
Let's have a look at how we can query if a prim path is in a collection. For more info about how collections work, check out our [Collections](../../core/elements/collection.md) section.

### Creating & querying collections <a name="collectionQuery"></a>
We interact with collectins via the `Usd.CollectionAPI` class [API Docs](https://openusd.org/release/api/class_usd_collection_a_p_i.html). The collection api is a multi-apply API schema, so we can add multiple collections to any prim. We can them access them via the collection API. The `UsdUtils` module also offers some useful functions to recompute collections so that they don't consume to much disk storage.

Here are the UsdUtils.ComputeCollectionIncludesAndExcludes [API docs](https://openusd.org/dev/api/authoring_8h.html#ad2939a973bd544ff30e4828ff09765db).

~~~admonish tip title=""
```python
{{#include ../../../../code/core/elements.py:collectionOverview}}
```
~~~

### Inverting a collection <a name="collectionInvert"></a>
When we want to isolate a certain part of the hierarchy (for example to pick what to render), a typical thing to do, is to give users a "render" collection which then gets applied by setting all prims not included to be [inactive](./prim.md#active). Here is an example of how to iterate a stage by pruning (skipping the child traversal) and deactivating anything that is not in the specific collection.

This is very fast and "sparse" as we don't edit leaf prims, instead we find the highest parent and deactivate it, if no children are part of the target collection.

~~~admonish tip title=""
```python
{{#include ../../../../code/core/elements.py:collectionInvert}}
```
~~~
