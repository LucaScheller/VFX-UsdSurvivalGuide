# Production Elements

- Scene Retimes/Freeze
    - Currently nternal refernce receive double offest (which makes sense, as they live refer to a layer)

- Layer Singleton Demo
```python
import os
from pxr import Sdf
pig_identifier = os.path.expandvars("$HFS/houdini/usd/assets/pig/geo.usdc")
pig_layer = Sdf.Layer.FindOrOpen(pig_identifier)

rubbertoy_identifier = os.path.expandvars("$HFS/houdini/usd/assets/rubbertoy/geo.usdc")
rubbertoy_layer = Sdf.Layer.FindOrOpen(rubbertoy_identifier)

pig_layer.TransferContent(rubbertoy_layer)
``
- Performance of traversals (metadata vs attribute reads)
- Expose properties to houdini
- common schemas for productions tips and tricks
- 
- Purpose Swapping for preview, bake point color for preview
- 
- large hierarchies vs combined meshes