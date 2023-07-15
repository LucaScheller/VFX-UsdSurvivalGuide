
### Prims

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimOverview}}
```
~~~

# Table of contents
1. [API Overview In-A-Nutshell](#summary)
2. [What should I use it for?](#usage)
3. [Resources](#resources)
4. [Overview](#overview)
    1. [Prim Basics](#primBasics)
        1. [Specifier](#primSpecifier)
        2. [Type Name](#primTypeName)
        3. [Kind](#primKind)
        4. [Metadata](#primMetadata)
        5. [Tokens (Low Level API)](#primTokens)
        6. [Debugging](#primDebugging)
    2. [Hierarchy (Parent/Child/Iteration)](#primHierarchy)
    3. [Schemas](#primSchemas)
    4. [Composition](#primComposition)
        1. [Instancing]()
    5. [Population (Loading Data)](#pathProperties)
    6. [Properties (Attributes/Relationships)]
    

## Overview
Let's look at the details of prims. The below examples demonstrate the difference between the higher and lower level API where possible. Some aspects of prims are only available via the high level API, as it acts on composition/stage related aspects. 

~~~admonish warning title=""
There is a lot of code duplication in the below examples, so that each example works by itself. In practice editing data is very concise and simple to read, so don't get overwhelmed by all the examples.
~~~

### Prim Basics <a name="primBasics"></a>
Setting core metadata via the high level is not all exposed on the prim itself via getters/setters, instead
the getters/setters come in part from schemas or schema APIs. For example setting the kind is done via the Usd.ModelAPI.

##### High Level
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimCoreHighLevel}}
```
~~~

We are also a few "shortcuts" that check specifiers/kinds (`.IsAbstract`, `.IsDefined`, `.IsGroup`, `.IsModel`), more about these in the kind section below.

##### Low Level
The Python lower level Sdf.PrimSpec offers quick access to setting common core metadata via standard class attributes:
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimCoreLowLevel}}
```
~~~

We will look at specifics in the below examples, so don't worry if you didn't understand everything just yet :)


#### Specifiers <a name="primSpecifier"></a>
Usd has the concept of [specifiers](https://openusd.org/release/glossary.html#usdglossary-specifier). 

~~~admonish important
The job of specifiers is mainly to define if a prim should be visible to hierarchy traversals. More info about traversals in our [Layer & Stage](./layer.md) section.
~~~

Here is an example USD ascii file with all three specifiers.
```json
def Cube "definedCube" ()
{
    double size = 2
}

over Cube "overedCube" ()
{
    double size = 2
}

class Cube "classCube" ()
{
    double size = 2
}
```

##### Sdf.SpecifierDef: `def`(define)
This specifier is used to specify a prim in a hierarchy, so that is it always visible to traversals.
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimBasicsSpecifierDef}}
```
~~~

##### Sdf.SpecifierOver: `over`
Prims defined with `over` only get loaded if the prim in another layer has been specified with a `def`specified. It gets used when you want to add data to an existing hierarchy, for example layering only position and normals data onto a character model, where the base model has all the static attributes like topology or UVs.

~~~admonish important
By default stage traversals will skip over `over` only prims.
~~~

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimBasicsSpecifierOver}}
```
~~~

##### Sdf.SpecifierClass: `class`
The `class` specifier gets used to define "template" hierarchies that can then get attached to other prims. A typical example would be to create a set of geometry render settings that then get applied to different parts of the scene by creating an inherit composition arc. This way you have a single control point if you want to adjust settings that then instantly get reflected across your whole hierarchy. 

~~~admonish important
- By default stage traversals will skip over `class` prims.
- Usd refers to class prims as "abstract", as they never directly contribute to the hierarchy.
~~~

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimBasicsSpecifierClass}}
```
~~~


