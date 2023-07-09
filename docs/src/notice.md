import pxr
def callback(notice, sender):
    print(notice, sender)

# Add
# Global
listener = pxr.Tf.Notice.RegisterGlobally(pxr.Usd.Notice.StageContentsChanged, callback)
listener = pxr.Usd.Notice.StageNotice.RegisterGlobally(pxr.Usd.Notice.StageContentsChanged, callback)
# Per Stage
listener = pxr.Tf.Notice.Register(pxr.Usd.Notice.StageContentsChanged, callback, stage)
listener = pxr.Usd.Notice.StageNotice.Register(pxr.Usd.Notice.StageContentsChanged, callback, stage)
# Remove
listener.Revoke()

# Stage Notice Included
# General
pxr.Usd.Notice.StageContentsChanged
pxr.Usd.Notice.StageEditTargetChanged
# Layer Muting
pxr.Usd.Notice.OnLayerMutingChanged
> .GetMutedLayers()
> .GetMutedLayers()
# Object Changed
pxr.Usd.Notice.ObjectsChanged
> .GetResyncedPaths()        # Composition Changes
> .GetChangedInfoOnlyPaths() #  Attribute/Metadata value changes
>> AffectedObject(UsdObject) (Generic)
>>> ResyncedObject(UsdObject) (Composition Change)
>>> ChangedInfoOnly(UsdObject) (Value Change)  / GetChangedFields(UsdObject/SdfPath) / HasChangedFields(UsdObject/SdfPath) 

# To create a new notice type:
class CustomNotice(Tf.Notice):
    '''TfNotice sent when CustomNotice does something of interest.'''
Tf.Type.Define(CustomNotice)

sender = stage
CustomNotice().SendGlobally()
CustomNotice().Send(sender)

listener = Tf.Notice.RegisterGlobally(CustomNotice, callback)
listener = Tf.Notice.Register(CustomNotice, callback, sender)
listener.Revoke()





```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```

```python,noplayground
print("yes")
```


~~~admonish example title=" Example"
```python
{{#include ../../../code/test.py:component}}
```
~~~

