#// ANCHOR: component
def componentExampleRootRepo():
    print("here")
#// ANCHOR_END: component



#// ANCHOR: pathString
from pxr import Sdf
path = Sdf.Path("/set/bicycle")
# Do not use this is performance critical loops
# See for more info: https://openusd.org/release/api/_usd__page__best_practices.html
path_str = path.pathString 
#// ANCHOR_END: pathString

