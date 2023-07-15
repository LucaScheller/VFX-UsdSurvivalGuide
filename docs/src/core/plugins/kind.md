# Kinds
The [kind](https://openusd.org/release/glossary.html#usdglossary-kind) metadata is a special metadata entry on prims that can be written  to mark prims with data what hierarchy level type it is. This way we can quickly traverse and select parts of the hierarchy that are of interest to us, without traversing into every child prim. The most common types are `component` and `group`. We use these (or sub-kinds) of these to make our stage more easily browse-able, so that we can visually/programmatically easily detect where assets start.

# Table of contents
1. [Kinds In-A-Nutshell](#summary)
2. [What should I use it for?](#usage)
3. [Resources](#resources)
4. [Overview](#overview)
    1. [Reading and Writing Kinds](#kindAuthoring)
    2. [Special Paths: emptyPath & absoluteRootPath](#pathSpecialPaths)
    3. [Variants ](#pathVariants)
    4. [Properties](#pathProperties)

## TL;DR - Kinds In-A-Nutshell <a name="summary"></a>
~~~admonish tip
The kind metadata is mainly used to for two things:
- Traversal: You can quickly detect (and stop traversal to children) where the assets are in your hierarchy by marking them as a a `model` subtype like `component`. A typical use case would be "find me all `fx` assets": In your pipeline you would define a 'fx' model kind subtype and then you can traverse for all prims that have the 'fx' kind set.
- DCCs use this to drive user selection in UIs. This way we can quickly select non-leaf prims that are of interest. For example to transform an asset in the hierarchy, we only want to select the asset root prim and not its children, so we can tell our DCC to select only `model` kind prims. This will limit the selection to all sub-kinds of `model`.
~~~

## What should I use it for? <a name="usage"></a>
~~~admonish tip
In production, you'll use kinds as a way to filter prims when looking for data. As kind data is written in prim metadata, it is very fast to access and suited for high performance queries/traversals. For more info on traversals, take a look at the [traversal]() section.
~~~
~~~admonish important
You should always tag all prims in the hierarchy with kinds at least to the asset level. Some DCCs will otherwise not traverse into the hierarchy if they come across a prim without a kind being set.
So this means you should have at least `group` kind metadata set for all parent prims of `model` sub-kind prims.
~~~

## Resources
- [Kind Glossary Definition](https://openusd.org/release/glossary.html#usdglossary-kind)
- [Extending Kinds](https://openusd.org/dev/api/kind_page_front.html#kind_extensions)
- [Kind Registry](https://openusd.org/dev/api/class_kind_registry.html) 

## Overview <a name="overview"></a>
Usd ships with these kinds by default, to register your own kinds, see the below examples for more details:
- `model`: The base kind for all model kinds, don't use it directly.
    - `component`: A sub-kind of 'model' that has no other child prims of type 'model'
        - `subcomponent`: An important subhierarchy of an component.
- `assembly`: A collection of model prims, typically used for sets/a assembled collection of models or environments.
- `group`: A group of model prims.

~~~admonish important
You should always tag all prims with kinds at least to the asset level in the hierarchy. Some DCCs will otherwise not traverse into the hierarchy if they come across a prim without a hierarchy.
So this means you should have `group` kinds set for all parent prims of `model` prims.
~~~

### Reading and Writing Kinds <a name="kindAuthoring"></a>
Kinds can be easily set via the high and low level APIs:
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:dataContainerPrimBasicsKinds}}
```
~~~