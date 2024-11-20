# Collections
Collections are USD's mechanism of storing a set of prim paths. We can nest/forward collections to other collections and relationships, which allows for powerful workflows. For example we can forward multiple collections to a light linking relationship or forwarding material binding relationships to a single collection on the asset root prim, which then in return forwards to the material prim.

# Table of Contents
1. [Collections In-A-Nutshell](#summary)
1. [What should I use it for?](#usage)
1. [Resources](#resources)
1. [Overview](#overview)
    1. [Creating & querying collections](#collectionQuery)
    1. [Inverting a collection](#collectionInvert)

## TL;DR - Metadata In-A-Nutshell <a name="summary"></a>
- Collections are encoded via a set of properties. A prim can store any number of collections.
    - `collection:<collectionName>:includes` relationship: A list of target `Sdf.Path`s to include, we can als target other collections.
    - `collection:<collectionName>:excludes` relationship: A list of target `Sdf.Path`s to exclude. These must be below the include paths.
    - `collection:<collectionName>:expansionRule`attribute: Controls how collections are computed, either by running `includes` - `excludes` (mode `explicitOnly`) or by expanding all child prims and then doing `includes` - `excludes` (mode `expandPrims`).
- Collections can link to other collections, which gives us a powerful mechanism of forwarding hierarchy structure information.
- Collections can easily be accessed and queried via the [Usd.CollectionAPI](https://openusd.org/release/api/class_usd_collection_a_p_i.html). The query can be limited via USD [filter predicates](https://openusd.org/dev/api/prim_flags_8h.html#Usd_PrimFlags), e.g. to defined prims only.
- To help speed up collection creation, USD also ships with util functions:
    - Collection creation: `UsdUtils.AuthorCollection(<collectionName>, prim, [<includePathList>], [<excludePathList>])`
    - Re-writing a collection to be as sparse as possible: `include_paths, exclude_paths = UsdUtils.ComputeCollectionIncludesAndExcludes(target_paths, stage)`

## What should I use it for? <a name="usage"></a>
~~~admonish tip
We use collections for multiple things:
- Creating a group of target paths, that are of interest to other departments, e.g. mark prims that are useful for FX/layout/lighting selections (for example character vs. background). Another common thing to use them for is storing render layer selections, that then get applied in our final render USD file.
- Faster navigation of hierarchies by isolating to collections that interest us.
- As collections can contain other collections, they are a powerful mechanism of forwarding and aggregating selections.
~~~

## Resources <a name="resources"></a>
- [Usd.CollectionAPI](https://openusd.org/release/api/class_usd_collection_a_p_i.html)
- [UsdUtils Collection Convenience Functions](https://openusd.org/dev/api/authoring_8h.html#ad2939a973bd544ff30e4828ff09765db)


## Overview <a name="overview"></a>
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

### Creating & querying collections <a name="collectionQuery"></a>
We interact with them via the `Usd.CollectionAPI` class [API Docs](https://openusd.org/release/api/class_usd_collection_a_p_i.html). The collection api is a multi-apply API schema, so we can add multiple collections to any prim.

Here are the UsdUtils.ComputeCollectionIncludesAndExcludes [API docs](https://openusd.org/dev/api/authoring_8h.html#ad2939a973bd544ff30e4828ff09765db).

~~~admonish tip title=""
```python
{{#include ../../../../../code/core/elements.py:collectionOverview}}
```
~~~

### Inverting a collection <a name="collectionInvert"></a>
When we want to isolate a certain part of the hierarchy (for example to pick what to render), a typical thing to do, is to give users a "render" collection which then gets applied by setting all prims not included to be [inactive](./prim.md#active). Here is an example of how to iterate a stage by pruning (skipping the child traversal) and deactivating anything that is not in the specific collection.

This is very fast and "sparse" as we don't edit leaf prims, instead we find the highest parent and deactivate it, if no children are part of the target collection.

~~~admonish tip title=""
```python
{{#include ../../../../../code/core/elements.py:collectionInvert}}
```
~~~
