
# Prims
For an overview and summary please see the parent [Data Containers](./data_container.md) section.

# Table of contents
1. [Prim Basics](#primBasics)
    1. [Specifier](#primSpecifier)
    2. [Type Name](#primTypeName)
    3. [Kind](#primKind)
    4. [Active](#primActive)
    5. [Metadata](#primMetadata)
    6. [Tokens (Low Level API)](#primTokens)
    7. [Debugging](#primDebugging)
2. [Hierarchy (Parent/Child)](#primHierarchy)
3. [Schemas](#primSchemas)
4. [Composition](#primComposition)
5. [Loading Data (Activation/Visibility)](#primLoading)
6. [Properties (Attributes/Relationships)](#primProperties)


## Overview
The main purpose of a prim is to define and store properties. The prim class itself only stores very little data:
- Path/Name
- A connection to its properties
- Metadata related to composition and schemas as well as core metadata(specifier, typeName, kind,activation, assetInfo, customData) 

This page covers the data on the prim itself, for properties check out this [section](./property.md).

The below examples demonstrate the difference between the higher and lower level API where possible. Some aspects of prims are only available via the high level API, as it acts on composition/stage related aspects. 

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
The Python lower level Sdf.PrimSpec offers quick access to setting common core metadata via standard class instance attributes:
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

over Cube "overCube" ()
{
    double size = 2
}

class Cube "classCube" ()
{
    double size = 2
}
```

This is how it affects traversal:
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimBasicsSpecifierTraversal}}
```
~~~


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
By default stage traversals will skip over `over` only prims. Prims that only have an `over` also do not get forwarded to Hydra render delegates.
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
- We target these class prims via inherits/internal references and specialize [composition arcs](../composition/livrps.md)
~~~

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimBasicsSpecifierClass}}
```
~~~


#### Type Name <a name="primTypeName"></a>
The type name specifies what concrete schema the prim adheres to.
In plain english: Usd has the concept of schemas, which are like OOP classes. Each prim can be an instance of a class, so that it receives the default attributes of that class. More about schemas in our [schemas](./schemas.md) section. You can also have prims without a type name, but in practice you shouldn't do this. For that case USD has an "empty" class that just has all the base attributes called "Scope".

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimBasicsTypeName}}
```
~~~

#### Kind <a name="primKind"></a>
The [kind](https://openusd.org/release/glossary.html#usdglossary-kind) metadata can be attached to prims to mark them what kind hierarchy level it is. This way we can quickly traverse and select parts of the hierarchy that are of interest to us, without traversing into every child prim.

For a full explanation we have a dedicated section: [Kinds](../plugins/kind.md) 

Here is the reference code on how to set kinds. For a practical example with stage traversals, check out the kinds page.
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimBasicsKinds}}
```
~~~

#### Active <a name="primActive"></a>
The `active` metadata controls if the prim and its children are loaded or not.
We only cover here how to set the metadata, for more info checkout our [Loading mechansims](./loading_mechanisms.md) section. Since it is a metadata entry, it can not be animated. For animated pruning we must use [visibility](./property.md#visibility).

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:metadataActive}}
```
~~~

#### Metadata <a name="primMetadata"></a>
We go into more detail about metadata in our [Metadata](./metadata.md) section. 

~~~admonish important
As you can see on this page, most of the prim functionality is actually done via metadata, except path, composition and property related functions/attributes.
~~~

#### Tokens (Low Level API) <a name="primTokens"></a>
Prim (as well as property, attribute and relationship) specs also have the tokens they can set as their metadata as class attributes ending with 'Key'.
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

### Hierarchy (Parent/Child) <a name="primHierarchy"></a>
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

#### Prim Type Definition (High Level)
With the [prim definition](https://openusd.org/dev/api/class_usd_prim_definition.html) we can inspect what the schemas provide. Basically you are inspecting the class (as to the prim being the instance, if we compare it to OOP paradigms).
In production, you won't be using this a lot, it is good to be aware of it though.

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimTypeDefinition}}
```
~~~

#### Prim Type Info (High Level)
The [prim type info](https://openusd.org/dev/api/class_usd_prim_type_info.html) holds the composed type info of a prim. You can think of it as as the class that answers Python `type()` like queries for Usd. It caches the results of type name and applied API schema names, so that `prim.IsA(<typeName>)` checks can be used to see if the prim matches a given type.

~~~admonish tip
The prim's `prim.IsA(<typeName>)` checks are highly performant, you should use them as often as possible when traversing stages to filter what prims you want to edit. Doing property based queries to determine if a prim is of interest to you, is a lot slower.
~~~

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimTypeInfo}}
```
~~~

### Composition <a name="primComposition"></a>
We discuss handling composition in our [Composition](../composition/overview.md) section as it follows some different rules and is a bigger topic to tackle.


### Loading Data (Purpose/Activation/Visibility) <a name="primLoading"></a>
We cover this in detail in our [Loading Data](./loading_mechanisms.md) section.

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimLoading}}
```
~~~

### Properties/Attributes/Relationships <a name="primProperties"></a>
We cover properties in more detail in our [properties](./property.md) section.

~~~admonish important title="Deep Dive | Properties"
Technically properties are also stored as metadata on the `Sdf.PrimSpec`. So later on when we look at composition, keep in mind that the prim stack therefore also drives the property stack. That's why the prim index is on the `prim` level and not on the `property` level.
```python
...
print(prim_spec.properties, prim_spec.attributes, prim_spec.relationships)
print(prim_spec.GetInfo("properties"))
...
```
~~~

Here are the basics for both API levels:

#### High Level API
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimPropertiesHighLevel}}
```
~~~

#### Low Level API
To access properties on `Sdf.PrimSpec`s we can call the `properties`, `attributes`, `relationships` methods. These return a dict with the {'name': spec} data.
Here is an example of what is returned when you create cube with a size attribute:


~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimPropertiesLowLevel}}
```
~~~

~~~admonish important
Since the lower level API doesn't see the schema properties, these commands will only return what is actually in the layer, in Usd speak `authored`.
~~~

With the high level API you can get the same/similar result by calling prim.GetAuthoredAttributes() as you can see above.
When you have multiple layers, the prim.GetAuthoredAttributes(), will give you the created attributes from all layers, where as the low level API only the ones from the active layer.

As mentioned in the `properties` section, properties is the base class, so the `properties` method will give you
the merged dict of the `attributes` and `relationship` dicts.





