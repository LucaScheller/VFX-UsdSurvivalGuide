# Section Name
Enter example intro.

~~~admonish question title="Still under construction!"
This sub-section is still under development, it is subject to change and needs extra validation.
~~~

# Table of Contents
1. [<Topic> In-A-Nutshell](#summary)
1. [What should I use it for?](#usage)
1. [Resources](#resources)
1. [Overview](#overview)
1. [Example A](#exampleA)
    1. [Subexample A](#subexampleA)
    1. [Subexample B](#subexampleB)

## TL;DR - <Topic> In-A-Nutshell <a name="summary"></a>
- Main points to know

## What should I use it for? <a name="usage"></a>
~~~admonish tip
Summarize actual production relevance.
~~~

## Resources <a name="resources"></a>
- [API Docs]()

## Overview <a name="overview"></a>
Chart example
```mermaid
flowchart TD
    usdObject(["Usd.Object (Includes Metadata API)"]) --> usdPrim([Usd.Prim])
    usdObject --> usdProperty([Usd.Property])
    usdProperty --> usdAttribute([Usd.Attribute])
    usdProperty --> usdRelationship([Usd.Relationship])
    usdStage(["Usd.Stage (Includes Metadata API)"])
```

Low Level API
```mermaid
flowchart TD
    sdfSpec(["Sdf.Spec (Includes Metadata API)"]) --> sdfPropertySpec([Sdf.Property])
    sdfSpec --> sdfPrimSpec([Sdf.PrimSpec])
    sdfSpec --> sdfVariantSetSpec([Sdf.VariantSetSpec])
    sdfSpec --> sdfVariantSpec([Sdf.VariantSpec])
    sdfPropertySpec --> sdfAttributeSpec([Sdf.AttributeSpec])
    sdfPropertySpec --> sdfRelationshipSpec([Sdf.RelationshipSpec])
    sdfLayer(["Sdf.Layer (Includes Metadata API)"])

```

~~~admonish tip
Example tip
~~~

## Example A <a name="exampleA"></a>
Example A

### Subexample A <a name="subexampleA"></a>
Example A

### Subexample B <a name="subexampleB"></a>
Example A