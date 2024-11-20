# Bounding Box Queries <a name="boundingbox"></a>
Whenever we change our geometry data, we have to update our "extents" attribute on [boundable prims](https://openusd.org/dev/api/class_usd_geom_boundable.html). The bbox cache allows us to efficiently query bounding boxes. The result is always returned in the form of a `Gf.BBox3d` object.

For some production related examples, check out our [Frustum Culling](../../dcc/houdini/fx/frustumCulling.md) and [Particles](../../dcc/houdini/fx/particles.md) sections.

Checkout the [official API docs](https://openusd.org/dev/api/class_usd_geom_b_box_cache.html) for more info.

The "extents" attribute is managed via the `UsdGeom.Boundable` schema, you can find the [docs](https://openusd.org/dev/api/class_usd_geom_boundable.html) here. This has to be set per boundable prim.

The "extensHint" attribute is managed via the `UsdGeom.ModeAPI`, you can find the [docs](https://openusd.org/dev/api/class_usd_geom_model_a_p_i.html) here. This can be used to accelerate lookups, by not looking into the child-hierarchy. We typically write it on prims that load payloads, to have extent data when the payload is unloaded.

~~~admonish info title=""
```python
{{#include ../../../../code/production/caches.py:stageQueryBBox}}
```
~~~