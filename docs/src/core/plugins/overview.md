# Plugin System
from pxr import Tf
root_type = Tf.Type.GetRoot()
for tf_type in root_type.GetAllDerivedTypes():
    print(tf_type.typeName, tf_type.pythonClass)


node = hou.pwd()
stage = node.editableStage()

# Add code to modify the stage.
# Use drop down menu to select examples.
from pxr import Tf
# Create notice callback
def callback(notice, sender):
    print(notice, sender)
# Create a new notice type
class CustomNotice(Tf.Notice):
    '''My custom notice'''
CustomNotice_FQN = "{}.{}".format(CustomNotice.__module__, CustomNotice.__name__)
# Register notice
custom_notice_type = Tf.Type.FindByName(CustomNotice_FQN)
if not custom_notice_type:
    custom_notice_type = Tf.Type.Define(CustomNotice)
# Register notice listeners
# Globally
listener = Tf.Notice.RegisterGlobally(CustomNotice, callback)
# For a specific stage
sender = stage
listener = Tf.Notice.Register(CustomNotice, callback, sender)
# Send notice
CustomNotice().SendGlobally()
CustomNotice().Send(sender)
# Remove listener
listener.Revoke()