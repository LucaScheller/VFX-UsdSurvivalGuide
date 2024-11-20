# RBD (Rigid Body Dynamics)
As mentioned in our [Point Instancer](./pointinstancers.md) section, we have four options for mapping Houdini's packed prims to USD:
- As transforms
- As point instancers
- As deformed geo (baking down the xform to actual geo data)
- As skeletons

Which confronts us with the question:

~~~admonish tip title="Pro Tip | How should I import my RBD(Rigid Body Dynamics) simulation?"
As mentioned in our [production FAQ](../../../production/faq.md#faqPrimCount), large prim counts cause a significant decrease in performance.
That's why we should avoid writing RBD sims as transform hierarchies and instead either go for deformed geo (not memory efficient) or skeletons 
(memory efficient).
~~~

~~~admonish danger title="Skeletons and Custom Normals"
Currently Hydra does not yet read in custom normals, when calculating skinning. This will likely be resolved in the very near future, until then we have to bake the skinning pre-render. This is very fast to do via the skeleton API, more details below.
~~~

On this page we'll focus on the skeleton import, as it is the only viable solution for large hierarchy imports. It is also the most efficient one, as skeletons only store the joint xforms, just like the RBD simulation point output.

Using skeletons does have one disadvantage: We can't select a mesh separately and hide it as skeletons deform subsets of each individual prim based on weighting.

The solution is to set the scale of the packed piece to 0. For hero simulations, where we need to have a separate hierarchy entry for every piece, we'll have to use the standard packed to xform import. We can also do a hybrid model: Simply change the hierarchy paths to your needs and import them as skeletons. This way, we can still disable meshes based on what we need, but get the benefits of skeletons.

You can find all the .hip files of our shown examples in our [USD Survival Guide - GitHub Repo](https://github.com/LucaScheller/VFX-UsdSurvivalGuide/tree/main/files/dcc/houdini).


## Houdini Native Import via KineFX/Crowd Agents
Let's first take a look at what Houdini supports out of the box:
- We can import KineFX characters and crowd agents as skeletons. This does have the overhead of creating KineFX characters/crowd agents in a way that they map to our target output hierarchy we want in LOPs. It is also harder to setup with a lot of different skeletons (Or we couldn't figure, input is always welcome).
- The "RBD Destruction" LOP node has a reference implementation of how to import packed prims as skeletons animations. It relies on Python for the heavy data lifting and doesn't scale well, we'll take a look at a high performance solution in the next section below, that uses Houdini's native import for the data loading and Python to map everything to its correct place.

Here is a video showing both methods:

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="../../../../media/dcc/houdini/fx/rbdKineFXCrowdAgent.mp4" type="video/mp4" alt="Houdini Character Skeleton Import">
</video>

This works great, if we have a character like approach. 

## Houdini High Performance RBD Skeleton Import

The problem is with RBD sims this is not the case: We usually have a large hierarchy consisting of assets, that we fracture, that should then be output to the same hierarchy location as the input hierarchy. As skeletons are only evaluated for child hierarchies, where we have a "SkelRoot" prim as an ancestor, our approach should be to make all asset root prims (the ones that reference/payload all the data), be converted to have the "SkelRoot" prim type. This way we can nicely attach a skeleton to each asset root, which means we can selectively payload (un)load our hierarchy as before, even though each asset root pulls the skeleton data from the same on disk cache.

Let's take a look how that works:

<video width="100%" height="100%" controls autoplay muted loop>
  <source src="../../../../media/dcc/houdini/fx/rbdSkeleton.mp4" type="video/mp4" alt="Houdini Skeleton Custom Import">
</video>

Now we won't breakdown how skelton's themselves work, as this is a topic on its own. You can read up on it in the [official API docs](https://openusd.org/dev/api/_usd_skel__intro.html).

What we'll do instead is break down our approach. We have three inputs from LOPs, where we are pulling data from:
- Geometry data: Here we import our meshes with:
    - their joint weighting (RBD always means a weight of 1, because we don't want to blend xforms). 
    - their joint index. Skeleton animations in USD can't have time varying joint index to joint name mapping. This is designed on purpose, to speed up skeleton mesh binding calculation.
    - their target skeleton. By doing our custom import we can custom build our skeleton hierarchy. In our example we choose to group by asset, so one skeleton per asset.
- Rest data: As with a SOP transform by points workflow, we have to provide:
    - the rest position
    - the bind position (We can re-use the rest position)
    - the joint names. We could also import them via the animation data, there is no benefit though, as joint idx to name mappings can't be animated (even though they are attributes and not relationships).
- Animation data: This pulls in the actual animation data as:
    - translations
    - rotations
    - scales (Houdini's RBD destruction .hda optionally disables animation import for scales as an performance opt-in)

After the initial import, we then "only" have to apply a few schemas and property renames. That's it, it's as simple as that!

So why is this a lot faster, than the other methods?

We use Houdini's super fast SOP import to our benefit. The whole thing that makes this work are the following two pieces of our node network:

Our joint name to index mapping is driven by a simple "Enumerate" node that runs per skeleton target prim path.

 <video width="100%" height="100%" controls autoplay muted loop>
  <source src="../../../../media/dcc/houdini/fx/rbdSkeletonJointIndexName.mp4" type="video/mp4" alt="Houdini Skeleton Joint Index Name">
</video>

Our joint xforms then create the same skeleton target prim path. We don't have to enumerate, because on LOP import our geometry is segmented based on the skeleton prim path. This slices the arrays the exact same way as the enumerate node. 

 <video width="100%" height="100%" controls autoplay muted loop>
  <source src="../../../../media/dcc/houdini/fx/rbdSkeletonJointXforms.mp4" type="video/mp4" alt="Houdini Skeleton Joint Xforms">
</video>

The outcome is that we let Houdini do all the heavy data operations like mesh importing and attribute segmentation by path.
We then only have to remap all the data entries to their correct parts. As USD is smart enough to not duplicate data for renames, this is fast and memory efficient.
