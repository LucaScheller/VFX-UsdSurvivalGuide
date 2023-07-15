# Glossary
This page is a cheatsheet for Usd vocabulary.

- Value Resolution: What layer has the winning priority out of all your layers where the data can be loaded from.
- layer
- prim
- property -> attribute/relationship
- stage
- authored == explicitly written

- authored: The high level API also has the extra destinction of <ContainerType>.HasAuthored<Name>() vs .Has<Name>(). HasAuthored only returns explicitly defined values, where Has is allowed to return schema fallbacks.