#### Type Name <a name="primTypeName"></a>
The type name specifies what concrete schema the prim adheres to.
In plain english: Usd has the concept of schemas, which are like OOP classes. Each prim can be an instance of a class, so that it receives the default attributes of that class. More about schemas in our [schemas]() section. You can also have prims without a type name, but in practice you shouldn't do this. For that case USD has an "empty" class that just has all the base attributes called "Scope".

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimBasicsTypeName}}
```
~~~

#### Kind <a name="primKind"></a>
The [kind](https://openusd.org/release/glossary.html#usdglossary-kind) metadata can be attached to prims to mark them what kind hierarchy level it is. This way we can quickly traverse and select parts of the hierarchy that are of interest to us, without traversing into every child prim.

~~~admonish tip
The kind metadata is mainly used to for two things:
- Traversal: You can quickly detect (and stop traversal to children) where the assets are in your hierarchy by marking them as a a `model` subtype like `component`. A typical usd case would be "find me all `fx` assets".
- DCCs use this to drive user selection in UIs. This way we can quickly select non-leaf prims, for example to transform an asset in the hierarchy with all its child prims.   
~~~

Usd ships with these kinds by default, you can easily register your own kinds, see our [kind](../plugins/kind.md) section for more details:
- `model`: The base kind for all model kinds, don't use it directly.
    - `component`: A model that has no model child prims.
        - `subcomponent`: An important subhierarchy of an component.
- `assembly`: A collection of model prims, typically used for sets/a assembled collection of models or environments.
- `group`: A group of model prims.

~~~admonish important
You should always tag all prims with kinds at least to the asset level in the hierarchy. Some DCCs will otherwise not traverse into the hierarchy if they come across a prim without a hierarchy.
So this means you should have `group` kinds set for all parent prims of `model` prims.
~~~

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimBasicsKinds}}
```
~~~

#### Metadata <a name="primMetadata"></a>
We go into more detail about metadata in our [Metadata](./metadata.md) section. 

~~~admonish important
As you can see on this page, most of the prim functionality is actually done via metadata, except path, composition and property related functions/attributes.
~~~

#### Tokens (Low Level API) <a name="primTokens"></a>
Prim(property, attribute and relationship specs) also have the tokens they can set as their metadata as class attributes ending with 'Key'.
These 'Key' attributes are the token names that can be set on the spec via `SetInfo`, for example prim_spec.SetInfo(prim_spec.KindKey, "group")
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimBasicsTokens}}
```
~~~

#### Debugging (Low Level API) <a name="primDebugging"></a>
You can also print a spec as its ascii representation (as it would be written to .usda files):
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimBasicsDebugging}}
```
~~~

### Hierarchy (Parent/Child/Iteration) <a name="primHierarchy"></a>
From any prim you can navigate to its hierarchy neighbors via the path related methods.
The lower level API is dict based when accessing children, the high level API returns iterators or lists.
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimHierarchy}}
```
~~~

### Schemas <a name="primSchemas"></a>

We explain in more detail what schemas are in our [schemas](./schemas.md) section.
In short: They are the "base classes" of Usd. Applied schemas are schemas that don't 
define the prim type and instead just "apply" (provide values) for specific metadata/properties

~~~admonish important
The 'IsA' check is a very valueable check to see if something is an instance of a (base) class. It is similar to Python's isinstance method.
~~~

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimSchemas}}
```
~~~

We can also get data about the [prim definition](https://openusd.org/dev/api/class_usd_prim_definition.html) and [prim type info](https://openusd.org/dev/api/class_usd_prim_type_info.html).


#### Prim Type Definition
With the prim type definition you can inspect what the schemas provide. Basically you are inspecting the class (as to the prim being the instance, if we compare it to OOP paradigms).
In production, you won't be using this a lot, it is good to be aware of it though.

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimTypeDefinition}}
```
~~~

#### Prim Type Info
The prim type info holds the composed type info of a prim. You can think of it as as the class that answers Python `type()` like queries for Usd. It caches the results of type name and applied API schema names, so that `prim.IsA(<typeName>)` checks can be used to see if the prim matches a given type.

~~~admonish tip
The prim's `prim.IsA(<typeName>)` checks are highly performant, you should use them as often as possible when traversing stages to filter what prims you want to edit. Doing property based queries to determine if a prim is of interest to you, is a lot slower.
~~~

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimTypeInfo}}
```
~~~


### Composition <a name="primComposition"></a>
We discuss handling composition in our [Composition] seciton as it follows some different rules and is a bigger topic to tackle.

#### Inherits:
- 'inheritPathList' 
#### Variants
-- 'variantSelections', 'BlockVariantSelection', 'GetVariantNames'
-- 'variantSets', 'variantSetNameList',
#### References
- 'hasReferences', 'referenceList', 'ClearReferenceList'
#### Payloads
- 'hasPayloads', 'payloadList', 'ClearPayloadList'
#### Specialize
- 'specializesList',





## Population
We cover this in detail in our [Population]() section.
# Has: 'HasAuthoredActive', 'HasAuthoredHidden'
# Get: 'IsActive', 'IsLoaded', 'IsHidden'
# Set: 'SetActive', 'SetHidden' 
# Clear: 'ClearActive', 'ClearHidden'
# Loading: 'Load', 'Unload'

The `active` and `hidden` (UI hidden) is metadata, the loading state is actually tracked via the stage and just exposed here as convenience.
```
<Add example of actual stage call> 
```



## Composition (High Level API)
We

