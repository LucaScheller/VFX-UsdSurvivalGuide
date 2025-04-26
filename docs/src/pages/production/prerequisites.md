# 'Are we ready for production'? Here is a preflight checklist for your USD pipeline
Now that you know the basics (if you did your homework 😉), let's make sure you are ready for your first test flight.

Below is a checklist that you can use to test if everything is ready to go.

~~~admonish warning title=""
You can never prepare a 100%, some times you gotta run before you walk as the experience (and pressure) from an actual project running on USD will be more valuable than any RnD. So make sure you have kept the points below in mind to at least some degree.
~~~

Vocabulary:
- Usd comes with a whole lot of new words, as a software developer you'll get used to it quite quickly, but don't forget about your users. Having an onboarding for vocab is definitely worth it, otherwise everyone speaks a different language which can cause a lot of communication overhead. 

Plugins (Covered in our [plugins](../core/plugins/overview.md) section):
- **Kinds** (Optional, Recommended): All you need for this one, is a simple .json file that you put in your `PXR_PLUGINPATH_NAME` search path. 
- **Schemas** (Optional, Recommended): There are two flavours of creating custom schemas: Codeless (only needs a `schema.usda` + `plugInfo.json` file) and compiled schemas (Needs compilation, but gives your software devs a better UX). If you don't have the resources for a C++ developer, codeless schemas are the way to go and more than enough to get you started.
- **Asset Resolver** (Mandatory): You unfortunately can't get around not using one, luckily we got you covered with our production ready asset resolvers over in our [VFX-UsdAssetResolver GitHub Repo](https://github.com/LucaScheller/VFX-UsdAssetResolver).

Data IO and Data Flow:
- As a pipeline/software developer the core thing that has to work is data IO. This is something a user should never have to think about. What does this mean for you:
    - Make sure your UX experience isn't too far from what artists already know.
- Make sure that your system of tracking layers and how your assets/shots are structured is solid enough to handle these cases:
    - Assets with different layers (model/material/fx/lighting)
    - FX (Asset and Shot FX, also make sure that you can also track non USD dependencies, like .bgeo, via metadata/other means)
    - Assemblies (Assets that reference other assets)
    - Multi-Shot workflows (Optional)
    - Re-times (Technically these are not possible via USD (at least over a whole layer stack), so be aware of the restrictions and communicate these!)
- It is very likely that you have to adjust certain aspects of how you handle composition at some point. In our [composition](../core/composition/overview.md) section we cover composition from an abstract implementation viewpoint, that should help keep your pipeline flexible down the line. It is one of the ways how you can be prepared for future eventualities, it does add a level of complexity though to your setups (pipeline wise, users should not have to worry about this).

