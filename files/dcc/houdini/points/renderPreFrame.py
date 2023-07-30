import os
import sys
from imp import reload
# Python Wrangle Module
dir_path = os.path.dirname(hou.hipFile.path())
if dir_path not in sys.path:
    sys.path.insert(0, dir_path)
import pythonWrangle
reload(pythonWrangle)
from pythonWrangle import run_kernel

frame = hou.frame()
run_kernel(stage, frame)
