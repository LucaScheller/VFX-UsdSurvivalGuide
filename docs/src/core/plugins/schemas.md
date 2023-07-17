# Schemas
~~~admonish tip
This page only covers how to create custom schemas, as we cover what schemas are in our [schemas](../elements/schemas.md) basic building blocks of USD section.
~~~

As there is a very well written documentation in the [official docs](https://openusd.org/release/api/_usd__page__generating_schemas.html), we only cover compilation(less) schema creation and installation here as a hands-on example and won't go into any customization details.

# Table of contents
1. [API Overview In-A-Nutshell](#summary)
2. [What should I use it for?](#usage)
3. [Resources](#resources)
4. [Overview](#overview)
    1. [Generate Codeless Schema](#usdGenSchemaCodelessSchema)
        1. [Edit GLOBAL prim 'customData' dict](#usdGenSchemaCodelessSchemaStep1)
        2. [Run usdGenSchema](#usdGenSchemaCodelessSchemaStep2)
        3. [Add the generated pluginInfo.json director to 'PXR_PLUGINPATH_NAME' env var.](#usdGenSchemaCodelessSchemaStep3)
        4. [Run your Usd (capable) application.](#usdGenSchemaCodelessSchemaStep4)
    1. [Generate Schema](#usdGenSchemaSchema)



## TL;DR - Schema Creation In-A-Nutshell <a name="summary"></a>
- Generating schemas in Usd is as easy as supplying a customized `schema.usd` file to the `usdGenSchema` commandline tool that ships with Usd. (That's right, you don't need to code!)
- Custom schemas allow us to create custom prim types/properties/metadata (with fallback values) so that we don't have to repeatedly re-create it ourselves.
- In OOP speak: It allows you to create your own subclasses that nicely fit into Usd and automatically generates all the `Get<PropertyName>`/`Set<PropertyName>` methods, so that it feels like you're using native USD classes.
- We can also create `codeless` schemas, these don't need to be compiled, but we won't get our nice automatically generated getters and setters and schema C++/Python a classes.

~~~admonish tip
Codeless schemas are ideal for smaller studios or when you need to prototype a schema. The result only consists of a `plugInfo.json` and `generatedSchema.usda` file and is instantly created without any need for compiling.
~~~

## What should I use it for? <a name="usage"></a>
~~~admonish tip
We'll usually want to generate custom schemas, when we want to have a set of properties/metadata that should always exist (with a fallback value) on certain prims. A typical use case for creating an own typed/API schema is storing common render farm settings or shot related data.
~~~

# Resources <a name="resources"></a>
- [API Docs](https://openusd.org/release/api/_usd__page__generating_schemas.html)

## Overview <a name="overview"></a>
For both examples will start of with the example schema that USD ships with in its official repo.

You can copy and paste the [content](https://github.com/PixarAnimationStudios/OpenUSD/blob/release/extras/usd/examples/usdSchemaExamples/schema.usda) into a file and then follow along or take the prepared files from [here](https://github.com/LucaScheller/VFX-UsdSurvivalGuide/tree/main/files/plugins/schemas) that ship with this repo.

Our guide focuses on working with Houdini, therefore we use the `usdGenSchema` that ships with Houdini. You can find it in your Houdini /bin directory.
~~~admonish tip title=""
```bash
$HFS/bin/usdGenSchema
# For example on Linux:
/opt/hfs19.5/bin/usdGenSchema
```
~~~

If you download/clone this repo, we ship with .bash scripts that automatically run all the below steps for you.

You'll first need to `cd` to the root repo dir and then run `./setup.sh`. Make sure that you edit the `setup.sh` file to point to the Houdini version. By default it will be the latest Houdini major release symlink, currently `/opt/hfs19.5`, that Houdini creates on install.

Then follow along the steps as mentioned below.

### Codeless TypedSchema <a name="usdGenSchemaCodelessSchema"></a>
Codeless schemas allow us to generate schemas without any C++/Python bindings. This means your won't get fancy `Schema.Get<PropertyName>`/`Schema.Set<PropertyName>` getters and setters, on the upside you don't need to compile anything. 

~~~admonish tip
Codeless schemas are ideal for smaller studios or when you need to prototype a schema. The result only consists of a `plugInfo.json` and `generatedSchema.usda` file.
~~~

To enable codeless schema generation, we simply have to add `bool skipCodeGeneration = true` to the customData metadata dict on the global prim in our schema.usda template file.
~~~admonish tip title=""
```python
over "GLOBAL" (
    customData = {
        bool skipCodeGeneration = true
    }
) {
}
```
~~~

Let's do this step by step for our example schema.

#### Step 1: Edit GLOBAl prim 'customData' dict <a name="usdGenSchemaCodelessSchemaStep1"></a>
Update the global prim custom data dict from:
~~~admonish tip title=""
```python
over "GLOBAL" (
    customData = {
        string libraryName       = "usdSchemaExamples"
        string libraryPath       = "."
        string libraryPrefix     = "UsdSchemaExamples"
        bool skipCodeGeneration = true
    }
) {
}
```
~~~
to:
~~~admonish tip title=""
```python
over "GLOBAL" (
    customData = {
        string libraryName       = "usdSchemaExamples"
        string libraryPath       = "."
        string libraryPrefix     = "UsdSchemaExamples"
        bool skipCodeGeneration = true
    }
) {
}
```
~~~

#### Step 2: Run usdGenSchema <a name="usdGenSchemaCodelessSchemaStep2"></a>
Next we need to generate the schema. 

Make sure that you first sourced you Houdini environment by running `$HFS/houdini_setup` so that it find all the correct libraries and python interpreter. On Windows you can als run `hython usdGenSchema schema.usda dst` to avoid having to source the env yourself.

Then run the following
~~~admonish tip title=""
```bash
cd /path/to/your/schema # In our case: ../VFX-UsdSurvivalGuide/files/plugins/schemas/codelessTypedSchema
usdGenSchema schema.usda dst
```
~~~
Or if you use the helper bash scripts in this repo (after sourcing the `setup.sh` in the repo root):
~~~admonish tip title=""
```bash
cd ./files/plugins/schemas/codelessTypedSchema/
chmod +x build.sh # Add execute rights
source ./build.sh # Run usdGenSchema and source the env vars for the plugin path
```
~~~

~~~admonish bug
Not sure if this is a bug, but the `usdGenSchema` in codeless mode currently outputs a wrong `plugInfo.json` file. (It leaves in the cmake @...@ string replacements).

The fix is simple, open the `plugInfo.json` file and replace:
```python
...
    "LibraryPath": "@PLUG_INFO_LIBRARY_PATH@", 
    "Name": "usdSchemaExamples", 
    "ResourcePath": "@PLUG_INFO_RESOURCE_PATH@", 
    "Root": "@PLUG_INFO_ROOT@", 
    "Type": "resource"
...
```
To:
```python
...
    "LibraryPath": ".", 
    "Name": "usdSchemaExamples", 
    "ResourcePath": ".", 
    "Root": ".", 
    "Type": "resource"
...
```
~~~

#### Step 3: Add the generated pluginInfo.json director to 'PXR_PLUGINPATH_NAME' env var. <a name="usdGenSchemaCodelessSchemaStep3"></a>
Next we need to add the pluginInfo.json directory to the `PXR_PLUGINPATH_NAME` environment variable.
~~~admonish tip title=""
```bash
// Linux
export PXR_PLUGINPATH_NAME=/Enter/Path/To/dist:${PXR_PLUGINPATH_NAME}
// Windows
set PXR_PLUGINPATH_NAME=/Enter/Path/To/dist:${PXR_PLUGINPATH_NAME}
```
~~~
If you used the helper bash script, it is already done for us.

#### Step 4: Run your Usd (capable) application. <a name="usdGenSchemaCodelessSchemaStep4"></a>
Yes, that's right! It was that easy. (Puts on sunglass, ah yeeaah! 😎)

If you run Houdini and then create a primitive, you can now choose the `ComplexPrim` as well as assign the `ParamAPI` API schema.

!["test"](./schemaCodelessHoudini.jpg#center)

Or if you want to test it in Python:
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:schemasPluginCodelessTest}}
```
~~~