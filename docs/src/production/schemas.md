# Commonly used schemas ('Classes' in OOP terminology) for production

Here is a list of the most used production schemas with a short explanation of what the schema provides:

- Typed:
    - [UsdGeom.Imageable](https://openusd.org/dev/api/class_usd_geom_imageable.html): Purpose, Visibility, Bounding Box
        - [UsdGeom](https://openusd.org/dev/api/usd_geom_page_front.html)
            - [UsdGeom.PointInstancer](https://openusd.org/dev/api/class_usd_geom_point_instancer.html): PointInstancers
            - [UsdGeom.PointBased](https://openusd.org/dev/api/class_usd_geom_point_based.html):
                - [UsdGeom.Mesh](https://openusd.org/dev/api/class_usd_geom_mesh.html): Polygon Meshes
                - [UsdGeom.Points](https://openusd.org/dev/api/class_usd_geom_points.html): Points
                - [UsdGeom.Curves](https://openusd.org/dev/api/class_usd_geom_curves.html): Curves
            - [UsdVol.Volume](https://openusd.org/dev/api/class_usd_vol_volume.html): Volumes
                - [UsdVol.OpenVDBAsset](https://openusd.org/dev/api/class_usd_vol_open_v_d_b_asset.html): VDB Volumes
            - [UsdGeom.Xformable](https://openusd.org/dev/api/class_usd_geom_xformable.html): Transforms
            - [UsdGeom.ModelAPI](https://openusd.org/dev/api/class_usd_geom_model_a_p_i.html): Draw Mode, ExtentHint  
            - [UsdGeom.Camera](https://openusd.org/dev/api/class_usd_geom_camera.html): Camera Attributes, Access to Gf.Camera
- API:
    - [Usd.ModeAPI](https://openusd.org/dev/api/class_usd_model_a_p_i.html): Asset info, Kind 
    - [Usd.ClipsAPI](https://openusd.org/dev/api/class_usd_clips_a_p_i.html): Value Clips (Metadata for per frame caches)
    - [Usd.CollectionAPI](https://openusd.org/dev/api/class_usd_collection_a_p_i.html): Collections
    - [Usd.PrimvarsAPI](https://openusd.org/dev/api/class_usd_geom_primvars_a_p_i.html): Primvars Attributes
    - [UsdGeom.XformCommonAPI](https://openusd.org/dev/api/class_usd_geom_xform_common_a_p_i.html): Simplified transforms
    - [Usd.VisibilityAPI (Beta)](https://openusd.org/dev/api/class_usd_geom_visibility_a_p_i.html): Visibility per purpose
    - [UsdSkel.BindingAPI](https://openusd.org/dev/api/class_usd_skel_binding_a_p_i.html): Skeleton bindings
    - [UsdShade.ConnectableAPI](https://openusd.org/dev/api/class_usd_shade_connectable_a_p_i.html): Shader connections
    - [UsdShade.CoordSysAPI](https://openusd.org/dev/api/class_usd_shade_coord_sys_a_p_i.html): Coordinate spaces for shaders
- Graphics Foundations (Gf):
    - [Gf.Camera](https://openusd.org/dev/api/class_gf_camera.html): Camera
    - [Gf.Frustum](https://openusd.org/dev/api/class_gf_frustum.html): Frustum