# Collections
Collections are USD's mechanism of storing a set of prim paths. We can nest/forward collections to other collections and relationships, which allows for powerful workflows. For example we can forward multiple collections to a light linking relationship or forwarding material binding relationships to a single collection on the asset root prim, which then in return forwards to the material prim.

Collections are made up of relationships and attributes:
- `collection:<collectionName>:includes` relationship: A list of target `Sdf.Path`s to include, we can als target other collections.
- `collection:<collectionName>:excludes` relationship: A list of target `Sdf.Path`s to exclude. These must be below the include paths. Excluding another collection does not work. 
- `collection:<collectionName>:expansionRule`attribute: This controls how collections are expanded:
    - `explicitOnly`: Do not expand to any child prims, instead just do an explicit diff between include and exclude paths. This is like a Python `set().difference()`.  
    - `expandPrims`: Expand the include paths to all children and subtract the exclude paths.
    - `expandPrimsAndProperties`: Same as `expandPrims`, but expand properties too. (Not used by anything at the moment).
- (Optional) `collection:<collectionName>:includeRoot` attribute: When using `expandPrims`/`expandPrimsAndProperties` this bool attribute enables the includes to target the `/` pseudo root prim.

~~~admonish danger title="Collection Size"
Make sure that you write your collections as sparsely as possible, as otherwise they can take a long time to combine when stitching multiple files, when writing per frame USD files.
~~~

We interact with them via the `Usd.CollectionAPI` class [API Docs](https://openusd.org/release/api/class_usd_collection_a_p_i.html). The collection api is a multi-apply API schema, so we can add multiple collections to any prim.

~~~admonish tip title=""
```python
{{#include ../../../../code/core/elements.py:relationshipCollections}}
```
~~~

Here are the UsdUtils.ComputeCollectionIncludesAndExcludes [API docs](https://openusd.org/dev/api/authoring_8h.html#ad2939a973bd544ff30e4828ff09765db).
