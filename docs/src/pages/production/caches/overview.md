# Stage API Query Caches
When inspecting stages, we often want to query a lot of data.

Some types of data, like transforms/material bindings or primavars, are inherited down the hierarchy. Instead of re-querying the ancestor data for each leaf prim query, USD ships with various query classes that cache their result, so that repeated queries have faster look ups.

For currently cover these query caches:
- [Xforms](./xform.md)
- [BoundingBox](./boundingbox.md)
- [Attribute/(Inherited) Primvars](./attribute.md)
- [Material Binding](./materialbinding.md)
- [Collection Membership](./collection.md)
- [Composition](./composition.md)