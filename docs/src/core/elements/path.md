# Paths
As Usd is a hierarchy based format, one of its core functions is handling paths.
In order to do this, Usd provides the pxr.Sdf.Path class. You'll be using quite a bunch, so that's why we want to familiarize ourselves with it first.

~~~admonish info title=""
```python
pxr.Sdf.Path("/My/Example/Path")
```
~~~

## TL;DR - API Overview In-A-Nutshell
Here is the TL;DR version:
Paths can encode the following path data:
- Prims ("/set/bicycle")
- Properties:
    - Attributes: "." ("/set/bicycle.size")
    - Relationships: "." ("/set.bikes")
        - Prim to prim: ("/set.bikes[/set/bicycles]") (E.g. Collections of primpaths)
        - Attribute to attribute: ("/set.size[/set/bicycles].size") (E.g. Serializing node graph connections)
- Variants ("/set/bicycle{style=blue}wheel.size")

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:pathSummary}}
```
~~~

## What should I use it for?
~~~admonish tip
Anything that is path related in your hierarchy, use Sdf.Path objects. It will make your life a lot easier than if you were to use strings.
~~~

## Resources
- [API Docs](https://openusd.org/release/api/class_sdf_path.html#sec_SdfPath_Overview)

## Basics
Each element in the path between the "/" symbol is a [prim](https://openusd.org/release/glossary.html#usdglossary-prim) similar to how on disk file paths mark a folder or a file.

Most Usd API calls that expect Sdf.Path objects implicitly take Python strings as well, we'd recommend using Sdf.Paths from the start though, as it is faster and more convenient.

We recommend going through these small examples (5-10 min), just to get used to the Path class.

### Creating a path & string representation

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:pathBasics}}
```
~~~

### Special Paths: emptyPath & absoluteRootPath

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:pathSpecialPaths}}
```
~~~

### Variants
We can also encode variants into the path via the {variantSetName=variantName} syntax.

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:pathVariants}}
```
~~~

### Properties
Paths can also encode properties (more about what these are in the next section).
Notice that attributes and relationships are both encoded with the "." prefix, hence the name "property" is used to describe them both.

~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:pathProperties}}
```
~~~

