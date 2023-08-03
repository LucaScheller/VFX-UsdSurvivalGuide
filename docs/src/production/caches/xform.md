# Xform Queries <a name="xform"></a>
As mentioned in our [transforms section](../../core/elements/transform.md), we can batch query transforms via the `UsdGeom.XformCache()`.

It caches ancestor parent xforms, so that when we query leaf prims under the same parent hierarchy, the lookup retrieves the cached parent xforms. The cache is managed per time code, so if we use `XformCache.SetTime(Usd.TimeCode(<someOtherFrame>))`, it clears the cache and re-populates it on the next query for the new time code.

Checkout the [official API docs](https://openusd.org/dev/api/class_usd_geom_xform_cache.html) for more info.

~~~admonish info title=""
```python
{{#include ../../../../code/production/caches.py:stageQueryTransform}}
```
~~~