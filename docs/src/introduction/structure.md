
# Structure
On this page will talk about how this guide is structured and what the best approach to reading it is.

# Table of Contents
1. [Structure](#structure)
1. [Learning Path](#learningPath)
1. [How To Run Our Code Examples](#code)


## Structure <a name="structure"></a>
Most of our sections follow this simple template:
- **Table of Contents**: Here we show the structure of the individual page, so we can jump to what we are interested in.
- **TL;DR (Too Long; Didn't Read) - In-A-Nutshell**: Here we give a short summary of the page, the most important stuff without all the details.
- **What should I use it for?**: Here we explain what relevance the page has in our day to day work with USD.
- **Resources**: Here we provide external supplementary reading material, often the USD API docs or USD glossary.
- **Overview**: Here we cover the individual topic in broad strokes, so you get the idea of what it is about.

This guide uses Houdini as its "backbone" for exploring concepts, as it is one of the easiest ways to get started with USD.

You can grab free-for-private use copy of Houdini via the [SideFX website](https://www.sidefx.com/). SideFX is the software development company behind the Houdini.

Almost all demos we show are from within Houdini, although you can also save the output of all our code snippets to a .usd file and view it in [USD view](../core/elements/standalone_utilities.md) or [USD manager](http://www.usdmanager.org/) by calling `stage.Export("/file/path.usd")`/`layer.Export("/file/path.usd")`

You can find all of our example files in our [Usd Survival Guide - GitHub Repository](
https://github.com/LucaScheller/VFX-UsdSurvivalGuide/tree/main/files) as well in our supplementary [Usd Asset Resolver - GitHub Repository](https://lucascheller.github.io/VFX-UsdAssetResolver/). Among these files are Houdini .hip scenes, Python snippets and a bit of C++/CMake code.

We also indicate important to know tips with stylized blocks, these come in the form of:

~~~admonish info title="Info | Useful information!"
Information blocks give you "good-to-know" information.
~~~

~~~admonish info title="Pro Tip | Here is an advanced tip!"
We often provide "Pro Tips" that give you pointers how to best approach advanced topics.
~~~

~~~admonish danger title="Danger | Here comes trouble!"
Danger blocks warn you about common pitfalls or short comings of USD and how to best workaround them.
~~~

~~~admonish tip title="Collapsible Block | Click me to show my content!" collapsible=true
For longer code snippets, we often collapse the code block to maintain site readability.
```python
print("Hello world!")
```
~~~

## Learning Path <a name="learningPath"></a>
We recommend working through the guide from start to finish in chronological order. While we can do it in a random order, especially our [Basic Building Blocks of Usd](../core/elements/overview.md) and [Composition](../core/composition/overview.md) build on each other and should therefore be done in order.

To give you are fair warning though, we do deep dive a bit in the beginning, so just make sure you get the gist of it and then come back later when you feel like you need a refresher or deep dive on a specific feature.

## How To Run Our Code Examples <a name="code"></a>
We also have code blocks, where if you hover other them, you can copy the content to you clipboard by pressing the copy icon on the right.
Most of our code examples are "containered", meaning they can run by themselves. 

This does come with a bit of the same boiler plate code per example. The big benefit though is that we can just copy and run them and don't have to initialize our environment.

Most snippets create in memory stages or layers. If we want to use the snippets in a Houdini Python LOP, we have to replace the stage/layer access as follows:

~~~admonish danger title="Danger | Houdini Python LOP Stage/Layer access"
In Houdini we can't call `hou.pwd().editableStage()` and `hou.pwd().editableLayer()` in the same Python LOP node.
Therefore, when running our high vs low level API examples, make sure you are using two different Python LOP nodes.
~~~

~~~admonish tip title=""
```python
from pxr import Sdf, Usd
## Stages
# Native USD
stage = Usd.Stage.CreateInMemory()
# Houdini Python LOP
stage = hou.pwd().editableStage()
## Layers
# Native USD
layer = Usd.Stage.CreateAnonymous()
# Houdini Python LOP
layer = hou.pwd().editableLayer()
```
~~~


