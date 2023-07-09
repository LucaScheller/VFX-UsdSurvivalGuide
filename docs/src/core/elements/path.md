# Paths

As Usd is a hierarchy based format, one of its core functions is handling paths.
In order to do this, Usd provides the pxr.Sdf.Path class. You'll be using quite a bunch, so that's why we want to familiarize ourselves with it first.

~~~admonish tips title=""
```python
pxr.Sdf.Path("/My/Example/Path")
```
~~~

## Resources
- [API Docs](https://openusd.org/release/api/class_sdf_path.html#sec_SdfPath_Overview)



## Basics

Each element in the path between the "/" symbol is a [prim](https://openusd.org/release/glossary.html#usdglossary-prim) similar to how on disk file paths mark a folder or a file.
~~~admonish tips title="Creating a path & string representation"
```python
{{#include ../../../../code/core/elements.py:pathBasics}}
```
~~~

~~~admonish tips title="Special Paths: emptyPath & absoluteRootPath"
```python
{{#include ../../../../code/core/elements.py:pathSpecialPaths}}
```
~~~

~~~admonish tips title="Encoding properties (attributes/relationships) in the path"
```python
{{#include ../../../../code/core/elements.py:pathProperties}}
```
~~~
