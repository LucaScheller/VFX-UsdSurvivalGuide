# Schemas
~~~admonish important
This page only covers how to compile/install custom schemas, as we cover what schemas are in our [schemas](../elements/schemas.md) basic building blocks of USD section.
~~~

As there is a very well written documentation in the [official docs](https://openusd.org/release/api/_usd__page__generating_schemas.html), we only cover compilation(less) schema creation and installation here as a hands-on example and won't go into any customization details. You can also check out Colin's excellent [Usd-Cook-Book](https://github.com/ColinKennedy/USD-Cookbook/tree/master/plugins/custom_schemas_with_python_bindings) example.

# Table of Contents
1. [API Overview In-A-Nutshell](#summary)
2. [What should I use it for?](#usage)
3. [Resources](#resources)
4. [Overview](#overview)
5. [Generate Codeless Schema](#usdGenSchemaCodelessSchema)
    1. [Edit 'GLOBAL' prim 'customData' dict](#usdGenSchemaCodelessSchemaStep1)
    2. [Run usdGenSchema](#usdGenSchemaCodelessSchemaStep2)
    3. [Add the generated pluginInfo.json director to 'PXR_PLUGINPATH_NAME' env var.](#usdGenSchemaCodelessSchemaStep3)
    4. [Run your Usd (capable) application.](#usdGenSchemaCodelessSchemaStep4)
6. [Generate Compiled Schema](#usdGenSchemaCompiledSchema)
    1. [Run usdGenSchema](#usdGenSchemaCompiledSchemaStep1)
    2. [Compile schema](#usdGenSchemaCompiledSchemaStep2)
    3. [Update environment variables.](#usdGenSchemaCompiledSchemaStep3)
    4. [Run your Usd (capable) application.](#usdGenSchemaCompiledSchemaStep4)


## TL;DR - Schema Creation In-A-Nutshell <a name="summary"></a>
- Generating schemas in Usd is as easy as supplying a customized `schema.usda` file to the `usdGenSchema` commandline tool that ships with Usd. That's right, you don't need to code!
- Custom schemas allow us to create custom prim types/properties/metadata (with fallback values) so that we don't have to repeatedly re-create it ourselves.
- In OOP speak: It allows you to create your own subclasses that nicely fit into Usd and automatically generates all the `Get<PropertyName>`/`Set<PropertyName>` methods, so that it feels like you're using native USD classes.
- We can also create `codeless` schemas, these don't need to be compiled, but we won't get our nice automatically generated getters and setters and schema C++/Python classes.

~~~admonish tip
Codeless schemas are ideal for smaller studios or when you need to prototype a schema. The result only consists of a `plugInfo.json` and `generatedSchema.usda` file and is instantly created without any need for compiling.
~~~

~~~admonish important title="Compiling against USD"
Most DCCs ship with a customized USD build, where most vendors adhere to the [VFX Reference Platform](https://vfxplatform.com/) and only change USD with major version software releases. They do backport important production patches though from time to time. That's why we recommend using the USD build from the DCC instead of trying to self compile and link it to the DCC, as this guarantees the most stability. This does mean though, that you have to compile all plugins against each (major version) releases of each individual DCC.
~~~

## What should I use it for? <a name="usage"></a>
~~~admonish tip
We'll usually want to generate custom schemas, when we want to have a set of properties/metadata that should always exist (with a fallback value) on certain prims. A typical use case for creating an own typed/API schema is storing common render farm settings or shot related data.
~~~

# Resources <a name="resources"></a>
- [API Docs](https://openusd.org/release/api/_usd__page__generating_schemas.html)

## Overview <a name="overview"></a>
For both examples we'll start of with the example schema that USD ships with in its official repo.

You can copy and paste the [content](https://github.com/PixarAnimationStudios/OpenUSD/blob/release/extras/usd/examples/usdSchemaExamples/schema.usda) into a file and then follow along or take the prepared files from [here](https://github.com/LucaScheller/VFX-UsdSurvivalGuide/tree/main/files/plugins/schemas) that ship with this repo.

Our guide focuses on working with Houdini, therefore we use the `usdGenSchema` that ships with Houdini. You can find it in your Houdini /bin directory.
~~~admonish tip title=""
```bash
$HFS/bin/usdGenSchema
# For example on Linux:
/opt/hfs19.5/bin/usdGenSchema
```
~~~

If you download/clone this repo, we ship with .bash scripts that automatically runs all the below steps for you.

You'll first need to `cd` to the root repo dir and then run `./setup.sh`. Make sure that you edit the `setup.sh` file to point to your Houdini version. By default it will be the latest Houdini major release symlink, currently `/opt/hfs19.5`, that Houdini creates on install.

Then follow along the steps as mentioned below.

## Codeless Schema <a name="usdGenSchemaCodelessSchema"></a>
Codeless schemas allow us to generate schemas without any C++/Python bindings. This means your won't get fancy `Schema.Get<PropertyName>`/`Schema.Set<PropertyName>` getters and setters. On the upside you don't need to compile anything. 

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

#### Step 1: Edit 'GLOBAL' prim 'customData' dict <a name="usdGenSchemaCodelessSchemaStep1"></a>
Update the global prim custom data dict from:
~~~admonish tip title=""
```python
over "GLOBAL" (
    customData = {
        string libraryName       = "usdSchemaExamples"
        string libraryPath       = "."
        string libraryPrefix     = "UsdSchemaExamples"
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

~~~admonish info title="Result | Click to expand content" collapsible=true
```python
{{#include ../../../../../files/plugins/schemas/codelessSchema/schema.usda}}
```
~~~

#### Step 2: Run usdGenSchema <a name="usdGenSchemaCodelessSchemaStep2"></a>
Next we need to generate the schema. 

Make sure that you first sourced you Houdini environment by running `$HFS/houdini_setup` so that it find all the correct libraries and python interpreter.

~~~admonish tip title="usdGenSchema on Windows"
On Windows you can also run `hython usdGenSchema schema.usda dst` to avoid having to source the env yourself.
~~~

Then run the following
~~~admonish tip title=""
```bash
cd /path/to/your/schema # In our case: .../VFX-UsdSurvivalGuide/files/plugins/schemas/codelessSchema
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

~~~admonish info title="Result | Click to expand content" collapsible=true
```python
{{#include ../../../../../files/plugins/schemas/codelessSchema/dist/plugInfo.json}}
```
~~~


#### Step 3: Add the generated pluginInfo.json director to 'PXR_PLUGINPATH_NAME' env var. <a name="usdGenSchemaCodelessSchemaStep3"></a>
Next we need to add the pluginInfo.json directory to the `PXR_PLUGINPATH_NAME` environment variable.
~~~admonish tip title=""
```bash
// Linux
export PXR_PLUGINPATH_NAME=/Enter/Path/To/dist:${PXR_PLUGINPATH_NAME}
// Windows
set PXR_PLUGINPATH_NAME=/Enter/Path/To/dist;%PXR_PLUGINPATH_NAME%
```
~~~
If you used the helper bash script, it is already done for us.

#### Step 4: Run your Usd (capable) application. <a name="usdGenSchemaCodelessSchemaStep4"></a>
Yes, that's right! It was that easy. (Puts on sunglass, ah yeeaah! 😎)

If you run Houdini and then create a primitive, you can now choose the `ComplexPrim` as well as assign the `ParamAPI` API schema.

!["test"](../../../media/core/plugins/schemaCodelessHoudini.jpg#center)

Or if you want to test it in Python:
~~~admonish info title=""
```python
{{#include ../../../../../code/core/elements.py:schemasPluginCodelessTest}}
```
~~~

## Compiled Schema <a name="usdGenSchemaCompiledSchema"></a>
Compiled schemas allow us to generate schemas with any C++/Python bindings. This means we'll get `Schema.Get<PropertyName>`/`Schema.Set<PropertyName>` getters and setters automatically which gives our schema a very native Usd feeling. You can then also edit the C++ files to add custom features on top to manipulate the data generated by your schema. This is how many of the schemas that ship with USD do it.

~~~admonish tip title="usdGenSchema on Windows"
Currently these instructions are only tested for Linux. We might add Windows support in the near future. (We use CMake, so in theory it should be possible to run the same steps in Windows too.)
~~~

Let's get started step by step for our example schema. 

We also ship with a `build.sh` for running all the below steps in one go. Make sure you first run the `setup.sh` as described in the [overview](#overview) section and then navigate to the compiledSchema folder.
~~~admonish tip title=""
```bash
cd .../VFX-UsdSurvivalGuide/files/plugins/schemas/compiledSchema
chmod +x build.sh # Add execute rights
source ./build.sh # Run usdGenSchema and source the env vars for the plugin path
```
~~~

This will completely rebuild all directories and set the correct environment variables. You can then go straight to the last step to try it out.

#### Step 1: Run usdGenSchema <a name="usdGenSchemaCompiledSchemaStep1"></a>
First we need to generate the schema. 

Make sure that you first sourced you Houdini environment by running `$HFS/houdini_setup` so that it can find all the correct libraries and python interpreter.

~~~admonish tip title="usdGenSchema on Windows"
On Windows you can also run `hython usdGenSchema schema.usda dst` to avoid having to source the env yourself.
~~~

Then run the following
~~~admonish tip title=""
```bash
cd /path/to/your/schema # In our case: ../VFX-UsdSurvivalGuide/files/plugins/schemas/compiledSchema
rm -R src
usdGenSchema schema.usda src
```
~~~

Currently `usdGenSchema` fails to generate the following files:
- `module.cpp`
- `moduleDeps.cpp`
- `__init__.py`

We needs these for the Python bindings to work, so we supplied them in the `VFX-UsdSurvivalGuide/files/plugins/schemas/compiledSchema/auxiliary` folder of this repo. Simply copy them into the `src` folder after running `usdGenSchema`. 

It does automatically detect the boost namespace, so the generated files will automatically work with Houdini's `hboost` namespace.

~~~admonish important
If you adjust your own schemas, you will have edit the following in these files:
- `module.cpp`: Per user define schema you need to add a line consisting of `TF_WRAP(<SchemaClassName>);`
- `moduleDeps.cpp`: If you add C++ methods, you will need to declare any dependencies what your schemas have. This file also contains the namespace for C++/Python where the class modules will be accessible. We change `RegisterLibrary(TfToken("usdSchemaExamples"), TfToken("pxr.UsdSchemaExamples"), reqs);` to `RegisterLibrary(TfToken("usdSchemaExamples"), TfToken("UsdSchemaExamples"), reqs);` as we don't want to inject into the default pxr namespace for this demo.
~~~

#### Step 2: Compile schema <a name="usdGenSchemaCompiledSchemaStep2"></a>
Next up we need to compile the schema. You can check out our asset resolver guide for more info on [system requirements](https://lucascheller.github.io/VFX-UsdAssetResolver/installation/requirements.html). In short you'll need a recent version of:
- gcc (compiler)
- cmake (build tool).

To compile, we first need to adjust our `CMakeLists.txt` file.

USD actually ships with a `CMakeLists.txt` file in the [examples](https://github.com/PixarAnimationStudios/OpenUSD/blob/release/extras/usd/examples/usdSchemaExamples/CMakeLists.txt) section. It uses some nice USD CMake convenience functions generate the make files.

We are not going to use that one though. Why? Since we are building against Houdini and to make things more explicit, we prefer showing how to explicitly define all headers/libraries ourselves. For that we provide the `CMakeLists.txt` file [here](https://github.com/LucaScheller/VFX-UsdSurvivalGuide/tree/main/files/plugins/schemas/compiledSchema).

Then run the following
~~~admonish tip title=""
```bash
# Clear build & install dirs
rm -R build
rm -R dist
# Build
cmake . -B build
cmake --build build --clean-first # make clean all
cmake --install build             # make install
```
~~~

Here is the content of the CMakeLists.txt file. We might make a CMake intro later, as it is pretty straight forward to setup once you know the basics.

~~~admonish info title="CMakeLists.txt | Click to expand content" collapsible=true
```python
{{#include ../../../../../files/plugins/schemas/compiledSchema/CMakeLists.txt}}
```
~~~

#### Step 3: Update environment variables. <a name="usdGenSchemaCompiledSchemaStep3"></a>
Next we need to update our environment variables. The cmake output log actually has a message that shows what to set:
- `PXR_PLUGINPATH_NAME`: The USD plugin search path variable.
- `PYTHONPATH`: This is the standard Python search path variable.
- `LD_LIBRARY_PATH`: This is the search path variable for how `.so` files are found on Linux.

~~~admonish tip title=""
```bash
// Linux
export PYTHONPATH=..../VFX-UsdSurvivalGuide/files/plugins/schemas/compiledSchema/dist/lib/python:/opt/hfs19.5/python/lib/python3.9/site-packages:$PYTHONPATH
export PXR_PLUGINPATH_NAME=.../VFX-UsdSurvivalGuide/files/plugins/schemas/compiledSchema/dist/resources:$PXR_PLUGINPATH_NAME
export LD_LIBRARY_PATH=.../VFX-UsdSurvivalGuide/files/plugins/schemas/compiledSchema/dist/lib:/python/lib:/dsolib:$LD_LIBRARY_PATH
// Windows
set PYTHONPATH=..../VFX-UsdSurvivalGuide/files/plugins/schemas/compiledSchema/dist/lib/python;/opt/hfs19.5/python/lib/python3.9/site-packages;%PYTHON_PATH%
set PXR_PLUGINPATH_NAME=.../VFX-UsdSurvivalGuide/files/plugins/schemas/compiledSchema/dist/resources;%PXR_PLUGINPATH_NAME%
```
For Windows, specifying the linked .dll search path is different. We'll add more info in the future.
~~~

#### Step 4: Run your Usd (capable) application. <a name="usdGenSchemaCompiledSchemaStep4"></a>
If we now run Houdini and then create a primitive, you can now choose the `ComplexPrim` as well as assign the `ParamAPI` API schema.

![""](../../../media/core/plugins/schemaCodelessHoudini.jpg#center)

Or if you want to test it in Python:
~~~admonish info title=""
```python
{{#include ../../../../../code/core/elements.py:schemasPluginCompiledTest}}
```
~~~

As you can see we now get our nice `Create<PropertyName>`/`Get<PropertyName>`/`Set<PropertyName>` methods as well as full Python exposure to our C++ classes.