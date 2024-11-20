# Metadata
USD allows us to extend the base metadata that is attached to every layer, prim and property (Supported are `Sdf.Layer` and subclasses of `Sdf.Spec`). This allows us to write custom fields with a specific type, so that we don't have to rely on writing everything into the `assetInfo` and `customData` entries.

To get an overview of metadata in USD, check out our dedicated [metadata section](../elements/metadata.md).

# Table of Contents
1. [Metadata Plugins In-A-Nutshell](#summary)
1. [What should I use it for?](#usage)
1. [Resources](#resources)
1. [Overview](#overview)
    1. [Installing a metadata plugin](#metadataPluginInstall)
    1. [Reading/Writing the installed custom metadata](#metadataPluginReadWrite)

## TL;DR - Metadata Plugins In-A-Nutshell <a name="summary"></a>
- Extending USD with custom metadata fields is as simple as creating a `plugInfo.json` file with entires for what custom fields you want and on what entities (Supported are `Sdf.Layer` and subclasses of `Sdf.Spec`). 

## What should I use it for? <a name="usage"></a>
~~~admonish tip
In production, most of the sidecar metadata should be tracked via the `assetInfo` and `customData` metadata entries. It does make sense to extend the functionality with own metadata keys for:
- Doing high performance lookups. Metadata is fast to read, as it follows simpler composition rules, so we can use it as a `IsA` replacement mechanism we can tag our prims/properties with.
- We can add [list editable ops](../composition/listeditableops.md) metadata fields, this can be used as a way to layer together different array sidecar data. For an example see our [Reading/Writing the installed custom metadata](#metadataPluginReadWrite) section.
~~~

## Resources
- [USD Survival Guide - Metadata](../elements/metadata.md)
- [USD API - Metadata](https://openusd.org/release/api/sdf_page_front.html#sdf_plugin_metadata)
- [USD Cookbook - Extending Metadata](https://github.com/ColinKennedy/USD-Cookbook/blob/master/references/working_with_plugins.md#Extend-Metadata) 

## Overview <a name="overview"></a>
Here is the minimal plugin template with all options you can configure for your metadata:
~~~admonish info title=""
```json
{
   "Plugins": [
       {
           "Name": "<PluginName>",
           "Type": "resource",
           "Info": {
               "SdfMetadata": {
                    "<field_name>" : {
                        "appliesTo": "<Optional comma-separated list of spec types this field applies to>",
                        "default": "<Optional default value for field>",
                        "displayGroup": "<Optional name of associated display group>",
                        "type": "<Required name indicating field type>",
                    }
               }
           }
       }
   ]
}
```
~~~


We can limit the metadata entry to the following `Sdf.Layer`/Subclasses of `Sdf.Spec`s with the `type` entry:

| "appliesTo" token	| Spec type                    |
|-------------------|------------------------------|
| layers	        | SdfLayer (SdfPseudoRootSpec) |
| prims	            | SdfPrimSpec, SdfVariantSpec  |
| properties	    | SdfPropertySpec              |
| attributes	    | SdfAttributeSpec             |
| relationships	    | SdfRelationshipSpec          |
| variants          | SdfVariantSpec               |

You can find all the supported data types on this page in the official docs: [USD Cookbook - Extending Metadata](https://openusd.org/release/api/sdf_page_front.html#sdf_plugin_metadata).

### Installing a metadata plugin <a name="metadataPluginInstall"></a>

Here is an example `plugInfo.json` file for metadata, it also ships with this repo [here](https://github.com/LucaScheller/VFX-UsdSurvivalGuide/tree/main/files/plugins/metadata).
~~~admonish info title=""
```python
{{#include ../../../../../files/plugins/metadata/plugInfo.json}}
```
~~~

To register the above metadata plugin, copy the contents into a file called `plugInfo.json`. Then set your `PXR_PLUGINPATH_NAME` environment variable to the folder containing the `plugInfo.json` file.

For Linux this can be done for the active shell as follows:
```bash
export PXR_PLUGINPATH_NAME=/my/cool/plugin/resources:${PXR_PLUGINPATH_NAME}
```

If you downloaded this repo, we provide the above example metadata plugin [here](https://github.com/LucaScheller/VFX-UsdSurvivalGuide/tree/main/files/plugins/metadata). All you need to do is point the environment variable there and launch a USD capable application.


### Reading/Writing the installed custom metadata <a name="metadataPluginReadWrite"></a>
Once the plugin is loaded, we can now read and write to the custom entry.

Custom metadata fields on the `Sdf.Layer` are not exposed via Python (as far as we could find).

~~~admonish info title=""
```python
{{#include ../../../../../code/core/elements.py:metadataPlugin}}
```
~~~