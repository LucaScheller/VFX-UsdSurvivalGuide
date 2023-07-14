# Resources
If you are interested in diving into topics yourself, here is a rough categorization:

### General
- [C++ Classes](https://openusd.org/release/api/annotated.html)

### High Level API

- [Usd Core API](https://openusd.org/release/api/usd_page_front.html)
    - [Asset Resolution (How file paths are evaluated)](https://openusd.org/release/api/ar_page_front.html)
    - [Cameras](https://openusd.org/release/api/class_gf_camera.html)
        - [Frustum](https://openusd.org/release/api/class_gf_frustum.html)
    - [Collections](https://openusd.org/release/api/class_usd_collection_a_p_i.html)
        - [Utils](https://openusd.org/release/api/authoring_8h.html)
    - [Event Listeners/Notifications](https://openusd.org/release/api/class_tf_notice.html) / [Notices](https://openusd.org/release/api/page_tf__notification.html)
    - [Hierarchy Iteration](https://openusd.org/release/api/class_usd_prim_range.html)
    - [Kinds](https://openusd.org/release/api/kind_page_front.html)
    - [Layers](https://openusd.org/release/api/class_sdf_layer.html)
        - [Stitching multiple layers to a single layer](https://openusd.org/release/api/stitch_8h.html)
        - [Loading different layers per frame (Value Clips)](https://openusd.org/release/api/_usd__page__value_clips.html)
            - [Utils](https://openusd.org/release/api/stitch_clips_8h.html)
        - [Flattening a stage to a layer]()
    - [Plugins](https://openusd.org/release/api/plug_page_front.html)
    - Class (Schema) APIs
        - [Collections](https://openusd.org/release/api/class_usd_collection_a_p_i.html)
        - [Lights](https://openusd.org/release/api/class_usd_lux_light_a_p_i.html)
        - [Node Graph Shader Connections](https://openusd.org/release/api/class_usd_shade_connectable_a_p_i.html)
        - [Value Clips](https://openusd.org/release/api/class_usd_clips_a_p_i.html)
        - [Transforms](https://openusd.org/release/api/class_usd_geom_xform_common_a_p_i.html)
    - Query/Lookup Caches
        - [Attributes](https://openusd.org/release/api/class_usd_attribute_query.html)
        - [Composition](https://openusd.org/release/api/class_usd_prim_composition_query.html)
        - [Collections](https://openusd.org/release/api/class_usd_collection_membership_query.html)
        - [Bounding Boxes](https://openusd.org/release/api/class_usd_geom_b_box_cache.html)
        - [Transforms](https://openusd.org/release/api/class_usd_geom_xform_cache.html)
    - [Stages]()
        - [Prims](https://openusd.org/release/api/class_usd_prim.html)
        - [Property](https://openusd.org/release/api/class_usd_property.html)
            - [Attribute](https://openusd.org/release/api/class_usd_attribute.html)
            - [Relationship](https://openusd.org/release/api/class_usd_relationship.html)
    - Statistics
        - [Stage Statistics](https://openusd.org/release/api/introspection_8h.html)
        - [Profiling Performance(Tracing)](https://openusd.org/release/api/trace_page_front.html)
    - [Utils](https://openusd.org/release/api/usd_utils_page_front.html)

### Low Level API

- [Sdf - Scene Description Foundations](https://openusd.org/release/api/sdf_page_front.html)
    - [Sdf.Layer]()
        - [Sdf.PrimSpec]()
            - [Sdf.PropertySpec](https://openusd.org/release/api/class_sdf_property_spec.html)
                - [Sdf.AttributeSpec](https://openusd.org/release/api/class_sdf_attribute_spec.html)
                - [Sdf.RelationshipSpec](https://openusd.org/release/api/class_sdf_relationship_spec.html)
        - [Sdf.VariantSpec](https://openusd.org/release/api/class_sdf_variant_spec.html)
    - [Sdf.Path](https://openusd.org/release/api/class_sdf_path.html)
    - [Sdf.ListOps](https://openusd.org/release/api/class_sdf_list_op.html)
- [Pcp - PrimCache Population (Composition)](https://openusd.org/release/api/pcp_page_front.html)
    - [Pcp.PrimIndex](https://openusd.org/release/api/class_pcp_prim_index.html)
