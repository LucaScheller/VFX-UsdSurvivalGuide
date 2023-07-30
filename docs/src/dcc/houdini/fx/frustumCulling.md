# Frustum Culling
USD also ships with 3d related classes in the `Gf` module. These allow us to also do bounding box intersection queries.

We also have a frustum class available to us, which makes implementing frustum culling quite easy! The below code is a great exercise that combines using numpy, the core USD math modules, cameras and time samples. We recommend studying it as it is a great learning resource.

The code also works on "normal" non point instancer boundable prims.

You can find all the .hip files of our shown examples in our [USD Survival Guide - GitHub Repo](https://github.com/LucaScheller/VFX-UsdSurvivalGuide/tree/main/files/dcc/houdini).

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="./media/frustumCullingPointIInstancer.mp4" type="video/mp4" alt="Houdini Frustum Culling">
</video>

If you look closely you'll notice that the python LOP node does not cause any time dependencies. This is where the power of USD really shines, as we can sample the full animation range at once. It also allows us to average the culling data.

For around 10 000 instances and 100 frames, this takes around 2 seconds.

Here is the code shown in the video.

~~~admonish tip title=""
```python
{{#include ../../../../../code/dcc/houdini.py:houdiniFrustumCulling}}
```
~~~