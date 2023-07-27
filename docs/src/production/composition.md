# A practical overview on composition
~~~admonish question title="Still under construction!"
As composition is USD's most complicated topic, this section will be enhanced with more examples in the future.
If you detect an error or have useful production examples, please [submit a ticket](https://github.com/LucaScheller/VFX-UsdSurvivalGuide/issues/new), so we can improve the guide!

In the near future, we'll add examples for:
- Best practice asset structures
- Push Vs Pull / FullPin Opt-In pipelines
~~~

~~~admonish tip
We have a supplementary Houdini scene, that you can follow along with, available in this [site's repository](https://github.com/LucaScheller/VFX-UsdSurvivalGuide/tree/main/files/composition). All the examples below will walk through this file as it easier to prototype and showcase arcs in Houdini via nodes, than writing it all in code.
~~~

### How to approach shot composition
When prototyping your shot composition, we recommend an API like approach to loading data:

We create a `/__CLASS__/assets` and a `/__CLASS__/shots/<layer_name>` hierarchy. All shot layers first load assets via references and shot (fx/anim/etc.) caches via payloads into their respective class hierarchy. We then inherit this into the actual "final" hierarchy. This has one huge benefit: 

The class hierarchy is a kind of "API" to your scene hierarchy. For example if we want to time shift (in USD speak layer offset) an asset that has multiple occurrences in our scene, we have a single point of control where we have to change the offset. Same goes for any other kind of edit. 

We take a look at variations of this pattern in our [Composition Strength Ordering (LIVRPS)](../core/composition/livrps.md) section in context of different arcs, we highly recommend looking through the "Pro Tip" sections there.

This approach solves composition "problems": When we want to payload something over an asset reference, we can't because the payload arc is weaker than the reference arc. By "proxying" it to a class prim and then inheriting it, we guarantee that it always has the strongest opinion. This makes it easier to think about composition, as it is then just a single list-editable op rather than multiple arcs coming from different sources.

The downside to this approach is that we (as pipeline devs) need to restructure all imports to always work this way. The cache files themselves can still write the "final" hierarchy, we just have to reference/payload it all in to the class hierarchy and then inherit it. This may sound like a lot of work, but it is actually quick to setup and definitely helps us/artists keep organized with larger scenes. 

It also keeps our whole setup [instanceable](../core/composition/livrps.md#compositionInstance), so that we have the best possible performance. 

~~~admonish danger title="Pro Tip | Instanceable Prims"
When creating our composition structure concept, we should always try to keep everything instanceable until the very last USD file (the one that usually gets rendered). This way we ensure optimal performance and scalability.
~~~

We also show an example for this approach in our [Composition Payloads section](../core/composition/livrps.md#compositionArcPayloadLoadWorkflow) as well as bellow in the next bullet point.

### Loading heavy caches into your shots
When writing heavy caches, we usually write per frame/chunk files and load them via value clips. Let's have a look how to best do this:
As a best practice we always want to keep everything [instanceable](../core/composition/livrps.md#compositionInstance), so let's keep that in mind when loading in the data. 

~~~admonish tip title="Pro Tip | How do we load value clipped files?"
- When making prims instanceable, the value clip metadata has to be under the instanceable prim, as the value clip metadata can't be read from outside of the instance (as it would then mean each instance could load different clips, which would defeat the purpose of instanceable prims).
- Value clip metadata can't be inherited/internally referenced/specialized in. It must reside on the prim as a direct opinion.
- We can't have data above the prims where we write our metadata. In a typical asset workflow, this means that all animation is below the asset prims (when using value clips).
~~~

Let's have a look how we can set it up in Houdini while prototyping, in production you should do this via code, see our [animation](../core/elements/animation.md#animationValueClips) section for how to do this.

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="compositionValueClipAbstraction.mp4" type="video/mp4" alt="Houdini Value Clip Composition">
</video>

The simplest version is to write the value clips, stitch them and load the resulting file as a payload per asset root prim. This doesn't work though, if you have to layer over a hierarchy that already exists, for example an asset.

We therefore go for the "API" like approach as discussed above: We first load the cache via a payload into a class hierarchy and then inherit it onto its final destination. This is a best-practise way of loading it. By "abstracting" the payload to class prims, we have a way to load it via any arc we want, for example we could also payload it into variants. By then inherting it to the "final" hierarchy location, we ensure that no matter what arc, the cache gets loaded. This way we can load the cache (as it has heavy data) as payloads and then ensure it gets loaded with the highest opinion (via inherits).

Let's also take a look at why this doesn't work when trying to write value clips at non asset root prims:

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="compositionValueClipAbstractionStageRoot.mp4" type="video/mp4" alt="Houdini Value Clip Composition">
</video>

Loading a payload for a whole cache file works, the problem you then run into though is, that the inherit arcs don't see the parent prims value clip metadata. So we'd have to load the whole layer as a value clip. While this is possible, we highly don't recommend it, as it is not clear where the data source is coming from and we are making the scene structure messy by not having clear points of data loading. We also can't make it instanceable (unles we intend on making the whole hierarchy instanceable, which in shots doesn't work because we need per prim overrides (on at least asset (parent) prims)).