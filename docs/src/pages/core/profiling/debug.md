# Debugging
The Usd API ships with a [debug class](https://openusd.org/dev/api/class_tf_debug.html), which allows you to log different messages by setting the `TF_DEBUG` environment variable to one of the symbols. This is useful to see if plugins are loaded or to see if the asset resolver is correctly hooked in.

## TL;DR - Debug In-A-Nutshell
- You can set the `TF_DEBUG` environment variable to one the the values listed below or symbol name from a plugin.
- You can also activate a symbol in the active session via Python: ```pxr.Tf.Debug.SetDebugSymbolsByName("AR_RESOLVER_INIT", True)```

## What should I use it for?
~~~admonish tip
Enabling debug symbols, allows you to inspect specific log outputs of Usd. Typical use cases are to check if plugins are loaded correctly or if data is properly being refreshed.
~~~

## Resources
- [Debug API Docs](https://openusd.org/dev/api/class_tf_debug.html)

## Overview
Environment Variables:

| Name                  | Value                |
|-----------------------|----------------------|
| TF_DEBUG              | 'DEBUG_SYMBOL_NAME'  |
| TF_DEBUG_OUTPUT_FILE  | 'stdout' or 'stderr' |

~~~admonish tip
Activating the log output via bash:
```bash
export TF_DEBUG=AR_RESOLVER_INIT
```
Then launch your app.
~~~
You can also set them interactively in the active session via Python. Wildcarding is allowd to turn on multiple debug symbols in batch.

~~~admonish tip
```python
activated_symbols = pxr.Tf.Debug.SetDebugSymbolsByName("AR_RESOLVER_INIT", True) # Returns: ["AR_RESOLVER_INIT"]
activated_symbols = pxr.Tf.Debug.SetDebugSymbolsByName("AR_*", True)
```
~~~

External plugins (like asset resolvers) often register own debug symbols which you can then use to see exactly what is going on.

To get a list of value `TF_DEBUG`values you can run:
~~~admonish info title=""
```python
{{#include ../../../../../code/core/elements.py:debuggingTokens}}
```
~~~

Full list of debug codes:

| Variable Name | Description |
|----|----|
| AR_RESOLVER_INIT | Print debug output during asset resolver initialization |
| GLF_DEBUG_CONTEXT_CAPS | Glf report when context caps are initialized and dump contents |
| GLF_DEBUG_DUMP_SHADOW_TEXTURES | Glf outputs shadows textures to image files |
| GLF_DEBUG_ERROR_STACKTRACE | Glf dump stack trace on GL error |
| GLF_DEBUG_POST_SURFACE_LIGHTING | Glf post surface lighting setup |
| GLF_DEBUG_SHADOW_TEXTURES | Glf logging for shadow map management |
| GUSD_STAGECACHE | GusdStageCache details. |
| HDST_DISABLE_FRUSTUM_CULLING | Disable view frustum culling |
| HDST_DISABLE_MULTITHREADED_CULLING | Force the use of the single threaded version of frustum culling |
| HDST_DRAW | Reports diagnostics for drawing |
| HDST_DRAWITEMS_CACHE | Reports lookups from the draw items cache. |
| HDST_DRAW_BATCH | Reports diagnostics for draw batches |
| HDST_DRAW_ITEM_GATHER | Reports when draw items are fetched for a render pass. |
| HDST_DUMP_FAILING_SHADER_SOURCE | Print generated shader source code for shaders that fail compilation |
| HDST_DUMP_FAILING_SHADER_SOURCEFILE | Write out generated shader source code to files for shaders that fail compilation |
| HDST_DUMP_GLSLFX_CONFIG | Print composed GLSLFX configuration |
| HDST_DUMP_SHADER_SOURCE | Print generated shader source code |
| HDST_DUMP_SHADER_SOURCEFILE | Write out generated shader source code to files |
| HDST_FORCE_DRAW_BATCH_REBUILD | Forces rebuild of draw batches. |
| HDST_MATERIAL_ADDED | Report when a material is added |
| HDST_MATERIAL_REMOVED | Report when a material is removed |
| HDX_DISABLE_ALPHA_TO_COVERAGE | Disable alpha to coverage transpancy |
| HDX_INTERSECT | Output debug info of intersector |
| HDX_SELECTION_SETUP | Output debug info during creation of selection buffer |
| HD_BPRIM_ADDED | Report when bprims are added |
| HD_BPRIM_REMOVED | Report when bprims are removed |
| HD_BUFFER_ARRAY_INFO | Report detail info of HdBufferArrays |
| HD_BUFFER_ARRAY_RANGE_CLEANED | Report when bufferArrayRange is cleaned |
| HD_CACHE_HITS | Report every cache hit |
| HD_CACHE_MISSES | Report every cache miss |
| HD_COUNTER_CHANGED | Report values when counters change |
| HD_DIRTY_ALL_COLLECTIONS | Reports diagnostics when all collections are marked dirty |
| HD_DIRTY_LIST | Reports dirty list state changes |
| HD_DISABLE_MULTITHREADED_RPRIM_SYNC | Run RPrim sync on a single thread |
| HD_DRAWITEMS_CULLED | Report the number of draw items culled in each render pass |
| HD_ENGINE_PHASE_INFO | Report the execution phase of the Hydra engine |
| HD_EXT_COMPUTATION_ADDED | Report when ExtComputations are added |
| HD_EXT_COMPUTATION_EXECUTION | Report when ExtComputations are executed |
| HD_EXT_COMPUTATION_REMOVED | Report when ExtComputations are removed |
| HD_EXT_COMPUTATION_UPDATED | Report when ExtComputations are updated |
| HD_FREEZE_CULL_FRUSTUM | Freeze the frustum used for culling at it's current value |
| HD_INSTANCER_ADDED | Report when instancers are added |
| HD_INSTANCER_CLEANED | Report when instancers are fully cleaned |
| HD_INSTANCER_REMOVED | Report when instancers are removed |
| HD_INSTANCER_UPDATED | Report when instancers are updated |
| HD_RENDER_SETTINGS | Report render settings changes |
| HD_RPRIM_ADDED | Report when rprims are added |
| HD_RPRIM_CLEANED | Report when rprims are fully cleaned |
| HD_RPRIM_REMOVED | Report when rprims are removed |
| HD_RPRIM_UPDATED | Report when rprims are updated |
| HD_SAFE_MODE | Enable additional security checks |
| HD_SELECTION_UPDATE | Report when selection is updated |
| HD_SHARED_EXT_COMPUTATION_DATA | Report info related to deduplication of ext computation data buffers |
| HD_SPRIM_ADDED | Report when sprims are added |
| HD_SPRIM_REMOVED | Report when sprims are removed |
| HD_SYNC_ALL | Report debugging info for the sync all algorithm. |
| HD_TASK_ADDED | Report when tasks are added |
| HD_TASK_REMOVED | Report when tasks are removed |
| HD_VARYING_STATE | Reports state tracking of varying state |
| HGIGL_DEBUG_ERROR_STACKTRACE | HgiGL dump stack trace on GL error |
| HGIGL_DEBUG_FRAMEBUFFER_CACHE | Debug framebuffer cache management per context arena. |
| HGI_DEBUG_DEVICE_CAPABILITIES | Hgi report when device capabilities are initialized and dump contents |
| HIO_DEBUG_DICTIONARY | glslfx dictionary parsing |
| HIO_DEBUG_FIELD_TEXTURE_DATA_PLUGINS | Hio field texture data plugin registration and loading |
| HIO_DEBUG_GLSLFX | Hio GLSLFX info |
| HIO_DEBUG_TEXTURE_IMAGE_PLUGINS | Hio image texture plugin registration and loading |
| NDR_DEBUG | Advanced debugging for Node Definition Registry |
| NDR_DISCOVERY | Diagnostics from discovering nodes for Node Definition Registry |
| NDR_INFO | Advisory information for Node Definition Registry |
| NDR_PARSING | Diagnostics from parsing nodes for Node Definition Registry |
| NDR_STATS | Statistics for registries derived from NdrRegistry |
| PCP_CHANGES | Pcp change processing |
| PCP_DEPENDENCIES | Pcp dependencies |
| PCP_NAMESPACE_EDIT | Pcp namespace edits |
| PCP_PRIM_INDEX | Print debug output to terminal during prim indexing |
| PCP_PRIM_INDEX_GRAPHS | Write graphviz 'dot' files during prim indexing (requires PCP_PRIM_INDEX) |
| PLUG_INFO_SEARCH | Plugin info file search |
| PLUG_LOAD | Plugin loading |
| PLUG_LOAD_IN_SECONDARY_THREAD | Plugins loaded from non-main threads |
| PLUG_REGISTRATION | Plugin registration |
| SDF_ASSET | Sdf asset resolution |
| SDF_ASSET_TRACE_INVALID_CONTEXT | Post stack trace when opening an SdfLayer with no path resolver context |
| SDF_CHANGES | Sdf change notification |
| SDF_FILE_FORMAT | Sdf file format plugins |
| SDF_LAYER | SdfLayer loading and lifetime |
| SDR_TYPE_CONFORMANCE | Diagnostcs from parsing and conforming default values for Sdr and Sdf type conformance |
| TF_ATTACH_DEBUGGER_ON_ERROR | attach/stop in a debugger for all errors |
| TF_ATTACH_DEBUGGER_ON_FATAL_ERROR | attach/stop in a debugger for fatal errors |
| TF_ATTACH_DEBUGGER_ON_WARNING | attach/stop in a debugger for all warnings |
| TF_DEBUG_REGISTRY | debug the TfDebug registry |
| TF_DISCOVERY_DETAILED | detailed debugging of TfRegistryManager |
| TF_DISCOVERY_TERSE | coarse grain debugging of TfRegistryManager |
| TF_DLCLOSE | show files closed by TfDlclose |
| TF_DLOPEN | show files opened by TfDlopen |
| TF_ERROR_MARK_TRACKING | capture stack traces at TfErrorMark ctor/dtor, enable TfReportActiveMarks debugging API. |
| TF_LOG_STACK_TRACE_ON_ERROR | log stack traces for all errors |
| TF_LOG_STACK_TRACE_ON_WARNING | log stack traces for all warnings |
| TF_PRINT_ALL_POSTED_ERRORS_TO_STDERR | print all posted errors immediately, meaning that even errors that are expected and handled will be printed, producing possibly confusing output |
| TF_SCRIPT_MODULE_LOADER | show script module loading activity |
| TF_TYPE_REGISTRY | show changes to the TfType registry |
| USDGEOM_BBOX | UsdGeom bounding box computation |
| USDGEOM_EXTENT | Reports when Boundable extents are computed dynamically because no cached authored attribute is present in the scene. |
| USDIMAGING_CHANGES | Report change processing events |
| USDIMAGING_COLLECTIONS | Report collection queries |
| USDIMAGING_COMPUTATIONS | Report Hydra computation usage in usdImaging. |
| USDIMAGING_COORDSYS | Coordinate systems |
| USDIMAGING_INSTANCER | Report instancer messages |
| USDIMAGING_PLUGINS | Report plugin status messages |
| USDIMAGING_POINT_INSTANCER_PROTO_CREATED | Report PI prototype stats as they are created |
| USDIMAGING_POINT_INSTANCER_PROTO_CULLING | Report PI culling debug info |
| USDIMAGING_POPULATION | Report population events |
| USDIMAGING_SELECTION | Report selection messages |
| USDIMAGING_SHADERS | Report shader status messages |
| USDIMAGING_TEXTURES | Report texture status messages |
| USDIMAGING_UPDATES | Report non-authored, time-varying data changes |
| USDMTLX_READER | UsdMtlx reader details |
| USDSKEL_BAKESKINNING | UsdSkelBakeSkinningLBS() method. |
| USDSKEL_CACHE | UsdSkel cache population. |
| USDUTILS_CREATE_USDZ_PACKAGE | UsdUtils USDZ package creation details |
| USD_AUTO_APPLY_API_SCHEMAS | USD API schema auto application details |
| USD_CHANGES | USD change processing |
| USD_CLIPS | USD clip details |
| USD_COMPOSITION | USD composition details |
| USD_DATA_BD | USD BD file format traces |
| USD_DATA_BD_TRY | USD BD call traces. Prints names, errors and results. |
| USD_INSTANCING | USD instancing diagnostics |
| USD_PATH_RESOLUTION | USD path resolution diagnostics |
| USD_PAYLOADS | USD payload load/unload messages |
| USD_PRIM_LIFETIMES | USD prim ctor/dtor messages |
| USD_SCHEMA_REGISTRATION | USD schema registration details. |
| USD_STAGE_CACHE | USD stage cache details |
| USD_STAGE_INSTANTIATION_TIME | USD stage instantiation timing |
| USD_STAGE_LIFETIMES | USD stage ctor/dtor messages |
| USD_STAGE_OPEN | USD stage opening details |
| USD_VALIDATE_VARIABILITY | USD attribute variability validation |
| USD_VALUE_RESOLUTION | USD trace of layers inspected as values are resolved |

You scrolled all the way to the end 🥳. Congratulations, you have now earned the rank of "Usd Nerd"!