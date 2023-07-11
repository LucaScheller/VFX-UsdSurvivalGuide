# Debugging & Performance Profiling

Usd has 

## Resources
- [API Docs](https://openusd.org/release/toolset.html)

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