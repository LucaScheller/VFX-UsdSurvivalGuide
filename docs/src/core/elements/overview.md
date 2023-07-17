# Elements
In this sub-section we have a look at the basic building blocks of Usd.

Our approach is incrementally going from the smallest building blocks to the larger ones (except for metadata we squeeze that in later as a deep dive), so the recommended order to work through is as follows:

- [Paths](./path.md)
- [Data Containers (Prims & Properties)](./data_container.md)
    - [Prims](./prim.md)
    - [Properties (Attributes/Relationships)](./property.md)
- [Data Types](./data_type.md)
- [Schemas ('Classes' in OOP terminology)](./schemas.md)
- [Metadata](./metadata.md)
- [Layers & Stages (Containers of actual data)](./layer.md)
- [Loading Data (Purpose/Visibility/Activation/Population)](./loading_mechanisms.md)
- [Animation/Time Varying Data](./animation.md)
- [Transforms](./transform.md)
- [Notices/Event Listeners](./notice.md)
- [Standalone Utilities](./standalone_utilities.md)

This will introduce you to the core classes you'll be using the most and then increasing the complexity step by step to see how they work together with the rest of the API.

~~~admonish tip title="Vocabulary/Terminology"
We try to stay terminology agnostic as much as we can, but some vocab you just have to learn to use USd. We compiled a small [cheat sheet](../glossary.md) here, that can assist you with all those weird Usd words.
~~~

Getting down the basic building blocks down is crucial, so take your time! In the current state the examples are a bit "dry", we'll try to make it more entertaining in the future.

Get yourself comfortable and let's get ready to roll! You'll master the principles of Usd in no time!