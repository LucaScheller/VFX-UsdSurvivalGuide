# Layers
```mermaid
flowchart LR
    layerSingleton(Layer Singleton/Registry) --> layer1([Layer])
    layer1([Layer]) --> prim1([Property])
    prim1([Prim]) --> property([Property])
    property --> attribute([Attribute])
    property --> relationship([Relationship])
    layerSingleton --> layer2([Layer])
    layer2([Layer]) --> prim2([...])
```

# Stages
Stages in its simplest form are views on layers.

```mermaid
flowchart LR
    stage(Stage) --> layerRoot(Pseudo Root Layer)
    layerRoot -- Sublayer --> layer1([Layer])
    layer1 -- Payload --> layer1Layer1([Layer])
    layer1 -- Sublayer--> layer1Layer2([Layer])
    layerRoot -- Sublayer --> layer2([Layer])
    layer2 -- Reference --> layer2Layer1([Layer])
    layer2Layer1 -- Payload --> layer2Layer1Layer1([Layer])
    layer2 -- Payload --> layer2Layer2([Layer])
    layerRoot -- Composition Arc --> layer3([...])
    layer3 -- Composition Arc --> layer3Layer1([...])
```