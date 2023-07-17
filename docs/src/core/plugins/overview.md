# Plugin System
Usd has a plugin system over which individual components are loaded.

~~~admonish Abstract title="Usd Pipeline Plugins"
In this guide we will cover how to create these minimal set of plugins needed to setup a production ready Usd pipeline:
- **Kinds Plugin** (No compiling needed): For this plugin all you need is a simple .json file that adds custom kinds. Head over to our [kind](./kind.md) section to get started.
- **Asset Resolver Plugin** (Compiling needed or use pre-packed resolvers): Head over to our [asset resolver](./assetresolver.md) section to get started. The actual [code](https://github.com/LucaScheller/VFX-UsdAssetResolver) and [guide](https://lucascheller.github.io/VFX-UsdAssetResolver/) is hosted here as it is a big enough topic of its own.
- **Schema Plugin** (Optional, compiling needed if you want Python C++/Bindings): A schema plugin allows you to create own prim types/API schemas. This is useful when you need to often create a standardized set of attributes on prims that are relevant for your pipeline. Head over to our [schemas](./schemas.md) section to get going or to our [schemas overview](../elements/schemas.md) section to get an overview of what schemas are.
~~~

Typical plugins are:
- Schemas
- Kinds
- Asset Resolver
- Hydra Delegates (Render Delegates)
- File Format Plugins (.abc/.vdb)

You can inspect if whats plugins werwe registered by setting the `TF_DEBUG` variable as mentioned in the [debugging](../profiling/debug.md) section:
```bash
export TF_DEBUG=PLUG_REGISTRATION
```

If you want to check via Python, you have to know under what registry the plugin is installed. There are several (info shamelessly copied from the below linked USD-CookBook page ;)):
- KindRegistry
- PlugRegistry
- Sdf_FileFormatRegistry
- ShaderResourceRegistry
- UsdImagingAdapterRegistry

Colin Kennedy's USD-Cookbook has an excellent overview on this topic:
[USD Cook-Book Plugins](ttps://github.com/ColinKennedy/USD-Cookbook/blob/33eac067a0a62578934105b19a2b9d8e4ea0646c/references/working_with_plugins.md)

Plugins are detected by looking at the `PXR_PLUGINPATH_NAME` environment variable for folders containing a`plugInfo.json` file.

To set it temporarily, you can run the following in a shell and then run your Usd application:
```
// Linux
export PXR_PLUGINPATH_NAME=/my/cool/plugin/resources:${PXR_PLUGINPATH_NAME}
// Windows
set PXR_PLUGINPATH_NAME=/my/cool/plugin/resources:${PXR_PLUGINPATH_NAME}
```

If you search you Usd installation, you'll find a few of these for different components of Usd. They are usually placed in a <Plugin Root>/resources folder as a common directory convention.

Via Python you can also partially search for plugins (depending on what registry they are in) and also print their plugInfo.json file content via the `.metadata` attribute.

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:pluginsRegistry}}
```
~~~

We can also use the plugin registry to lookup from what plugin a specific type/class (in this case a schema) is registered by:
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:schemasPluginRegistry}}
```
~~~

