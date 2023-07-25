# Composition Strength Ordering (LIVRPS)
In this section we'll cover how composition arcs work and interact with each other. We cover how to create composition arcs via code in our [composition arcs](./arcs.md) section. This section will also have code examples, but with the focus on practical usage instead of API structure.

~~~admonish tip
We have a supplementary Houdini scene, that you can follow along with, available in this [site's repository]().

~~~

# Table of contents
1. [Composition Strength Ordering In-A-Nutshell](#summary)
1. [What should I use it for?](#usage)
1. [Resources](#resources)
1. [Overview](#overview)
1. [Composition Strength Ordering](#compositionStrengthOrdering)
1. [Composition Arc Categories](#compositionArcCategory)
    1. [Composition Arc By Use Case](#compositionArcCategoryByUseCase)
    1. [Composition Arc By Time Offset/Scale Capability](#compositionArcCategoryByTimeOffset)
    1. [Composition Arc By Target Type (File/Hierarchy)](#compositionArcCategoryByTargetType)
1. [Composition Arcs](#compositionArcs)
    1. [Sublayers / Local Opinions](#compositionArcSublayer)
        1. [Value Clips](#compositionArcValueClips)
    1. [Inherits](#compositionArcInherit)
    1. [Variants](#compositionArcVariant)
    1. [References](#compositionArcReference)
        1. [References File](#compositionArcReferenceExternal)
        1. [References Internal](#compositionArcReferenceInternal)
    1. [Payloads](#compositionArcPayload)
    1. [Specializes](#compositionArcSpecialize)

## TL;DR - Composition Arcs In-A-Nutshell <a name="summary"></a>
- ToDo

## What should I use it for? <a name="usage"></a>
~~~admonish tip
We'll be using composition arcs to load data from different files and hierarchy locations. This is the core mechanism that makes USD powerful, as we can layer/combine our layers in meaningful ways.
~~~

## Resources <a name="resources"></a>
- [Example]()

## Overview <a name="overview"></a>
USD's composition arcs each fulfill a different purpose. As we can attach attach all arcs (except sublayers) to any part of the hierarchy other than the pseudo root prim. When loading our data, we have a pre-defined load order of how arcs prioritize against each other. Each prim (and property) in our hierarchy then gets resolved (see our [Inspecting Compositon](./pcp.md) section) based on this order rule set and the outcome is a (or multiple) value sources, that answer data queries into our hierarchy.

All arcs, except the `sublayer` arc, target (load) a specific prim of a layer (stack). This allows us to rename the prim, where the arc is created on, to something different, than what the arc's source hierarchy prim is named. An essential task that USD performs for us, is mapping paths from the target layer to the source layer (stack).

## Composition Strength Ordering <a name="compositionStrengthOrdering"></a>
To prioritize how different arcs evaluate against each other, we have `composition strength ordering`. This is a fancy word for "what layer (file) provides the actual value for my prim/property/metadata based on all available composition arcs". (I think we'll stick to using `composition strength ordering` 😉).

All arcs, except sublayers, make use of list editing, see our [fundamentals](./fundamentals.md#compositionFundamentalsListEditableOps) for a detailed explanation. We highly recommend reading it first before continuing.

Let's look at the order:

![LIVRPS Order Visualized](compositionLIVRPS.svg)
~~~admonish quote title="Credits"
All credits for this info graphic go to [Remedy-Entertainment - Book Of USD](https://remedy-entertainment.github.io/USDBook/terminology/LIVRPS.html). Check out their site, it is another great value source for USD.
~~~

USD refers to this with the acronym `L(V)IVRPS(F)`:
- **L**ocal: Search for [direct opinions](https://openusd.org/release/glossary.html#direct-opinion) in the active root layer stack. 
    - **V**alue Clips: Search for [direct opinions](https://openusd.org/release/glossary.html#direct-opinion) from value clips. These are weaker than direct opinions on layers.
- **I**nherits: Search for inherits affecting the path. This searches in the (nested) layer stack by recursively applying *LIVRP* (No specializes) evaluation.
- **V**ariant Sets: Search for variants affecting the path. This searches in the (nested) layer stack by recursively applying *LIVRP* (No specializes) evaluation.
- **R**eferences: Search for references affecting the path. This searches in the (nested) layer stack by recursively applying *LIVRP* (No specializes) evaluation.
- **P**ayloads: Search for payloads affecting the path. This searches in the (nested) layer stack by recursively applying *LIVRP* (No specializes) evaluation.
- **S**pecializes: Search for payloads affecting the path. This searches in the (nested) layer stack by recursively applying full *LIVRPS* evaluation. This causes the specialize opinions to always be last.
- **(F)** allback value: Look for [schema](../elements/schemas.md) fallbacks.


Now if you just didn't understand any of that, don't worry! We'll have a look where what are is typically used in the examples below.

~~~admonish important title="Important | Nested Composition Arc Resolve Order"
When resolving nested composition arcs and value clips, the arc/value clip metadata, that is authored on the closest ancestor parent prim or the prim itself, wins. In short to quote from the USD glossary `“ancestral arcs” are weaker than “direct arcs”`. To make our lives easier, we recommend having predefined locations where you author composition arcs. A typical location is your asset root prim and a set/assembly root prim.
~~~

## Composition Arc Categories <a name="compositionArcCategory"></a>
Let's try looking at arcs from a use case perspective. Depending on what we want to achieve, we usually end up with a specific arc designed to fill our needs.

### Composition Arc By Use Case <a name="compositionArcCategoryByUseCase"></a>
Here is a comparison between arcs by use case. Note that this is only a very "rough" overview, there are a few more things to pay attention to when picking the correct arc. It does help to first understand what the different arcs try to achieve though.

~~~admonish tip title=""
```mermaid
flowchart LR
    userRoot(["I want to load"])
    userExternal(["a file (with a time offset/scale)"])
    userExternalWholeLayer(["with the whole content (that is light weight and links to other files)"])
    userExternalHierarchyInLayer(["with only a specific part of its hierarchy (to a specific path in the stage)"])
    userExternalHierarchyInLayerHeavyData(["thats contains a lot of heavy data"])
    userExternalHierarchyInLayerLightData(["thats contains light weight data"])
    userInternal(["an existing sub-hierarchy in the active layer stack/stage"])
    userInternalTimeOffset(["into a new hierarchy location (with a time offset/scale)"])
    userInternalOverride(["to add overrides to multiple (instanced) prims"])
    userInternalBaseValues(["to act as the base-line values that can be overriden by higher layers and arcs"])
    userInternalVariation(["as a variation of the hierarchy"])

    compositionArcSublayer(["Sublayer"])
    compositionArcInherit(["Inherit"])
    compositionArcVariant(["Variant"])
    compositionArcReferenceFile(["Reference"])
    compositionArcReferenceInternal(["Reference"])
    compositionArcPayload(["Payload"])
    compositionArcSpecialize(["Specialize"])
    style compositionArcSublayer fill:#63beff
    style compositionArcInherit fill:#63beff
    style compositionArcVariant fill:#63beff
    style compositionArcReferenceFile fill:#63beff
    style compositionArcReferenceInternal fill:#63beff
    style compositionArcPayload fill:#63beff
    style compositionArcSpecialize fill:#63beff

    userRoot --> userExternal
    userExternal --> userExternalWholeLayer
    userExternal --> userExternalHierarchyInLayer
    userExternalWholeLayer --> compositionArcSublayer
    userExternalHierarchyInLayer --> userExternalHierarchyInLayerHeavyData
    userExternalHierarchyInLayer --> userExternalHierarchyInLayerLightData
    userExternalHierarchyInLayerLightData --> compositionArcReferenceFile
    userExternalHierarchyInLayerHeavyData --> compositionArcPayload
    userRoot --> userInternal
    userInternal --> userInternalTimeOffset
    userInternalTimeOffset --> compositionArcReferenceInternal
    userInternal --> userInternalOverride
    userInternalOverride --> compositionArcInherit
    userInternal --> userInternalBaseValues
    userInternalBaseValues --> compositionArcSpecialize
    userInternal --> userInternalVariation
    userInternalVariation --> compositionArcVariant
```
~~~

### Composition Arc By Time Offset/Scale Capability <a name="compositionArcCategoryByTimeOffset"></a>
Some arcs can specify a time offset/scale via a`Sdf.LayerOffset`.
~~~admonish tip title=""
```mermaid
flowchart LR
    userRoot(["I want to"])
    userRootTimeOffset(["time offset/scale my hierarchy (via a `Sdf.LayerOffset`)"])
    userRootNoTimeOffset(["not time offset/scale my hierarchy"])

    compositionArcSublayer(["Sublayer"])
    compositionArcInherit(["Inherit"])
    compositionArcVariant(["Variant"])
    compositionArcReference(["Reference (External/Internal)"])
    compositionArcPayload(["Payload"])
    compositionArcSpecialize(["Specialize"])
    style compositionArcSublayer fill:#63beff
    style compositionArcInherit fill:#63beff
    style compositionArcVariant fill:#63beff
    style compositionArcReference fill:#63beff
    style compositionArcPayload fill:#63beff
    style compositionArcSpecialize fill:#63beff

    userRoot --> userRootTimeOffset
    userRootTimeOffset --> compositionArcSublayer
    userRootTimeOffset --> compositionArcReference
    userRootTimeOffset --> compositionArcPayload
    userRoot --> userRootNoTimeOffset
    userRootNoTimeOffset --> compositionArcInherit
    userRootNoTimeOffset --> compositionArcVariant
    userRootNoTimeOffset --> compositionArcSpecialize
```
~~~

### Composition Arc By Target Type (File/Hierarchy) <a name="compositionArcCategoryByTargetType"></a>
Here is a comparison between arcs that can target external layers (files) and arcs that target another part of the hierarchy.

~~~admonish tip title=""
```mermaid
flowchart TD
    compositionArcSublayer(["Sublayers (Direct Opinions)"])
    compositionArcValueClip(["Value Clips (Lower than Direct Opinions)"])
    compositionArcInherit(["Inherits"])
    compositionArcVariant(["Variants"])
    compositionArcReferenceFile(["References"])
    compositionArcReferenceInternal(["References"])
    compositionArcPayload(["Payloads"])
    compositionArcSpecialize(["Specialize"])
    compositionArcInternal(["Internal Arcs (Target Hierarchy)"])
    compositionArcExternal(["File Arcs (Target File (+ Hierarchy))"])
    style compositionArcSublayer fill:#63beff
    style compositionArcInherit fill:#63beff
    style compositionArcVariant fill:#63beff
    style compositionArcReferenceFile fill:#63beff
    style compositionArcReferenceInternal fill:#63beff
    style compositionArcPayload fill:#63beff
    style compositionArcSpecialize fill:#63beff    

    compositionArcInternal --> compositionArcInherit
    compositionArcInternal --> compositionArcVariant
    compositionArcInternal --> compositionArcReferenceInternal
    compositionArcInternal --> compositionArcSpecialize
    compositionArcExternal --> compositionArcSublayer
    compositionArcExternal --> compositionArcReferenceFile
    compositionArcExternal --> compositionArcPayload
    compositionArcSublayer --> compositionArcValueClip
```
~~~


## Composition Arcs
ToDo