# Has: 'HasAuthoredInherits', 'HasVariantSets', 'HasAuthoredReferences', 'HasPayload', 'HasAuthoredPayloads'
# Get: 'GetInherits', 'GetTypeName', 'GetReferences', 'GetPayloads'
# Set: 'SetPayload', 'SetTypeName', 'GetSpecializes', 'HasAuthoredSpecializes'
# Clear: 'ClearPayload', 'ClearDocumentation'




#### Composition Instancing/Instanceable prims
We cover instancing in our [Instancing] section.
##### Instanceable Prims
# Has: IsInstanceable', HasAuthoredInstanceable',
# Get: 'GetInstances'
# Set: 'SetInstanceable'
# Clear: 'ClearInstanceable'

To check if our prim in a prototype (Usd speak for 'hiearchy that gets duplicated')

##### Prototypes
# Has: 'IsInPrototype', 'IsPathInPrototype',  'IsPrototype',  'IsInstance',  'IsInstanceProxy', 'IsPrototypePath'
# Get: 'GetPrimInPrototype', 'GetPrototype'
 
 



#### Composition Internals
To query data about composition, we have to go through the high level Usd API first, as the Sdf low level API is not aware of composition related data.
The high level Usd API then queries into the low level Pcp (Prim cache population) API, which tracks all composition related data and builds a value resolution index, 
in simple terms: A stack of layers per spec (prim/property) that knows about all the value sources (layers) a value can come from. Once a value is requested, the highest layer in the stack wins and returns the value.
We cover more about this topic in our [Pcp]() section and our query cache sections.


```python
from pxr import Sdf, Usd
# Create stage with two different layers
stage = Usd.Stage.CreateInMemory()
root_layer = stage.GetRootLayer()
layer_top = Sdf.Layer.CreateAnonymous("exampleTopLayer")
layer_bottom = Sdf.Layer.CreateAnonymous("exampleBottomLayer")
root_layer.subLayerPaths.append(layer_top.identifier)
root_layer.subLayerPaths.append(layer_bottom.identifier)
# Define specs in two different layers
prim_path = Sdf.Path("/cube")
stage.SetEditTarget(layer_top)
prim = stage.DefinePrim(prim_path, "Xform")
prim.SetTypeName("Cube")
stage.SetEditTarget(layer_bottom)
prim = stage.DefinePrim(prim_path, "Xform")
prim.SetTypeName("Cube")
# Print the stack (set of layers that contribute data to this prim)
print(prim.GetPrimStack()) # Returns: [Sdf.Find('anon:0x7f6e590dc300:exampleTopLayer', '/cube'), Sdf.Find('anon:0x7f6e590dc580:exampleBottomLayer', '/cube')]
print(prim.GetPrimIndex()) # More on this in our [Pcp section]()
print(prim.ComputeExpandedPrimIndex()) # More on this in our [Pcp section](). you'll always want to use the expanded version, otherwise you might miss some data sources!
```








## Path related



## Properties
'HasProperty','RemoveProperty',    'GetProperties' 'GetProperty', 'GetPropertiesInNamespace', 'GetPropertyNames', 'GetAuthoredProperties', 'GetAuthoredPropertiesInNamespace', 'GetAuthoredPropertyNames',
'HasAttribute', 'GetAttribute', 'CreateAttribute', 'GetAttributes', 'GetAuthoredAttributes',
'CreateRelationship', 'GetRelationships', 'GetAuthoredRelationships', 'GetRelationship'  'HasRelationship',

 'FindAllAttributeConnectionPaths', 'FindAllRelationshipTargetPaths',





### Properties/Attributes/Relationships
To access the prim_specs properties we can call the `properties`, `attributes`, `relationships` methods. These return a dict with the {'name': spec} data.
Here is an example of what is returned when you create cube with a size attribute:
```
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/cube")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
attr_spec = Sdf.AttributeSpec(prim_spec, "size", Sdf.ValueTypeNames.Float)
print(prim_spec.attributes) # Returns: {'size': Sdf.Find('anon:0x7f6efe199480:LOP:/stage/python', '/cube.size')}
```
Since the lower level API doesn't see the schema properties, these commands will only return what is actually in the layer, in Usd speak `authored`.
With the high level API you can get the same/similar result by calling prim.GetAuthoredAttributes(), this will return all authored attributes though
(not just the one in you active layer).

As mentioned in the `properties`,`attributes`, `relationships` section, properties is the base class, so the `properties` method will give you
the merged dict of the `attributes` and `relationship` dicts.

To remove a property you can run:
```
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/cube")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
attr_spec = Sdf.AttributeSpec(prim_spec, "size", Sdf.ValueTypeNames.Float)
prim_spec.RemoveProperty(attr_spec)
```


