"""This file contains all code examples for the 'Core Elements' section.
The following mdBook syntax allows us to sparsely import content:
#// ANCHOR: contentId
def example():
    print("here")
#// ANCHOR_END: contentId
"""

"""api.md"""

#// ANCHOR: apiHighVsLowLevel
### High Level ### (Notice how we still use elements of the low level API)
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
attr = prim.CreateAttribute("tire:size", Sdf.ValueTypeNames.Float)
attr.Set(10)

### Low Level ###
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.specifier = Sdf.SpecifierDef
prim_spec.typeName = "Xform"
attr_spec = Sdf.AttributeSpec(prim_spec, "tire:size", Sdf.ValueTypeNames.Float)
attr_spec.default = 10
#// ANCHOR_END: apiHighVsLowLevel

"""path.md"""

#// ANCHOR: pathSummary
from pxr import Sdf
# Prims
prim_path = Sdf.Path("/set/bicycle")
prim_path_str = Sdf.Path("/set/bicycle").pathString # Returns the Python str "/set/bicycle"
# Properties (Attribute/Relationship)
property_path = Sdf.Path("/set/bicycle.size")
property_with_namespace_path = Sdf.Path("/set/bicycle.tire:size")
# Attribute targets (connections)
attribute_rel_target_path = Sdf.Path("/set.bikes[/set/bicycles].size") # Attribute to attribute linking (E.g. serializing node graph connections to Usd)
# Relationship targets
prim_rel_target_path = Sdf.Path("/set.bikes[/set/bicycles]")           # Prim to prim linking (E.g. path collections)
# Variants
variant_path = prim_path.AppendVariantSelection("style", "blue") # Returns: Sdf.Path('/set/bicycle{style=blue}')
variant_path = Sdf.Path('/set/bicycle{style=blue}frame/screws')
#// ANCHOR_END: pathSummary

#// ANCHOR: pathBasics
from pxr import Sdf
path = Sdf.Path("/set/bicycle")
path_name = path.name     # Similar to os.path.basename(), returns the last element of the path
path_empty = path.isEmpty # Property to check if path is empty
# Path validation (E.g. for user created paths)
Sdf.Path.IsValidPathString("/some/_wrong!_/path") # Returns: (False, 'Error Message')
# Join paths (Similar to os.path.join())
path = Sdf.Path("/set/bicycle")
path.AppendPath(Sdf.Path("frame/screws")) # Returns: Sdf.Path("/set/bicycle/frame/screws")
# Manually join individual path elements
path = Sdf.Path(Sdf.childDelimiter.join(["set", "bicycle"])) 
# Get the parent path
parent_path = path.GetParentPath() # Returns Sdf.Path("/set")
parent_path.IsRootPrimPath()       # Returns: True (Root prims are prims that only
                                   #                have a single '/')        
ancestor_range = path.GetAncestorsRange() # Returns an iterator for the parent paths, the same as recursively calling GetParentPath()
# Add child path
child_path = path.AppendChild("wheel") # Returns: Sdf.Path("/set/bicycle/wheel")
# Check if path is a prim path (and not a attribute/relationship path)
path.IsPrimPath() # Returns: True
# Check if path starts with another path
# Important: It actually compares individual path elements (So it is not a str.startswith())
Sdf.Path("/set/cityA/bicycle").HasPrefix(Sdf.Path("/set"))      # Returns: True
Sdf.Path("/set/cityA/bicycle").HasPrefix(Sdf.Path("/set/city")) # Returns: False
Sdf.Path("/set/bicycle").GetCommonPrefix(Sdf.Path("/set"))      # Returns: Sdf.Path("/set")
# Relative/Absolute paths
path = Sdf.Path("/set/cityA/bicycle")
rel_path = path.MakeRelativePath("/set")     # Returns: Sdf.Path('cityA/bicycle')
abs_path = rel_path.MakeAbsolutePath("/set") # Returns: Sdf.Path('/set/cityA/bicycle')
abs_path.IsAbsolutePath()                    # Returns: True -> Checks path[0] == "/"
# Do not use this is performance critical loops
# See for more info: https://openusd.org/release/api/_usd__page__best_practices.html
# This gives you a standard python string
path_str = path.pathString
#// ANCHOR_END: pathBasics

#// ANCHOR: pathSpecialPaths
from pxr import Sdf
# Shortcut for Sdf.Path("/")
root_path = Sdf.Path.absoluteRootPath
root_path == Sdf.Path("/") # Returns: True
# We'll cover in a later section how to rename/remove things in Usd,
# so don't worry about the details how this works yet. Just remember that
# an emptyPath exists and that its usage is to remove something.
src_path = Sdf.Path("/set/bicycle")
dst_path = Sdf.Path.emptyPath
edit = Sdf.BatchNamespaceEdit()
edit.Add(src_path, dst_path)
#// ANCHOR_END: pathSpecialPaths

#// ANCHOR: pathProperties
# Properties (see the next section) are also encoded
# in the path via the "." (Sdf.Path.propertyDelimiter) token
from pxr import Sdf
path = Sdf.Path("/set/bicycle.size")
property_name = path.name # Be aware, this will return 'size' (last element)
# Append property to prim path
Sdf.Path("/set/bicycle").AppendProperty("size") # Returns: Sdf.Path("/set/bicycle.size")
# Properties can also be namespaced with ":" (Sdf.Path.namespaceDelimiter)
path = Sdf.Path("/set/bicycle.tire:size").name 
property_name = path.name                 # Returns: 'tire:size'
property_name = path.ReplaceName("color") # Returns: Sdf.Path("/set/bicycle.color")
# Check if path is a property path (and not a prim path)
path.IsPropertyPath() # Returns: True
# Check if path is a property path (and not a prim path)
Sdf.Path("/set/bicycle.tire:size").IsPrimPropertyPath()  # Returns: True
Sdf.Path("/set/bicycle").IsPrimPropertyPath()            # Returns: False
# Convenience methods
path = Sdf.Path("/set/bicycle").AppendProperty(Sdf.Path.JoinIdentifier(["tire", "size"]))
namespaced_elements = Sdf.Path.TokenizeIdentifier("tire:size")   # Returns: ["tire", "size"]
last_element = Sdf.path.StripNamespace("/set/bicycle.tire:size") # Returns: 'size'
# With GetPrimPath we can strip away all property encodings
path = Sdf.Path("/set/bicycle.tire:size")
prim_path = path.GetPrimPath(path) # Returns: Sdf.Path('/set/bicycle')

# We can't actually differentiate between a attribute and relationship based on the property path.
# Hence the "Property" terminology.
# In practice we rarely use/see this as this is a pretty low level API use case.
# The only 'common' case, where you will see this is when calling the Sdf.Layer.Traverse function.
# To encode prim relation targets, we can use:
prim_rel_target_path = Sdf.Path("/set.bikes[/set/bicycle]")
prim_rel_target_path.IsTargetPath() # Returns: True
prim_rel_target_path = Sdf.Path("/set.bikes").AppendTarget("/set/bicycle")
# We can also encode attribute connection targets (For example shader node graph connections):
attribute_rel_target_path = Sdf.Path("/set.bikes[/set/bicycles].size")
attribute_rel_target_path.IsRelationalAttributePath()  # Returns: True
#// ANCHOR_END: pathProperties

#// ANCHOR: pathVariants
# Variants (see the next sections) are also encoded
# in the path via the "{variantSetName=variantName}" syntax.
from pxr import Sdf
path = Sdf.Path("/set/bicycle")
variant_path = path.AppendVariantSelection("style", "blue") # Returns: Sdf.Path('/set/bicycle{style=blue}')
variant_path = Sdf.Path('/set/bicycle{style=blue}frame/screws')
# Property path to prim path with variants
property_path = Sdf.Path('/set/bicycle{style=blue}frame/screws.size')
variant_path = property_path.GetPrimOrPrimVariantSelectionPath() # Returns: Sdf.Path('/set/bicycle{style=blue}frame/screws')
# Typical iteration example:
variant_path = Sdf.Path('/set/bicycle{style=blue}frame/screws')
if variant_path.ContainsPrimVariantSelection():          # Returns: True # For any variant selection in the whole path
    for parent_path in variant_path.GetAncestorRange():
        if parent_path.IsPrimVariantSelectionPath():
            print(parent_path.GetVariantSelection())     # Returns: ('style', 'blue')

# When authoring relationships, we usually want to remove all variant encodings in the path:
variant_path = Sdf.Path('/set/bicycle{style=blue}frame/screws')
prim_rel_target_path = variant_path.StripAllVariantSelections() # Returns: Sdf.Path('/set/bicycle/frame/screws')
#// ANCHOR_END: pathVariants

## Data Containers ##

#// ANCHOR: dataContainerPrimOverview
### High Level ###
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
attr = prim.CreateAttribute("tire:size", Sdf.ValueTypeNames.Float)
attr.Set(10)

### Low Level ###
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.specifier = Sdf.SpecifierDef
prim_spec.typeName = "Xform"
attr_spec = Sdf.AttributeSpec(prim_spec, "tire:size", Sdf.ValueTypeNames.Float)
attr_spec.default = 10
#// ANCHOR_END: dataContainerPrimOverview


#// ANCHOR: dataContainerPrimCoreHighLevel
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/cube")
prim = stage.DefinePrim(prim_path, "Xform") # Here defining the prim uses a `Sdf.SpecifierDef` define op by default.
# The specifier and type name is something you'll usually always set.
prim.SetSpecifier(Sdf.SpecifierOver)
prim.SetTypeName("Cube")
# The other core specs are set via schema APIs, for example:
model_API = Usd.ModelAPI(prim)
if not model_API.GetKind():
    model_API.SetKind(Kind.Tokens.group)
#// ANCHOR_END: dataContainerPrimCoreHighLevel


#// ANCHOR: dataContainerPrimCoreLowLevel
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/cube")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path) # Here defining the prim uses a `Sdf.SpecifierOver` define op by default.
# The specifier and type name is something you'll usually always set.
prim_spec.specifier = Sdf.SpecifierDef # Or Sdf.SpecifierOver/Sdf.SpecifierClass
prim_spec.typeName = "Cube"
prim_spec.active = True # There is also a prim_spec.ClearActive() shortcut for removing active metadata
prim_spec.kind = "group"    # There is also a prim_spec.ClearKind() shortcut for removing kind metadata
prim_spec.instanceable = False # There is also a prim_spec.ClearInstanceable() shortcut for removing instanceable metadata.
prim_spec.hidden = False # A hint for UI apps to hide the spec for viewers

# You can also set them via the standard metadata commands:
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/cube")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
# The specifier and type name is something you'll usually always set.
prim_spec.SetInfo(prim_spec.SpecifierKey, Sdf.SpecifierDef) # Or Sdf.SpecifierOver/Sdf.SpecifierClass
prim_spec.SetInfo(prim_spec.TypeNameKey, "Cube")
# These are some other common specs:
prim_spec.SetInfo(prim_spec.ActiveKey, True)
prim_spec.SetInfo(prim_spec.KindKey, "group")
prim_spec.SetInfo("instanceable", False) 
prim_spec.SetInfo(prim_spec.HiddenKey, False)
#// ANCHOR_END: dataContainerPrimCoreLowLevel


#// ANCHOR: dataContainerPrimBasicsSpecifierTraversal
### High Level ###
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
# Replicate the Usd file example above:
stage.DefinePrim("/definedCube", "Cube").SetSpecifier(Sdf.SpecifierDef)
stage.DefinePrim("/overCube", "Cube").SetSpecifier(Sdf.SpecifierOver)
stage.DefinePrim("/classCube", "Cube").SetSpecifier(Sdf.SpecifierClass)
## Traverse with default filter (USD calls filter 'predicate')
# UsdPrimIsActive & UsdPrimIsDefined & UsdPrimIsLoaded & ~UsdPrimIsAbstract
for prim in stage.Traverse():
    print(prim)
# Returns:
# Usd.Prim(</definedCube>)
## Traverse with 'all' filter (USD calls filter 'predicate')
for prim in stage.TraverseAll():
    print(prim)
# Returns:
# Usd.Prim(</definedCube>)
# Usd.Prim(</overCube>)
# Usd.Prim(</classCube>)
## Traverse with IsAbstract (== IsClass) filter (USD calls filter 'predicate')
predicate = Usd.PrimIsAbstract
for prim in stage.Traverse(predicate):
    print(prim)
# Returns:
# Usd.Prim(</classCube>)
## Traverse with ~PrimIsDefined filter (==IsNotDefined) (USD calls filter 'predicate')
predicate = ~Usd.PrimIsDefined
for prim in stage.Traverse(predicate):
    print(prim)
# Returns:
# Usd.Prim(</overCube>)
#// ANCHOR_END: dataContainerPrimBasicsSpecifierTraversal


#// ANCHOR: dataContainerPrimBasicsSpecifierDef
### High Level ###
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
# The .DefinePrim method uses a Sdf.SpecifierDef specifier by default
prim = stage.DefinePrim(prim_path, "Xform")
prim.SetSpecifier(Sdf.SpecifierDef)

### Low Level ###
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
# The .CreatePrimInLayer method uses a Sdf.SpecifierOver specifier by default
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.specifier = Sdf.SpecifierDef
#// ANCHOR_END: dataContainerPrimBasicsSpecifierDef

#// ANCHOR: dataContainerPrimBasicsSpecifierOver
### High Level ###
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
# The .DefinePrim method uses a Sdf.SpecifierDef specifier by default
prim = stage.DefinePrim(prim_path, "Xform")
prim.SetSpecifier(Sdf.SpecifierOver)
# The prim class' IsDefined method checks if a prim (and all its parents) have the "def" specifier.
print(prim.GetSpecifier() == Sdf.SpecifierSdf, prim.IsDefined())

### Low Level ###
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
# The .CreatePrimInLayer method uses a Sdf.SpecifierOver specifier by default
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.specifier = Sdf.SpecifierOver
#// ANCHOR_END: dataContainerPrimBasicsSpecifierOver

#// ANCHOR: dataContainerPrimBasicsSpecifierClass
### High Level ###
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
# The .DefinePrim method uses a Sdf.SpecifierDef specifier by default
prim = stage.DefinePrim(prim_path, "Xform")
prim.SetSpecifier(Sdf.SpecifierOver)
# The prim class' IsAbstract method checks if a prim (and all its parents) have the "Class" specifier.
print(prim.GetSpecifier() == Sdf.SpecifierClass, prim.IsAbstract())

### Low Level ###
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
# The .CreatePrimInLayer method uses a Sdf.SpecifierOver specifier by default
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.specifier = Sdf.SpecifierClass
#// ANCHOR_END: dataContainerPrimBasicsSpecifierClass

#// ANCHOR: dataContainerPrimBasicsTypeName
### High Level ###
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
prim.SetTypeName("Xform")

### Low Level ###
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.typeName = "Xform"

# Default type without any fancy bells and whistles:
prim.SetTypeName("Scope")
prim_spec.typeName = "Scope"
#// ANCHOR_END: dataContainerPrimBasicsTypeName


#// ANCHOR: dataContainerPrimBasicsKinds
### High Level ###
from pxr import Kind, Sdf, Usd
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
model_API = Usd.ModelAPI(prim)
model_API.SetKind(Kind.Tokens.component)
# The prim class' IsModel/IsGroup method checks if a prim (and all its parents) are (sub-) kinds of model/group.
model_API.SetKind(Kind.Tokens.model)
kind = model_API.GetKind()
print(kind, (Kind.Registry.GetBaseKind(kind) or kind) == Kind.Tokens.model, prim.IsModel())
model_API.SetKind(Kind.Tokens.group)
kind = model_API.GetKind()
print(kind, (Kind.Registry.GetBaseKind(kind) or kind) == Kind.Tokens.group, prim.IsGroup())

### Low Level ###
from pxr import Kind, Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.SetInfo("kind", Kind.Tokens.component)
#// ANCHOR_END: dataContainerPrimBasicsKinds

#// ANCHOR: dataContainerPrimBasicsTokens
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/cube")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.SetInfo(prim_spec.KindKey, "group")
#// ANCHOR_END: dataContainerPrimBasicsTokens


#// ANCHOR: dataContainerPrimBasicsDebugging
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/cube")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.specifier = Sdf.SpecifierDef
prim_spec.SetInfo(prim_spec.KindKey, "group")
attr_spec = Sdf.AttributeSpec(prim_spec, "size", Sdf.ValueTypeNames.Float)
# Running this
print(prim_spec.GetAsText())
# Returns:
"""
def "cube" (
    kind = "group"
)
{
    float size
}
"""
#// ANCHOR_END: dataContainerPrimBasicsDebugging


#// ANCHOR: dataContainerPrimHierarchy
### High Level ###
# Has: 'IsPseudoRoot' 
# Get: 'GetParent', 'GetPath', 'GetName', 'GetStage',
#      'GetChild', 'GetChildren', 'GetAllChildren',   
#      'GetChildrenNames', 'GetAllChildrenNames',
#      'GetFilteredChildren', 'GetFilteredChildrenNames', 
# The GetAll<MethodNames> return children that have specifiers other than Sdf.SpecifierDef
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/set/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
parent_prim = prim.GetParent()
print(prim.GetPath()) # Returns: Sdf.Path("/set/bicycle")
print(prim.GetParent()) # Returns: Usd.Prim("/set")
print(parent_prim.GetChildren()) # Returns: [Usd.Prim(</set/bicycle>)]
print(parent_prim.GetChildrenNames()) # Returns: ['bicycle']

### Low Level ###
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/set/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
print(prim_spec.path) # Returns: Sdf.Path("/set/bicycle")
print(prim_spec.name) # Returns: "bicycle"
# To rename a prim, you can simply set the name attribute to something else.
# If you want to batch-rename, you should use the Sdf.BatchNamespaceEdit class, see our explanation [here]()
prim_spec.name = "coolBicycle"
print(prim_spec.nameParent) # Returns: Sdf.PrimSpec("/set")
print(prim_spec.nameParent.nameChildren) # Returns: {'coolCube': Sdf.Find('anon:0x7f6e5a0e3c00:LOP:/stage/pythonscript3', '/set/coolBicycle')}
print(prim_spec.layer) # Returns: The active layer object the spec is on.
#// ANCHOR_END: dataContainerPrimHierarchy


#// ANCHOR: dataContainerPrimSchemas
### High Level ###
# Has: 'IsA', 'HasAPI', 'CanApplyAPI'
# Get: 'GetTypeName', 'GetAppliedSchemas'
# Set: 'SetTypeName', 'AddAppliedSchema', 'ApplyAPI'
# Clear: 'ClearTypeName', 'RemoveAppliedSchema', 'RemoveAPI'
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
# Typed Schemas
prim.SetTypeName("Xform")
# Applied schemas
prim.AddAppliedSchema("SkelBindingAPI")
# AddAppliedSchema does not check if the schema actually exists, 
# you have to use this for codeless schemas.
# prim.RemoveAppliedSchema("SkelBindingAPI")
# Single-Apply API Schemas
prim.ApplyAPI("UsdGeomModelAPI")

### Low Level ###
# To set applied API schemas via the low level API, we just 
# need to set the `apiSchemas` key to a Token Listeditable Op.
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
# Typed Schemas
prim_spec.typeName = "Xform"
# Applied Schemas
schemas = Sdf.TokenListOp.Create(
    prependedItems=["SkelBindingAPI", "UsdGeomModelAPI"]
)
prim_spec.SetInfo("apiSchemas", schemas)
#// ANCHOR_END: dataContainerPrimSchemas

#// ANCHOR: dataContainerPrimTypeDefinition
from pxr import Sdf, Tf, Usd, UsdGeom
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
prim.ApplyAPI("UsdGeomModelAPI")
prim_def = prim.GetPrimDefinition()
print(prim_def.GetAppliedAPISchemas()) # Returns: ['GeomModelAPI']
print(prim_def.GetPropertyNames()) 
# Returns: All properties that come from the type name schema and applied schemas
"""
['model:drawModeColor', 'model:cardTextureZPos', 'model:drawMode', 'model:cardTextureZNeg', 
'model:cardTextureYPos', 'model:cardTextureYNeg', 'model:cardTextureXPos', 'model:cardTextur
eXNeg', 'model:cardGeometry', 'model:applyDrawMode', 'proxyPrim', 'visibility', 'xformOpOrde
r', 'purpose']
"""
# You can also bake down the prim definition, this won't flatten custom properties though.
dst_prim = stage.DefinePrim("/flattenedExample")
dst_prim = prim_def.FlattenTo("/flattenedExample")
# This will also flatten all metadata (docs etc.), this should only be used, if you need to export
# a custom schema to an external vendor. (Not sure if this the "official" way to do it, I'm sure
# there are better ones.)
#// ANCHOR_END: dataContainerPrimTypeDefinition

#// ANCHOR: dataContainerPrimTypeInfo
from pxr import Sdf, Tf, Usd, UsdGeom
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
prim.ApplyAPI("UsdGeomModelAPI")
print(prim.IsA(UsdGeom.Xform)) # Returns: True
print(prim.IsA(Tf.Type.FindByName('UsdGeomXform'))) # Returns: True
prim_type_info = prim.GetPrimTypeInfo()
print(prim_type_info.GetAppliedAPISchemas()) # Returns: ['GeomModelAPI']
print(prim_type_info.GetSchemaType()) # Returns: Tf.Type.FindByName('UsdGeomXform')
print(prim_type_info.GetSchemaTypeName()) # Returns: Xform
#// ANCHOR_END: dataContainerPrimTypeInfo

#// ANCHOR: dataContainerPrimLoading
### High Level ###
from pxr import Sdf, Tf, Usd, UsdGeom
# Has: 'HasAuthoredActive', 'HasAuthoredHidden'
# Get: 'IsActive', 'IsLoaded', 'IsHidden'
# Set: 'SetActive', 'SetHidden' 
# Clear: 'ClearActive', 'ClearHidden'
# Loading: 'Load', 'Unload'
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
## Activation: Controls subhierarchy loading of prim.
prim.SetActive(False) # 
# prim.ClearActive()
## Visibility: Controls the visiblity for render delegates (subhierarchy will still be loaded)
imageable_API = UsdGeom.Imageable(prim)
visibility_attr = imageable_API.CreateVisibilityAttr()
visibility_attr.Set(UsdGeom.Tokens.invisible)
## Purpose: Controls if the prim is visible for what the renderer requested.
imageable_API = UsdGeom.Imageable(prim)
purpose_attr = imageable_API.CreatePurposeAttr()
purpose_attr.Set(UsdGeom.Tokens.render)
## Payload loading: Control payload loading (High Level only as it redirects the request to the stage).
# In our example stage here, we have no payloads, so we don't see a difference.
prim.Load()
prim.UnLoad()
# Calling this on the prim is the same thing.
prim = stage.GetPrimAtPath(prim_path)
prim.GetStage().Load(prim_path)
prim.GetStage().Unload(prim_path)
## Hidden: # Hint to hide for UIs
prim.SetHidden(False)
# prim.ClearHidden()

### Low Level ###
from pxr import Sdf, UsdGeom
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/set/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
## Activation: Controls subhierarchy loading of prim.
prim_spec.active = False
# prim_spec.ClearActive()
## Visibility: Controls the visiblity for render delegates (subhierarchy will still be loaded)
visibility_attr_spec = Sdf.AttributeSpec(prim_spec, UsdGeom.Tokens.purpose, Sdf.ValueTypeNames.Token)
visibility_attr_spec.default = UsdGeom.Tokens.invisible
## Purpose: Controls if the prim is visible for what the renderer requested.
purpose_attr_spec = Sdf.AttributeSpec(prim_spec, UsdGeom.Tokens.purpose, Sdf.ValueTypeNames.Token)
purpose_attr_spec.default = UsdGeom.Tokens.render
## Hidden: # Hint to hide for UIs
prim_spec.hidden = True 
# prim_spec.ClearHidden()
#// ANCHOR_END: dataContainerPrimLoading


#// ANCHOR: dataContainerPrimPropertiesHighLevel
from pxr import Usd, Sdf
# Has: 'HasProperty', 'HasAttribute', 'HasRelationship'
# Get: 'GetProperties', 'GetAuthoredProperties', 'GetPropertyNames', 'GetPropertiesInNamespace', 'GetAuthoredPropertiesInNamespace'
#      'GetAttribute', 'GetAttributes', 'GetAuthoredAttributes'
#      'GetRelationship', 'GetRelationships', 'GetAuthoredRelationships'
#      'FindAllAttributeConnectionPaths', 'FindAllRelationshipTargetPaths'
# Set: 'CreateAttribute', 'CreateRelationship'
# Clear: 'RemoveProperty', 
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Cube")
# As the cube schema ships with a "size" attribute, we don't have to create it first
# Usd is smart enough to check the schema for the type and creates it for us.
size_attr = prim.GetAttribute("size")
size_attr.Set(10)
## Looking up attributes
print(prim.GetAttributes())
# Returns: All the attributes that are provided by the schema
"""
[Usd.Prim(</bicycle>).GetAttribute('doubleSided'), Usd.Prim(</bicycle>).GetAttribute('extent'), Usd.
Prim(</bicycle>).GetAttribute('orientation'), Usd.Prim(</bicycle>).GetAttribute('primvars:displayCol
or'), Usd.Prim(</bicycle>).GetAttribute('primvars:displayOpacity'), Usd.Prim(</bicycle>).GetAttribut
e('purpose'), Usd.Prim(</bicycle>).GetAttribute('size'), Usd.Prim(</bicycle>).GetAttribute('visibili
ty'), Usd.Prim(</bicycle>).GetAttribute('xformOpOrder')]
"""
print(prim.GetAuthoredAttributes())
# Returns: Only the attributes we have written to in the active stage.
# [Usd.Prim(</bicycle>).GetAttribute('size')]
## Looking up relationships:
print(prim.GetRelationships())
# Returns:
# [Usd.Prim(</bicycle>).GetRelationship('proxyPrim')]
box_prim = stage.DefinePrim("/box")
prim.GetRelationship("proxyPrim").SetTargets([box_prim.GetPath()])
# If we now check our properties, you can see both the size attribute
# and proxyPrim relationship show up.
print(prim.GetAuthoredProperties())
# Returns:
# [Usd.Prim(</bicycle>).GetRelationship('proxyPrim'),
#  Usd.Prim(</bicycle>).GetAttribute('size')]
## Creating attributes:
# If we want to create non-schema attributes (or even schema attributes without using
# the schema getter/setters), we can run:
tire_size_attr = prim.CreateAttribute("tire:size", Sdf.ValueTypeNames.Float)
tire_size_attr.Set(5)
#// ANCHOR_END: dataContainerPrimPropertiesHighLevel

#// ANCHOR: dataContainerPrimPropertiesLowLevel
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/cube")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.specifier = Sdf.SpecifierDef
attr_spec = Sdf.AttributeSpec(prim_spec, "size", Sdf.ValueTypeNames.Float)
print(prim_spec.attributes) # Returns: {'size': Sdf.Find('anon:0x7f6efe199480:LOP:/stage/python', '/cube.size')}
attr_spec.default = 10
# To remove a property you can run:
# prim_spec.RemoveProperty(attr_spec)
# Let's re-create what we did in the high level API example.
box_prim_path = Sdf.Path("/box")
box_prim_spec = Sdf.CreatePrimInLayer(layer, box_prim_path)
box_prim_spec.specifier = Sdf.SpecifierDef
rel_spec = Sdf.RelationshipSpec(prim_spec, "proxyPrim")
rel_spec.targetPathList.explicitItems = [prim_path]
# Get all authored properties (in the active layer only)
print(prim_spec.properties)
# Returns:
"""
{'size': Sdf.Find('anon:0x7ff87c9c2000', '/cube.size'),
 'proxyPrim': Sdf.Find('anon:0x7ff87c9c2000', '/cube.proxyPrim')}
"""
#// ANCHOR_END: dataContainerPrimPropertiesLowLevel

#// ANCHOR: metadataSummary
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
prim.SetMetadata("assetInfo", {"version": 1})
prim.SetAssetInfoByKey("identifier", Sdf.AssetPath("bicycler.usd"))
prim.SetMetadata("customData", {"sizeUnit": "meter"})
prim.SetCustomDataByKey("nested:shape", "round")
#// ANCHOR_END: metadataSummary


#// ANCHOR: metadataBasics
"""
### General
# Has:   'HasAuthoredMetadata'/'HasAuthoredMetadataDictKey'/'HasMetadata'/'HasMetadataDictKey'
# Get:   'GetAllAuthoredMetadata'/'GetAllMetadata'/'GetMetadata'/'GetMetadataByDictKey'
# Set:   'SetMetadata'/'SetMetadataByDictKey', 
# Clear: 'ClearMetadata'/'ClearMetadataByDictKey'
### Asset Info (Prims only)
# Has: 'HasAssetInfo'/'HasAssetInfoKey'/'HasAuthoredAssetInfo'/'HasAuthoredAssetInfoKey'
# Get: 'GetAssetInfo'/'GetAssetInfoByKey'
# Set: 'SetAssetInfo'/'SetAssetInfoByKey', 
# Clear: 'ClearAssetInfo'/'ClearAssetInfoByKey'
### Custom Data (Prims, Properties(Attributes/Relationships), Layers)
# Has: 'HasCustomData'/'HasCustomDataKey'/'HasAuthoredCustomData'/'HasAuthoredCustomDataKey'
# Get: 'GetCustomData'/'GetCustomDataByKey'
# Set: 'SetCustomData'/'SetCustomDataByKey', 
# Clear: 'ClearCustomData'/'ClearCustomDataByKey'
"""
from pxr import Usd, Sdf

stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
prim.SetAssetInfoByKey("identifier", Sdf.AssetPath("bicycler.usd"))
prim.SetAssetInfoByKey("nested", {"assetPath": Sdf.AssetPath("bicycler.usd"), "version": 1})
prim.SetMetadataByDictKey("assetInfo", "nested:color", "blue")
attr = prim.CreateAttribute("tire:size", Sdf.ValueTypeNames.Float)
attr.SetMetadata("customData", {"sizeUnit": "meter"})
attr.SetCustomDataByKey("nested:shape", "round")

print(prim.HasAuthoredMetadata("assetInfo")) # Returns: True
print(prim.HasAuthoredMetadataDictKey("assetInfo", "identifier")) # Returns: True
print(prim.HasMetadata("assetInfo")) # Returns: True
print(prim.HasMetadataDictKey("assetInfo", "nested:color")) # Returns: True
# prim.ClearMetadata("assetInfo") # Remove all assetInfo in the current layer.
#// ANCHOR_END: metadataBasics


#// ANCHOR: metadataValidateDict
data = {"myCustomKey": 1}
success_state, metadata, error_message = Sdf.ConvertToValidMetadataDictionary(data)
#// ANCHOR_END: metadataValidateDict


#// ANCHOR: metadataNestedKeyPath
from pxr import Usd, Sdf
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
prim.SetAssetInfoByKey("nested:color", "blue")
print(prim.GetAssetInfo()) # Returns: {'nested': {'color': 'blue'}}
print(prim.GetAssetInfoByKey("nested:color")) # Returns: "blue"
#// ANCHOR_END: metadataNestedKeyPath


#// ANCHOR: metadataAuthored
from pxr import Usd, Sdf
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
prim.SetAssetInfoByKey("identifier", "bicycle.usd")
# The difference between "authored" and non "authored" methods is
# that "authored" methods don't return fallback values that come from schemas.
print(prim.GetAllAuthoredMetadata()) 
# Returns:
# {'assetInfo': {'identifier': 'bicycle.usd'}, 
#  'specifier': Sdf.SpecifierDef, 
#  'typeName': 'Xform'}
print(prim.GetAllMetadata()) 
# Returns:
#{'assetInfo': {'identifier': 'bicycle.usd'}, 
# 'documentation': 'Concrete prim schema for a transform, which implements Xformable ',
# 'specifier': Sdf.SpecifierDef,
# 'typeName': 'Xform'}
#// ANCHOR_END: metadataAuthored


#// ANCHOR: metadataStage
from pxr import Usd, Sdf
stage = Usd.Stage.CreateInMemory()
stage.SetMetadata("customLayerData", {"myCustomStageData": 1})
# Is the same as:
layer = stage.GetRootLayer()
metadata = layer.customLayerData
metadata["myCustomRootData"] = 1
layer.metadata = metadata
# Or:
layer = stage.GetSessionLayer()
metadata = layer.customLayerData
metadata["myCustomSessionData"] = 1
layer.metadata = metadata
# To get the composed value from the session and root layer:
# This actually only returns the value of the root layer, I'm guessing this is a bug?
stage.GetMetadata("customLayerData")
#// ANCHOR_END: metadataStage


#// ANCHOR: metadataLayer
from pxr import Usd, Sdf
layer = Sdf.Layer.CreateAnonymous()
layer.customLayerData = {"myCustomPipelineKey": "myCoolValue"}
#// ANCHOR_END: metadataLayer


#// ANCHOR: metadataPrimPropertySpec
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
### Prims ###
prim_spec = Sdf.CreatePrimInLayer(layer, "/bicycle")
prim_spec.specifier = Sdf.SpecifierDef
# Asset Info and Custom Data
prim_spec.assetInfo = {"identifier": Sdf.AssetPath("bicycle.usd")}
prim_spec.customData = {"myCoolData": "myCoolValue"}
# General metadata
# Has: 'HasInfo'
# Get: 'ListInfoKeys', 'GetMetaDataInfoKeys', 'GetInfo', 'GetFallbackForInfo', 'GetMetaDataDisplayGroup'
# Set: 'SetInfo', 'SetInfoDictionaryValue'
# Clear: 'ClearInfo'
print(prim_spec.ListInfoKeys()) # Returns: ['assetInfo', 'customData', 'specifier']
# To get all registered schema keys run:
print(prim_spec.GetMetaDataInfoKeys())
"""Returns: ['payloadAssetDependencies', 'payload', 'kind', 'suffix', 'inactiveIds', 'clipSets',
'HDAKeepEngineOpen', 'permission', 'displayGroupOrder', 'assetInfo', 'HDAParms', 'instanceable', 
'symmetryFunction', 'HDATimeCacheMode', 'clips', 'HDAAssetName', 'active', 'HDATimeCacheEnd', 
'customData', 'HDAOptions', 'prefix', 'apiSchemas', 'suffixSubstitutions', 'symmetryArguments',
'hidden', 'HDATimeCacheStart', 'sdrMetadata', 'typeName', 'HDATimeCacheInterval', 'documentation',
'prefixSubstitutions', 'symmetricPeer']"""
# For the fallback values and UI grouping hint you can use
# 'GetFallbackForInfo' and 'GetMetaDataDisplayGroup'.
# Prim spec core data is actually also just metadata info
prim_spec.SetInfo("specifier", Sdf.SpecifierDef)
prim_spec.SetInfo("typeName", "Xform")
# Is the same as:
prim_spec.specifier = Sdf.SpecifierDef
prim_spec.typeName = "Xform"

### Properties ###
attr_spec = Sdf.AttributeSpec(prim_spec, "tire:size", Sdf.ValueTypeNames.Float)
# Custom Data
attr_spec.customData = {"myCoolData": "myCoolValue"}
# We can actually use the attr_spec.customData assignment here too,
# doesn't make that much sense though
# General metadata
# Has: 'HasInfo'
# Get: 'ListInfoKeys', 'GetMetaDataInfoKeys', 'GetInfo', 'GetFallbackForInfo', 'GetMetaDataDisplayGroup'
# Set: 'SetInfo', 'SetInfoDictionaryValue'
# Clear: 'ClearInfo'
# The API here is the same as for the prim_spec, as it all inherits from Sdf.Spec
# To get all registered schema keys run:
print(attr_spec.GetMetaDataInfoKeys())
"""Returns: ['unauthoredValuesIndex', 'interpolation', 'displayGroup', 'faceIndexPrimvar', 
'suffix', 'constraintTargetIdentifier', 'permission', 'assetInfo', 'symmetryFunction', 'uvPrimvar',
'elementSize', 'allowedTokens', 'customData', 'prefix', 'renderType', 'symmetryArguments', 
'hidden', 'displayName', 'sdrMetadata', 'faceOffsetPrimvar', 'weight', 'documentation', 
'colorSpace', 'symmetricPeer', 'connectability']
"""
#// ANCHOR_END: metadataPrimPropertySpec

#// ANCHOR: metadataDocs
from pxr import Usd, Sdf
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Cube")
# Shortcut to get the docs metadata
# Has: 'HasAuthoredDocumentation'
# Get: 'GetDocumentation'
# Set: 'SetDocumentation'
# Clear: 'ClearDocumentation'
for attr in prim.GetAttributes():
    print(attr.GetName(), attr.GetDocumentation())
    # Or
    print(attr.GetMetadata("documentation"))
#// ANCHOR_END: metadataDocs

#// ANCHOR: metadataDocsResult
"""
doubleSided Although some renderers treat all parametric or polygonal
        surfaces as if they were effectively laminae with outward-facing
        normals on both sides, some renderers derive significant optimizations
        by considering these surfaces to have only a single outward side,
        typically determined by control-point winding order and/or 
        orientation.  By doing so they can perform "backface culling" to
        avoid drawing the many polygons of most closed surfaces that face away
        from the viewer.
        
        However, it is often advantageous to model thin objects such as paper
        and cloth as single, open surfaces that must be viewable from both
        sides, always.  Setting a gprim's doubleSided attribute to 
        \c true instructs all renderers to disable optimizations such as
        backface culling for the gprim, and attempt (not all renderers are able
        to do so, but the USD reference GL renderer always will) to provide
        forward-facing normals on each side of the surface for lighting
        calculations.
extent Extent is re-defined on Cube only to provide a fallback value.
        \sa UsdGeomGprim::GetExtentAttr().
orientation Orientation specifies whether the gprim's surface normal 
        should be computed using the right hand rule, or the left hand rule.
        Please see for a deeper explanation and
        generalization of orientation to composed scenes with transformation
        hierarchies.
primvars:displayColor It is useful to have an "official" colorSet that can be used
        as a display or modeling color, even in the absence of any specified
        shader for a gprim.  DisplayColor serves this role; because it is a
        UsdGeomPrimvar, it can also be used as a gprim override for any shader
        that consumes a displayColor parameter.
primvars:displayOpacity Companion to displayColor that specifies opacity, broken
        out as an independent attribute rather than an rgba color, both so that
        each can be independently overridden, and because shaders rarely consume
        rgba parameters.
purpose Purpose is a classification of geometry into categories that 
        can each be independently included or excluded from traversals of prims 
        on a stage, such as rendering or bounding-box computation traversals.

        See for more detail about how 
        purpose is computed and used.
size Indicates the length of each edge of the cube.  If you
        author size you must also author extent.
        
        \sa GetExtentAttr()
visibility Visibility is meant to be the simplest form of "pruning" 
        visibility that is supported by most DCC apps.  Visibility is 
        animatable, allowing a sub-tree of geometry to be present for some 
        segment of a shot, and absent from others; unlike the action of 
        deactivating geometry prims, invisible geometry is still 
        available for inspection, for positioning, for defining volumes, etc.
xformOpOrder Encodes the sequence of transformation operations in the
        order in which they should be pushed onto a transform stack while
        visiting a UsdStage's prims in a graph traversal that will effect
        the desired positioning for this prim and its descendant prims.
        
        You should rarely, if ever, need to manipulate this attribute directly.
        It is managed by the AddXformOp(), SetResetXformStack(), and
        SetXformOpOrder(), and consulted by GetOrderedXformOps() and
        GetLocalTransformation().
"""
#// ANCHOR_END: metadataDocsResult

#// ANCHOR: metadataActive
from pxr import Sdf, Usd
### High Level ###
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
prim.SetActive(False)

### Low Level ###
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/cube")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.active = False
# Or
prim_spec.SetInfo(prim_spec.ActiveKey, True)
#// ANCHOR_END: metadataActive


#// ANCHOR: metadataAssetInfo
from pxr import Sdf, Usd
### High Level ###
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
prim.SetMetadata("assetInfo", {"identifier": Sdf.AssetPath("bicycler.usd")})
prim.SetAssetInfoByKey("name", "bicycle")
prim.SetAssetInfoByKey("version", "v001")
prim.SetAssetInfoByKey("payloadAssetDependencies", Sdf.AssetPathArray(["assetIndentifierA", "assetIndentifierA"]))
# Sdf.AssetPathArray([]) auto-casts all elements to Sdf.AssetPath objects.

### Low Level ###
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/cube")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.assetInfo = {"identifier": Sdf.AssetPath("bicycle.usd")}
prim_spec.assetInfo["name"] = "bicycle"
prim_spec.assetInfo["version"] = "v001"
prim_spec.assetInfo["payloadAssetDependencies"] = Sdf.AssetPathArray(["assetIndentifierA", "assetIndentifierA"])
# Sdf.AssetPathArray([]) auto-casts all elements to Sdf.AssetPath objects.
#// ANCHOR_END: metadataAssetInfo

#// ANCHOR: metadataCustomData
from pxr import Sdf, Usd
### High Level ###
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
prim.SetMetadata("customData", {"sizeUnit": "meter"})
prim.SetCustomDataByKey("nested:shape", "round")

### Low Level ###
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/cube")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.customData = {"myCoolData": "myCoolValue"}
#// ANCHOR_END: metadataCustomData


#// ANCHOR: metadataComment
from pxr import Sdf, Usd
### High Level ###
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
prim.SetMetadata("comment", "This is a cool prim!")

### Low Level ###
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/cube")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.SetInfo("comment", "This is a cool prim spec!")
#// ANCHOR_END: metadataComment

#// ANCHOR: metadataIcon
from pxr import Sdf, Usd
### High Level ###
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
prim.SetMetadata("customData", {"icon": "/path/to/icon.png"})
prim.SetCustomDataByKey("icon", "/path/to/icon.png")

### Low Level ###
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/cube")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.customData = {"icon": "/path/to/icon.png"}
#// ANCHOR_END: metadataIcon

#// ANCHOR: metadataHidden
from pxr import Sdf, Usd
### High Level ###
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
prim.SetHidden(True)

### Low Level ###
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/cube")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.SetInfo("hidden", True)
#// ANCHOR_END: metadataHidden

#// ANCHOR: metadataVariability
from pxr import Sdf, Usd
### High Level ###
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/box")
prim = stage.DefinePrim(prim_path, "Cube")
attr = prim.CreateAttribute("height", Sdf.ValueTypeNames.Double)
attr.SetMetadata("variability", Sdf.VariabilityUniform)
### Low Level ###
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/box")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.typeName = "Cube"
attr_spec = Sdf.AttributeSpec(prim_spec, "height", Sdf.ValueTypeNames.Double)
attr_spec.SetInfo("variability", Sdf.VariabilityVarying)
#// ANCHOR_END: metadataVariability

#// ANCHOR: metadataCustom
from pxr import Sdf, Usd
### High Level ###
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/box")
prim = stage.DefinePrim(prim_path, "Cube")
attr = prim.CreateAttribute("height", Sdf.ValueTypeNames.Double)
# This is not necessary to do explicitly as
# the high level API does this for us.
attr.SetMetadata("custom", True)
# Or
print(attr.IsCustom())
attr.SetCustom(True)
### Low Level ###
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/box")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.typeName = "Cube"
attr_spec = Sdf.AttributeSpec(prim_spec, "height", Sdf.ValueTypeNames.Double)
attr_spec.SetInfo("custom", True)
#// ANCHOR_END: metadataCustom

#// ANCHOR: debuggingTokens
from pxr import Tf
# To check if a symbol is active:
Tf.Debug.IsDebugSymbolNameEnabled("MY_SYMBOL_NAME")
# To print all symbols
docs = Tf.Debug.GetDebugSymbolDescriptions()
for name in Tf.Debug.GetDebugSymbolNames():
    desc = Tf.Debug.GetDebugSymbolDescription(name)
    print("{:<50} | {}".format(name, desc))
#// ANCHOR_END: debuggingTokens

#// ANCHOR: debuggingTokensMarkdown
from pxr import Tf
docs = Tf.Debug.GetDebugSymbolDescriptions()
print("| Variable Name | Description |")
print("|-|-|")
for name in Tf.Debug.GetDebugSymbolNames():
    desc = Tf.Debug.GetDebugSymbolDescription(name)
    print("| {} | {} |".format(name, desc))
#// ANCHOR_END: debuggingTokensMarkdown

#// ANCHOR: profilingTraceAttach
import os
from pxr import Trace, Usd
# Code with trace attached
class Bar():
    @Trace.TraceMethod
    def foo(self):
        print("Bar.foo")

@Trace.TraceFunction
def foo(stage):
    with Trace.TraceScope("InnerScope"):
        bar = Bar()
        for prim in stage.Traverse():
            prim.HasAttribute("size")
#// ANCHOR_END: profilingTraceAttach

#// ANCHOR: profilingTraceCollect
import os
from pxr import Trace, Usd
# The Trace.Collector() and Trace.Reporter.globalReporter return a singletons
# The default traces all go to TraceCategory::Default, this is not configurable via python
global_reporter = Trace.Reporter.globalReporter
global_reporter.ClearTree()
collector = Trace.Collector()
collector.Clear()
# Start recording events.
collector.enabled = True
# Enable the Usd Python API tracing (No the manually attached tracers)
collector.pythonTracingEnabled = False
# Run code
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
foo(stage)
# Stop recording events.
collector.enabled = False
# Print the ASCII report
trace_dir_path = os.path.dirname(os.path.expanduser("~/Desktop/UsdTracing"))
global_reporter.Report(os.path.join(trace_dir_path, "report.trace"))
global_reporter.ReportChromeTracingToFile(os.path.join(trace_dir_path,"report.json"))
#// ANCHOR_END: profilingTraceCollect

#// ANCHOR: profilingStopWatch
from pxr import Tf
sw = Tf.Stopwatch()
sw.Start()
sw.Stop()
sw.Start()
sw.Stop()
print(sw.GetMilliseconds(), sw.sampleCount)
sw.Reset()
# Add sampleCount + accumulated time from other stop watch
other_sw = Tf.StopWatch()
other_sw.Start()
other_sw.Stop()
sw.AddFrom(other_sw) 
print(sw.GetMilliseconds(), sw.sampleCount)
#// ANCHOR_END: profilingStopWatch

#// ANCHOR: pluginsRegistry
from pxr import Plug
registry = Plug.Registry()
for plugin in registry.GetAllPlugins():
    print(plugin.name, plugin.path, plugin.isLoaded)
    # To print the plugInfo.json content run:
    # print(plugin.metadata)
#// ANCHOR_END: pluginsRegistry

#// ANCHOR: assetResolverBound
from pxr import Ar
from usdAssetResolver import FileResolver
print(Ar.GetResolver())
print(Ar.GetUnderlyingResolver()) # Returns: <usdAssetResolver.FileResolver.Resolver object at <address>>
#// ANCHOR_END: assetResolverBound

#// ANCHOR: assetResolverScopedCache
from pxr import Ar
with Ar.ResolverScopedCache() as scope:
    resolver = Ar.GetResolver()
    path = resolver.Resolve("box.usda")
#// ANCHOR_END: assetResolverScopedCache

#// ANCHOR: assetResolverContextAccess
context_collection = stage.GetPathResolverContext()
activeResolver_context = context_collection.Get()[0]
#// ANCHOR_END: assetResolverContextAccess 

#// ANCHOR: assetResolverContextCreation
from pxr import Ar, Usd
from usdAssetResolver import FileResolver
resolver = Ar.GetUnderlyingResolver()
context_collection = resolver.CreateDefaultContext() # Returns: Ar.ResolverContext(FileResolver.ResolverContext())
context = context_collection.Get()[0]
context.ModifySomething() # Call specific functions of your resolver.
# Create a stage that uses the context
stage = Usd.Stage.CreateInMemory("/output/stage/filePath.usd", pathResolverContext=context)
# Or
stage = Usd.Stage.Open("/Existing/filePath/to/UsdFile.usd", pathResolverContext=context)
#// ANCHOR_END: assetResolverContextCreation

#// ANCHOR: assetResolverContextRefresh
from pxr import Ar
...
resolver = Ar.GetResolver()
# The resolver context is actually a list, as there can be multiple resolvers 
# running at the same time. In this example we only have a single non-URI resolver
# running, therefore we only have a single element in the list.
context_collection = stage.GetPathResolverContext()
activeResolver_context = context_collection.Get()[0]
# Your asset resolver has to Python expose methods to modify the context.
activeResolver_context.ModifySomething()
# Trigger Refresh (Some DCCs, like Houdini, additionally require node re-cooks.)
resolver.RefreshContext(context_collection)
...
#// ANCHOR_END: assetResolverContextRefresh

#// ANCHOR: assetResolverStageContextResolve
resolved_path = stage.ResolveIdentifierToEditTarget("someAssetIdentifier")
# Get the Python string
resolved_path_str = path.GetPathString() # Or str(resolved_path)
#// ANCHOR_END: assetResolverStageContextResolve

#// ANCHOR: assetResolverResolve
from pxr import Ar
resolver = Ar.GetResolver()
resolved_path = resolver.Resolve("someAssetIdentifier")
# Get the Python string
resolved_path_str = path.GetPathString() # Or str(resolved_path)
#// ANCHOR_END: assetResolverResolve

#// ANCHOR: assetResolverAssetPath
from pxr import Sdf
asset_path = Sdf.AssetPath("someAssetIdentifier", "/some/Resolved/Path.usd")
print(asset_path.path)         # Returns: "someAssetIdentifier"
print(asset_path.resolvedPath) # Returns: "/some/Resolved/Path.usd"
#// ANCHOR_END: assetResolverAssetPath


#// ANCHOR: noticeRegisterRevoke
from pxr import Tf, Usd
def callback(notice, sender):
    print(notice, sender)
# Add
# Global
listener = Tf.Notice.RegisterGlobally(Usd.Notice.StageContentsChanged, callback)
# Per Stage
listener = Tf.Notice.Register(Usd.Notice.StageContentsChanged, callback, stage)
# Remove
listener.Revoke()
#// ANCHOR_END: noticeRegisterRevoke


#// ANCHOR: noticeCommon
from pxr import Usd, Plug
# Generic (Do not send what stage they are from)
notice = Usd.Notice.StageContentsChanged
notice = Usd.Notice.StageEditTargetChanged
# Layer Muting
notice = Usd.Notice.LayerMutingChanged
# In the callback you can get the changed layers by calling:
# notice.GetMutedLayers()
# notice.GetUnmutedLayers()
# Object Changed
notice = Usd.Notice.ObjectsChanged
# In the callback you can get the following info by calling:
# notice.GetResyncedPaths()          # Changed Paths (Composition or Creation/Rename/Removal)
# notice.GetChangedInfoOnlyPaths()   # Attribute/Metadata value changes
# With these methods you can test if a Usd object 
# (UsdObject==BaseClass for Prims/Properties/Metadata) has been affected.
# notice.AffectedObject(UsdObject) (Generic)
# notice.ResyncedObject(UsdObject) (Composition Change)
# notice.ChangedInfoOnly(UsdObject) (Value Change)
# notice.HasChangedFields(UsdObject/SdfPath) 
# notice.GetChangedFields(UsdObject/SdfPath)
# Plugin registered
notice = Plug.Notice.DidRegisterPlugins
# notice.GetNewPlugins() # Get new plugins
#// ANCHOR_END: noticeCommon


#// ANCHOR: noticePlugins
from pxr import Tf, Usd, Plug

def DidRegisterPlugins_callback(notice):
    print(notice, notice.GetNewPlugins())

listener = Tf.Notice.RegisterGlobally(Plug.Notice.DidRegisterPlugins, DidRegisterPlugins_callback)
listener.Revoke()
#// ANCHOR_END: noticePlugins


#// ANCHOR: noticeCommonApplied
from pxr import Tf, Usd, Sdf

def ObjectsChanged_callback(notice, sender):
    stage = notice.GetStage()
    print("---")
    print(">", notice, sender)
    print(">> (notice.GetResyncedPaths) - Updated paths", notice.GetResyncedPaths())
    print(">> (notice.GetChangedInfoOnlyPaths) - Attribute/Metadata value changes", notice.GetChangedInfoOnlyPaths())
    
    prim = stage.GetPrimAtPath("/bicycle")
    if prim:
        # Check if a specific UsdObject was affected
        print(">> (notice.AffectedObject) - Something changed for", prim.GetPath(), notice.AffectedObject(prim))
        print(">> (notice.ResyncedObject) - Updated path for", prim.GetPath(), notice.ResyncedObject(prim))
        print(">> (notice.ChangedInfoOnly) - Attribute/Metadata ChangedInfoOnly", prim.GetPath(), notice.ChangedInfoOnly(prim))
        print(">> (notice.HasChangedFields) - Attribute/Metadata HasChanges", prim.GetPath(), notice.HasChangedFields(prim))
        print(">> (notice.GetChangedFields) - Attribute/Metadata ChangedFields", prim.GetPath(), notice.GetChangedFields(prim))

    attr = stage.GetAttributeAtPath("/bicycle.tire:size")
    if attr:
        # Check if a specific UsdObject was affected
        print(">> (notice.AffectedObject) - Something changed for", attr.GetPath(), notice.AffectedObject(attr))
        print(">> (notice.ResyncedObject) - Updated path for", attr.GetPath(), notice.ResyncedObject(attr))
        print(">> (notice.ChangedInfoOnly) - Attribute/Metadata ChangedInfoOnly", attr.GetPath(), notice.ChangedInfoOnly(attr))
        print(">> (notice.HasChangedFields) - Attribute/Metadata HasChanges", attr.GetPath(), notice.HasChangedFields(attr))
        print(">> (notice.GetChangedFields) - Attribute/Metadata ChangedFields", attr.GetPath(), notice.GetChangedFields(attr))

# Add
listener = Tf.Notice.RegisterGlobally(Usd.Notice.ObjectsChanged, ObjectsChanged_callback)
# Edit
stage = Usd.Stage.CreateInMemory()
# Create Prim
prim = stage.DefinePrim("/bicycle")
# Results:
# >> <pxr.Usd.ObjectsChanged object at 0x7f071d58e820> Usd.Stage.Open(rootLayer=Sdf.Find('anon:0x7f06927ccc00:tmp.usda'), sessionLayer=Sdf.Find('anon:0x7f06927cdb00:tmp-session.usda'))
# >> (notice.GetResyncedPaths) - Updated paths [Sdf.Path('/bicycle')]
# >> (notice.GetChangedInfoOnlyPaths) - Attribute/Metadata value changes []
# >> (notice.AffectedObject) - Something changed for /bicycle True
# >> (notice.ResyncedObject) - Updated path for /bicycle True
# >> (notice.ChangedInfoOnly) - Attribute/Metadata ChangedFieldsOnly /bicycle False
# >> (notice.HasChangedFields) - Attribute/Metadata HasChanges /bicycle True
# >> (notice.GetChangedFields) - Attribute/Metadata ChangedFields /bicycle ['specifier']
# Create Attribute
attr = prim.CreateAttribute("tire:size", Sdf.ValueTypeNames.Float)
# Results:
# >> <pxr.Usd.ObjectsChanged object at 0x7f071d58e820> Usd.Stage.Open(rootLayer=Sdf.Find('anon:0x7f06927ccc00:tmp.usda'), sessionLayer=Sdf.Find('anon:0x7f06927cdb00:tmp-session.usda'))
# >> (notice.GetResyncedPaths) - Updated paths [Sdf.Path('/bicycle.tire:size')]
# >> (notice.GetChangedInfoOnlyPaths) - Attribute/Metadata value changes []
# >> (notice.AffectedObject) - Something changed for /bicycle False
# >> (notice.ResyncedObject) - Updated path for /bicycle False
# >> (notice.ChangedInfoOnly) - Attribute/Metadata ChangedInfoOnly /bicycle False
# >> (notice.HasChangedFields) - Attribute/Metadata HasChanges /bicycle False
# >> (notice.GetChangedFields) - Attribute/Metadata ChangedFields /bicycle []
# >> (notice.AffectedObject) - Something changed for /bicycle.tire:size True
# >> (notice.ResyncedObject) - Updated path for /bicycle.tire:size True
# >> (notice.ChangedInfoOnly) - Attribute/Metadata ChangedInfoOnly /bicycle.tire:size False
# >> (notice.HasChangedFields) - Attribute/Metadata HasChanges /bicycle.tire:size True
# >> (notice.GetChangedFields) - Attribute/Metadata ChangedFields /bicycle.tire:size ['custom']
# Remove
listener.Revoke()
#// ANCHOR_END: noticeCommonApplied


#// ANCHOR: noticeCustom
from pxr import Tf, Usd
# Create notice callback
def callback(notice, sender):
    print(notice, sender)
# Create a new notice type
class CustomNotice(Tf.Notice):
    '''My custom notice'''
# Get fully qualified domain name
CustomNotice_FQN = "{}.{}".format(CustomNotice.__module__, CustomNotice.__name__)
# Register notice
# Important: If you overwrite the CustomNotice Class in the same Python session
# (for example when running this snippet twice in a DCC Python session), you
# cannot send anymore notifications as the defined type will have lost the pointer
# to the class, but you can't re-define it because of how the type definition works.
if not Tf.Type.FindByName(CustomNotice_FQN):
    Tf.Type.Define(CustomNotice)
# Register notice listeners
# Globally
listener = Tf.Notice.RegisterGlobally(CustomNotice, callback)
# For a specific stage
sender = Usd.Stage.CreateInMemory()
listener = Tf.Notice.Register(CustomNotice, callback, sender)
# Send notice
CustomNotice().SendGlobally()
CustomNotice().Send(sender)
# Remove listener
listener.Revoke()
#// ANCHOR_END: noticeCustom


#// ANCHOR: kindRegistry
from pxr import Kind
registry = Kind.Registry()
for kind in registry.GetAllKinds():
    base_kind = Kind.Registry.GetBaseKind(kind)
    print(f"{kind:<15} - Base Kind - {base_kind}")
# Returns:
"""
set             - Base Kind - assembly
assembly        - Base Kind - group
fx              - Base Kind - component
environment     - Base Kind - assembly
character       - Base Kind - component
group           - Base Kind - model
component       - Base Kind - model
model           - Base Kind 
subcomponent    - Base Kind 
"""    
print(registry.HasKind("fx")) # Returns: True
print(registry.IsA("fx", "model")) # Returns: True
#// ANCHOR_END: kindRegistry

#// ANCHOR: kindTraversal
from pxr import Kind, Sdf, Usd
stage = Usd.Stage.CreateInMemory()
prim = stage.DefinePrim(Sdf.Path("/set"), "Xform")
Usd.ModelAPI(prim).SetKind("set")
prim = stage.DefinePrim(Sdf.Path("/set/garage"), "Xform")
Usd.ModelAPI(prim).SetKind("group")
prim = stage.DefinePrim(Sdf.Path("/set/garage/bicycle"), "Xform")
Usd.ModelAPI(prim).SetKind("prop")
prim = stage.DefinePrim(Sdf.Path("/set/yard"), "Xform")
Usd.ModelAPI(prim).SetKind("group")
prim = stage.DefinePrim(Sdf.Path("/set/yard/explosion"), "Xform")
Usd.ModelAPI(prim).SetKind("fx")
# Result:
print(stage.ExportToString())
"""
def Xform "set" (
    kind = "set"
)
{
    def Xform "garage" (
        kind = "group"
    )
    {
        def Xform "bicycle" (
            kind = "prop"
        )
        {
        }
    }

    def Xform "yard" (
        kind = "group"
    )
    {
        def Xform "explosion" (
            kind = "fx"
        )
        {
        }
    }
}
"""
for prim in stage.Traverse():
    print("{:<20} - IsModel: {} - IsGroup: {}".format(prim.GetPath().pathString, prim.IsModel(), prim.IsGroup()))
# Returns:
"""
/set                 - IsModel: True - IsGroup: True
/set/garage          - IsModel: True - IsGroup: True
/set/garage/bicycle  - IsModel: True - IsGroup: False
/set/yard            - IsModel: True - IsGroup: True
/set/yard/explosion  - IsModel: True - IsGroup: False
"""
registry = Kind.Registry()
for prim in stage.Traverse():
    kind = Usd.ModelAPI(prim).GetKind()
    print("{:<25} - {:<5} - {}".format(prim.GetPath().pathString, kind, registry.IsA("fx", "component")))

# Failed traversal because of missing kinds
stage = Usd.Stage.CreateInMemory()
prim = stage.DefinePrim(Sdf.Path("/set"), "Xform")
Usd.ModelAPI(prim).SetKind("set")
prim = stage.DefinePrim(Sdf.Path("/set/garage"), "Xform")
prim = stage.DefinePrim(Sdf.Path("/set/garage/bicycle"), "Xform")
Usd.ModelAPI(prim).SetKind("prop")
prim = stage.DefinePrim(Sdf.Path("/set/yard"), "Xform")
prim = stage.DefinePrim(Sdf.Path("/set/yard/explosion"), "Xform")
Usd.ModelAPI(prim).SetKind("fx")
registry = Kind.Registry()
for prim in stage.Traverse():
    kind = Usd.ModelAPI(prim).GetKind()
    print("{:<20} - Kind: {:10} - IsA('component') {}".format(prim.GetPath().pathString, kind, registry.IsA(kind, "component")))
    print("{:<20} - IsModel: {} - IsGroup: {}".format(prim.GetPath().pathString, prim.IsModel(), prim.IsGroup()))
"""
/set                 - Kind: set        - IsA('component') False
/set                 - IsModel: True - IsGroup: True
/set/garage          - Kind:            - IsA('component') False
/set/garage          - IsModel: False - IsGroup: False
/set/garage/bicycle  - Kind: prop       - IsA('component') True
/set/garage/bicycle  - IsModel: False - IsGroup: False
/set/yard            - Kind:            - IsA('component') False
/set/yard            - IsModel: False - IsGroup: False
/set/yard/explosion  - Kind: fx         - IsA('component') True
/set/yard/explosion  - IsModel: False - IsGroup: False
"""
#// ANCHOR_END: kindTraversal



#// ANCHOR: animationOverview
from pxr import Sdf, Usd
### High Level ###
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Cube")
size_attr = prim.GetAttribute("size")
for frame in range(1001, 1005):
    time_code = Usd.TimeCode(float(frame - 1001))
    # .Set() takes args in the .Set(<value>, <frame>) format
    size_attr.Set(frame, time_code)
print(size_attr.Get(1005)) # Returns: 4

### Low Level ###
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.specifier = Sdf.SpecifierDef
prim_spec.typeName = "Cube"
attr_spec = Sdf.AttributeSpec(prim_spec, "size", Sdf.ValueTypeNames.Double)
for frame in range(1001, 1005):
    value = float(frame - 1001)
    # .SetTimeSample() takes args in the .SetTimeSample(<path>, <frame>, <value>) format
    layer.SetTimeSample(attr_spec.path, frame, value)
print(layer.QueryTimeSample(attr_spec.path, 1005)) # Returns: 4
#// ANCHOR_END: animationOverview

#// ANCHOR: animationTimeCode
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Cube")
size_attr = prim.GetAttribute("size")
## Set default value
time_code = Usd.TimeCode.Default()
size_attr.Set(10, time_code)
# Or:
size_attr.Set(10) # The default is to set `default` (non-per-frame) data.
## Set per frame value
for frame in range(1001, 1005):
    time_code = Usd.TimeCode(frame)
    size_attr.Set(frame, time_code)
# Or
# As with Sdf.Path implicit casting from strings in a lot of places in the USD API,
# the time code is implicitly casted from a Python float. 
# It is recommended to do the above, to be more future proof of 
# potentially encoding time unit based samples.
for frame in range(1001, 1005):
    size_attr.Set(frame, frame)
## Other than that the TimeCode class only has a via Is/Get methods of interest:
size_attr.IsDefault() # Returns: True if no time value was given
size_attr.IsNumeric() # Returns: True if not IsDefault()
size_attr.GetValue() # Returns: The time value (if not IsDefault()
#// ANCHOR_END: animationTimeCode

#// ANCHOR: animationLayerOffset
from pxr import Sdf, Usd
# The Sdf.LayerOffset(<offset>, <scale>) class has 
# no attributes/methods other than LayerOffset.offset & LayerOffset.scale.
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/animal")
root_layer = stage.GetRootLayer()
## For sublayering via Python, we first need to sublayer, then edit offset.
# In Houdini we can't due this directly due to Houdini's stage handling system.
file_path = "/opt/hfs19.5/houdini/usd/assets/pig/pig.usd"
root_layer.subLayerPaths.append(file_path)
print(root_layer.subLayerPaths)
print(root_layer.subLayerOffsets)
# Since layer offsets are read only, we need to assign it to a new one in-place.
# !DANGER! Due to how it is exposed to Python, we can't assign a whole array with the
# new offsets, instead we can only swap individual elements in the array, so that the
# array pointer is kept intact.
root_layer.subLayerOffsets[0] = Sdf.LayerOffset(25, 1) 
## For references
ref = Sdf.Reference(file_path, "/pig", Sdf.LayerOffset(25, 1))
prim = stage.DefinePrim(prim_path)
ref_API = prim.GetReferences()
ref_API.AddReference(ref)
ref = Sdf.Reference("", "/animal", Sdf.LayerOffset(50, 1))
internal_prim = stage.DefinePrim(prim_path.ReplaceName("internal"))
ref_API = internal_prim.GetReferences()
ref_API.AddReference(ref)
## For payloads
payload = Sdf.Payload(file_path, "/pig", Sdf.LayerOffset(25, 1))
prim = stage.DefinePrim(prim_path)
payload_API = prim.GetPayloads()
payload_API.AddPayload(payload)
#// ANCHOR_END: animationLayerOffset


#// ANCHOR: animationWrite
from pxr import Sdf, Usd
### High Level ###
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Cube")
size_attr = prim.GetAttribute("size")
## Set default value
time_code = Usd.TimeCode.Default()
size_attr.Set(10, time_code)
# Or:
size_attr.Set(10) # The default is to set `default` (non-per-frame) data.
## Set per frame value
for frame in range(1001, 1005):
    value = float(frame - 1001)
    time_code = Usd.TimeCode(frame)
    size_attr.Set(value, time_code)
# Clear default value
size_attr.ClearDefault(1001)
# Remove a time sample
size_attr.ClearAtTime(1001)

### Low Level ###
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.specifier = Sdf.SpecifierDef
prim_spec.typeName = "Cube"
attr_spec = Sdf.AttributeSpec(prim_spec, "size", Sdf.ValueTypeNames.Double)
## Set default value
attr_spec.default = 10
## Set per frame value
for frame in range(1001, 1005):
    value = float(frame - 1001)
    layer.SetTimeSample(attr_spec.path, frame, value)
# Clear default value
attr_spec.ClearDefaultValue()
# Remove a time sample
layer.EraseTimeSample(attr_spec.path, 1001)
#// ANCHOR_END: animationWrite

#// ANCHOR: animationRead
from pxr import Gf, Sdf, Usd
### High Level ###
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Cube")
size_attr = prim.GetAttribute("size")
size_attr.Set(10) 
for frame in range(1001, 1005):
    time_code = Usd.TimeCode(frame)
    size_attr.Set(frame-1001, time_code)
# Query the default value (must be same value source aka layer as the time samples).
print(size_attr.Get()) # Returns: 10
# Query the animation time samples
for time_sample in size_attr.GetTimeSamples():
    print(size_attr.Get(time_sample))
# Returns:
"""
0.0, 1.0, 2.0, 3.0
"""
# Other important time sample methods:
# !Danger! For value clipped (per frame loaded layers),
# this will look into all layers, which is quite expensive.
print(size_attr.GetNumTimeSamples()) # Returns: 4
# You should rather use:
# This does a check for time sample found > 2.
# So it stops looking for more samples after the second sample.
print(size_attr.ValueMightBeTimeVarying()) # Returns: True
## We can also query what the closest time sample to a frame:
print(size_attr.GetBracketingTimeSamples(1003.3)) 
# Returns: (<Found sample>, <lower closest sample>, <upper closest sample>)
(True, 1003.0, 1004.0)
## We can also query time samples in a range. This is useful if we only want to lookup and copy
# a certain range, for example in a pre-render script.
print(size_attr.GetTimeSamplesInInterval(Gf.Interval(1001, 1003))) 
# Returns: [1001.0, 1002.0, 1003.0]


### Low Level ###
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.specifier = Sdf.SpecifierDef
prim_spec.typeName = "Cube"
attr_spec = Sdf.AttributeSpec(prim_spec, "size", Sdf.ValueTypeNames.Double)
attr_spec.default = 10
for frame in range(1001, 1005):
    value = float(frame - 1001)
    layer.SetTimeSample(attr_spec.path, frame, value)
# Query the default value
print(attr_spec.default) # Returns: 10
# Query the animation time samples
time_sample_count = layer.GetNumTimeSamplesForPath(attr_spec.path)
for time_sample in layer.ListTimeSamplesForPath(attr_spec.path):
    print(layer.QueryTimeSample(attr_spec.path, time_sample))
# Returns:
"""
0.0, 1.0, 2.0, 3.0
"""
## We can also query what the closest time sample is to a frame:
print(layer.GetBracketingTimeSamplesForPath(attr_spec.path, 1003.3)) 
# Returns: (<Found sample>, <lower closest sample>, <upper closest sample>)
(True, 1003.0, 1004.0)
#// ANCHOR_END: animationRead

#// ANCHOR: animationTimeVarying
# !Danger! For value clipped (per frame loaded layers),
# this will look into all layers, which is quite expensive.
print(size_attr.GetNumTimeSamples())
# You should rather use:
# This does a check for time sample found > 2.
# So it stops looking for more samples after the second sample.
print(size_attr.ValueMightBeTimeVarying())
#// ANCHOR_END: animationTimeVarying

#// ANCHOR: animationSpecialValues
from pxr import Sdf, Usd
### High Level ###
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Cube")
size_attr = prim.GetAttribute("size")
for frame in range(1001, 1005):
    time_code = Usd.TimeCode(frame)
    size_attr.Set(frame - 1001, time_code)
## Value Blocking
size_attr.Set(1001, Sdf.ValueBlock())

### Low Level ###
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.specifier = Sdf.SpecifierDef
prim_spec.typeName = "Cube"
attr_spec = Sdf.AttributeSpec(prim_spec, "size", Sdf.ValueTypeNames.Double)
for frame in range(1001, 1005):
    value = float(frame - 1001)
    layer.SetTimeSample(attr_spec.path, frame, value)

## Value Blocking
layer.SetTimeSample(attr_spec.path, 1001, Sdf.ValueBlock())
#// ANCHOR_END: animationSpecialValues

#// ANCHOR: animationFPS
from pxr import Sdf, Usd
### High Level ###
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Cube")
size_attr = prim.GetAttribute("size")
for frame in range(1001, 1005):
    time_code = Usd.TimeCode(frame)
    size_attr.Set(frame - 1001, time_code)
# FPS Metadata
stage.SetTimeCodesPerSecond(25)
stage.SetFramesPerSecond(25)
stage.SetStartTimeCode(1001)
stage.SetEndTimeCode(1005)

### Low Level ###
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.specifier = Sdf.SpecifierDef
prim_spec.typeName = "Cube"
attr_spec = Sdf.AttributeSpec(prim_spec, "size", Sdf.ValueTypeNames.Double)
for frame in range(1001, 1005):
    value = float(frame - 1001)
    layer.SetTimeSample(attr_spec.path, frame, value)
# FPS Metadata
time_samples = Sdf.Layer.ListAllTimeSamples()
layer.timeCodesPerSecond = 25
layer.framesPerSecond = 25
layer.startTimeCode = time_samples[0]
layer.endTimeCode = time_samples[-1]
#// ANCHOR_END: animationFPS


#// ANCHOR: animationStitchCmdlineTool
...
openedFiles = [Sdf.Layer.FindOrOpen(fname) for fname in results.usdFiles]
... 
# the extra computation and fail more gracefully
try:
    for usdFile in openedFiles:
        UsdUtils.StitchLayers(outLayer, usdFile)
        outLayer.Save()
# if something in the authoring fails, remove the output file
except Exception as e:
    print('Failed to complete stitching, removing output file %s' % results.out)
    print(e)
    os.remove(results.out) 
...
#// ANCHOR_END: animationStitchCmdlineTool

#// ANCHOR: animationStitchClipsUtils
from pxr import Sdf, UsdUtils

clip_time_code_start = 1001
clip_time_code_end = 1003
clip_set_name = "cacheClip"
clip_prim_path = "/prim"
clip_interpolate_missing = False
time_sample_files = ["/cache/value_clips/time_sample.1001.usd",
                     "/cache/value_clips/time_sample.1002.usd",
                     "/cache/value_clips/time_sample.1003.usd"]
topology_file_path = "/cache/value_clips/topology.usd"
manifest_file_path = "/cache/value_clips/manifest.usd"
cache_file_path = "/cache/cache.usd"

# We can also use:
# topology_file_path = UsdUtils.GenerateClipTopologyName(cache_file_path)
# Returns: "/cache/cache.topology.usd"
# manifest_file_path = UsdUtils.GenerateClipManifestName(cache_file_path)
# Returns: "/cache/cache.manifest.usd"

topology_layer = Sdf.Layer.CreateNew(topology_file_path)
manifest_layer = Sdf.Layer.CreateNew(manifest_file_path)
cache_layer = Sdf.Layer.CreateNew(cache_file_path)

UsdUtils.StitchClipsTopology(topology_layer, time_sample_files)
UsdUtils.StitchClipsManifest(manifest_layer, topology_layer, 
                             time_sample_files, clip_prim_path)

UsdUtils.StitchClips(cache_layer,
                     time_sample_files,
                     clip_prim_path, 
                     clip_time_code_start,
                     clip_time_code_end,
                     clip_interpolate_missing,
                     clip_set_name)
cache_layer.Save()

# Result in "/cache/cache.usd"
"""
(
    framesPerSecond = 24
    metersPerUnit = 1
    subLayers = [
        @./value_clips/topology.usd@
    ]
    timeCodesPerSecond = 24
)

def "prim" (
    clips = {
        dictionary cacheClip = {
            double2[] active = [(1001, 0), (1002, 1), (1003, 2)] 
            asset[] assetPaths = [@./value_clips/time_sample.1001.usd@, @./value_clips/time_sample.1002.usd@, @./value_clips/time_sample.1003.usd@]
            asset manifestAssetPath = @./value_clips/manifest.usd@
            string primPath = "/prim"
            double2[] times = [(1001, 1001), (1002, 1002), (1003, 1003)]
        }
    }
    clipSets = ["cacheClip"]
)
{
}
"""

## API Overview
UsdUtils
# Generate topology and manifest files based USD preferred naming convention.
UsdUtils.GenerateClipTopologyName("/cache_file.usd") # Returns: "/cache_file.topology.usd"
UsdUtils.GenerateClipManifestName("/cache_file.usd") # Returns: "/cache_file.manifest.usd"
# Open layers
topology_layer = Sdf.Layer.CreateNew(topology_file_path)
manifest_layer = Sdf.Layer.CreateNew(manifest_file_path)
cache_layer = Sdf.Layer.CreateNew(cache_file_path)
## Create topology and manifest. This is the heavy part of creating value clips
## as it has to open all layers.
# Generate topology layer, this opens all the time sample layers and copies all
# attributes that don't have time samples and relationships into the topology_layer.
UsdUtils.StitchClipsTopology(topology_layer, time_sample_files)
# Generate manifest layer, this opens all the time sample layers and creates a 
# hierarchy without values of all attributes that have time samples. This is the inverse
# of the topology layer except it doesn't create values. The hierarchy is then used to
# determine what a clip should load as animation. 
UsdUtils.StitchClipsManifest(manifest_layer, topology_layer, 
                             time_sample_files, clip_prim_path)
# Generate cache layer, this creates the metadata that links to the above created files.
UsdUtils.StitchClips(cache_layer,
                     time_sample_files,
                     clip_prim_path, 
                     clip_time_code_start,
                     clip_time_code_end,
                     clip_interpolate_missing,
                     clip_set_name)
#// ANCHOR_END: animationStitchClipsUtils


#// ANCHOR: animationStitchClipsAPI
from pxr import Sdf, Usd, UsdUtils

time_sample_files = ["/cache/value_clips/time_sample.1001.usd",
                     "/cache/value_clips/time_sample.1002.usd",
                     "/cache/value_clips/time_sample.1003.usd"]
time_sample_asset_paths = Sdf.AssetPathArray(time_sample_files)
topology_file_path = "/cache/value_clips/topology.usd"
manifest_file_path = "/cache/value_clips/manifest.usd"
cache_file_path = "/cache/cache.usd"

topology_layer = Sdf.Layer.CreateNew(topology_file_path)
manifest_layer = Sdf.Layer.CreateNew(manifest_file_path)
cache_layer = Sdf.Layer.CreateNew(cache_file_path)

UsdUtils.StitchClipsTopology(topology_layer, time_sample_files)
UsdUtils.StitchClipsManifest(manifest_layer, topology_layer, 
                             time_sample_files, clip_prim_path)

clip_set_name = "cacheClip"
clip_prim_path = "/prim"
clip_interpolate_missing = False

# For simplicity in this example we already know where the asset roots are.
# If you need to check where they are, you can traverse the topology layer,
# as it contains the full hierarchy of the per frame files.
prim = stage.DefinePrim("/valueClippedPrim", "Xform")
# The clips API is a small wrapper around setting metadata fields. 
clips_API = Usd.ClipsAPI(prim)
# Most function signatures work via the following args:
# clips_API.<method>(<methodArg>, <clipSetName>)
# We'll only be looking at non-template value clips related methods here.
## We have Get<MethodName>/Set<MethodName> for all metadata keys:
# clips_API.Get/SetClipPrimPath 
# clips_API.Get/SetClipAssetPaths
# clips_API.Get/SetClipManifestAssetPath
# clips_API.Get/SetClipActive
# clips_API.Get/SetClipTimes 
# clips_API.Get/SetInterpolateMissingClipValues
## To get/set the whole clips metadata dict, we can run:
# clips_API.Get/SetClips()
## To get/set what clips are active:
# clips_API.Get/SetClipSets

## Convenience methods for generating a manifest based on the
# clips set by clips_API.SetClipAssetPaths
# clips_API.GenerateClipManifest
## Or from a user specified list. This is similar to UsdUtils.StitchClipsManifest()
# clips_API.GenerateClipManifestFromLayers

## Get the resolved asset paths in 'assetPaths' metadata.
# clips_API.ComputeClipAssetPaths

prim = stage.DefinePrim("/valueClippedPrim", "Xform")
clips_API = Usd.ClipsAPI(prim)
clips_API.SetClipPrimPath(clip_prim_path, clip_set_name)
clips_API.SetClipAssetPaths(time_sample_asset_paths, clip_set_name)
clips_API.SetClipActive([(1001, 0), (1002, 1), (1003, 2)], clip_set_name)
clips_API.SetClipTimes([(1001, 1001), (1002, 1001), (1003, 1001)], clip_set_name)
clips_API.SetInterpolateMissingClipValues(clip_interpolate_missing, clip_set_name)
# We can also print all clip metadata
print(clips_API.GetClips())
# Enable the clip
clip_sets_active = Sdf.StringListOp.CreateExplicit([clip_set_name])
clips_API.SetClipSets(clip_sets_active)
#Returns:
"""
{'cacheClip': 
    {
        'primPath': '/prim',
        'interpolateMissingClipValues': False, 
        'active': Vt.Vec2dArray(3, (Gf.Vec2d(1001.0, 0.0), Gf.Vec2d(1002.0, 1.0), Gf.Vec2d(1003.0, 2.0))),
        'assetPaths': Sdf.AssetPathArray(3, (Sdf.AssetPath('/cache/value_clips/time_sample.1001.usd'),
                                            Sdf.AssetPath('/cache/value_clips/time_sample.1002.usd'),
                                            Sdf.AssetPath('/cache/value_clips/time_sample.1003.usd'))),
        'times': Vt.Vec2dArray(3, (Gf.Vec2d(1001.0, 1001.0), Gf.Vec2d(1002.0, 1001.0), Gf.Vec2d(1003.0, 1001.0)))
    }
}
"""
#// ANCHOR_END: animationStitchClipsAPI


#// ANCHOR: schemasOverview
### Typed Schemas ###
# From type name
prim_type_name = prim.GetTypeName()
prim_typed_schema = Usd.SchemaRegistry.GetTypeFromName(prim_type_name).pythonClass(prim)
# From prim type info
prim_typed_schema = prim.GetPrimTypeInfo().GetSchemaType().pythonClass(prim)

### API Schemas ###
# Non-Applied API Schemas
non_applied_api_schema = Usd.ModelAPI(prim)
# Applied API Schemas
applied_api_schema = UsdGeom.MotionAPI.Apply(prim)
#// ANCHOR_END: schemasOverview

#// ANCHOR: schemasTyped
###### Typed Schemas ######
### High Level ###
# Has: 'IsA',
# Get: 'GetTypeName'
# Set: 'SetTypeName'
# Clear: 'ClearTypeName'
from pxr import Sdf, Usd, UsdGeom
stage = Usd.Stage.CreateInMemory()

# Define prim via stage
prim_path = Sdf.Path("/bicycleA")
prim = stage.DefinePrim(prim_path, "Cube")
# Define prim via typed schema
prim_path = Sdf.Path("/bicycleB")
prim_typed_schema = UsdGeom.Cube.Define(stage, prim_path)
# Returns the schema class object, so we have to get the prim
prim = prim_typed_schema.GetPrim()
# Since the "Cube" schema is a subclass of the
# non.concrete typed UsdGeom.Boundable schema, we can check:
print(prim.IsA(UsdGeom.Cube)) # Returns: True
print(prim.IsA(UsdGeom.Boundable)) # Returns: True
# To remove the type, we can call:
# prim.ClearTypeName()
# To access the schema class methods, we give our prim to the 
# class constructor:
prim_typed_schema = UsdGeom.Cube(prim)
# The typed Cube schema for example has a Get/Set method for the schema's size attribute.
prim_typed_schema.GetSizeAttr().Set(5)
# Or we let Usd gives us the Python class
prim_typed_schema = prim.GetPrimTypeInfo().GetSchemaType().pythonClass(prim)
prim_typed_schema.GetSizeAttr().Set(10)
# Or we get it from the type name
prim_typed_schema = Usd.SchemaRegistry.GetTypeFromName(prim.GetTypeName()).pythonClass(prim)

### Low Level ###
# To set typed schemas via the low level API, we just 
# need to set the PrimSpec.typeName = "<SchemaName>"
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.typeName = "Cube"
#// ANCHOR_END: schemasTyped


#// ANCHOR: schemasAPI
###### API Schemas ######
### High Level ###
# Has: 'HasAPI', 'CanApplyAPI'
# Get: 'GetAppliedSchemas'
# Set: 'AddAppliedSchema', 'ApplyAPI'
# Clear: 'RemoveAppliedSchema', 'RemoveAPI'
from pxr import Sdf, Usd, UsdGeom
stage = Usd.Stage.CreateInMemory()

### Applied Schemas ###
# Define prim via stage
prim_path = Sdf.Path("/bicycleA")
prim = stage.DefinePrim(prim_path, "Cube")
# Check if it can be applied
print(UsdGeom.MotionAPI.CanApply(prim)) # Returns True
# Apply API schema (in active layer),
prim.ApplyAPI("UsdGeomModelAPI") # Returns: True
# Add applied schema
# This does not check if the schema actually exists, 
# you have to use this for codeless schemas.
prim.AddAppliedSchema("SkelBindingAPI") # Returns: True #
# Apply and get the schema class (preferred usage)
applied_api_schema = UsdGeom.MotionAPI.Apply(prim)
# Remove applied schema (in active layer)
# prim.RemoveAppliedSchema("SkelBindingAPI")
# prim.RemoveAPI("UsdGeomModelAPI")
# For multi-apply schemas, we can feed in our custom name,
# for example for collections it drives the collection name.
prim.ApplyAPI("UsdCollectionAPI", "myCoolCollectionName")
applied_multi_api_schema = Usd.CollectionAPI.Apply(prim, "myCoolCollectionName")
### Non-Applied Schemas ###
# Non-Applied schemas do not have an `Apply` method
# (who would have guessed that?)
non_applied_api_schema = Usd.ModelAPI(prim)

### Low Level ###
# To set applied API schemas via the low level API, we just 
# need to set the `apiSchemas` key to a Token Listeditable Op.
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
schemas = Sdf.TokenListOp.Create(
    prependedItems=["SkelBindingAPI", "UsdGeomModelAPI"]
)
prim_spec.SetInfo("apiSchemas", schemas)
# We don't have nice access the the schema class as in the high level API
#// ANCHOR_END: schemasAPI


#// ANCHOR: schemasPluginRegistry
from pxr import Plug, Tf, Usd
registry = Plug.Registry()
print(">>>>>", "Typed Schemas")
for type_name in registry.GetAllDerivedTypes(Usd.Typed):
    print(type_name)
print(">>>>>", "API Schemas")
for type_name in registry.GetAllDerivedTypes(Usd.APISchemaBase):
    print(type_name)

# For example to lookup where the "Cube" type is registered from,
# we can run:
print(">>>>>", "Cube Schema Plugin Source")
plugin = registry.GetPluginForType(Tf.Type.FindByName("UsdGeomCube"))
print(plugin.name)
print(plugin.path)
print(plugin.resourcePath)
print(plugin.metadata)
#// ANCHOR_END: schemasPluginRegistry

#// ANCHOR: schemasRegistry
from pxr import Plug, Sdf, Tf, Usd
registry = Usd.Schema.Registry()

## Get Tf.Type registry entry (which allows us to get the Python class)
## The result can also be used to run IsA checks for typed schemas.
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycleA")
prim = stage.DefinePrim(prim_path, "Cube")
print(prim.IsA(registry.GetTypeFromName("UsdGeomImageable"))) # Returns: True
print(prim.IsA(registry.GetTypeFromName("UsdGeomImageable").pythonClass)) # Returns: True


# GetTypeFromName allows prim type names and the Tf.Type.typeName.
print(registry.GetTypeFromName("UsdGeomCube"))      # Returns: Tf.Type("UsdGeomCube")
print(registry.GetTypeFromName("Cube"))             # Returns: Tf.Type("UsdGeomCube")
# For typed schemas we can also use:
print(registry.GetTypeFromSchemaTypeName("Imageable")) # Returns: Tf.Type('UsdGeomImageable') -> Tf.Type.typeName gives us 'UsdGeomImageable'
print(registry.GetTypeFromSchemaTypeName("Cube"))      # Returns: Tf.Type("UsdGeomCube") -> Tf.Type.typeName gives us 'UsdGeomCube'
print(registry.GetSchemaTypeName("UsdGeomImageable"))  # Returns: "Imageable"
print(registry.GetSchemaTypeName("UsdGeomCube"))       # Returns: "Cube"
# For concrete typed schemas:
print(registry.GetConcreteSchemaTypeName("UsdGeomCube"))  # Returns: "Cube"
print(registry.GetConcreteTypeFromSchemaTypeName("Cube")) # Returns: Tf.Type("UsdGeomCube")
# For API schemas:
print(registry.GetAPISchemaTypeName("UsdSkelBindingAPI"))  # Returns: "SkelBindingAPI"
print(registry.GetAPITypeFromSchemaTypeName("SkelBindingAPI")) # Returns: Tf.Type("UsdSkelBindingAPI")
#// ANCHOR_END: schemasRegistry


#// ANCHOR: schemasRegistryToPrimDefinition
from pxr import Usd
registry = Usd.Schema.Registry()
## Useful inspection lookups ##
# Find API schemas. This uses the `Schema Type Name` syntax:
cube_def = registry.FindConcretePrimDefinition("Cube")
print(cube_def.GetPropertyNames())
# Returns:
"""
['doubleSided', 'extent', 'orientation', 'primvars:displayColor', 
 'primvars:displayOpacity', 'purpose', 'size', 'visibility',
 'xformOpOrder', 'proxyPrim']
"""
skel_bind_def = registry.FindAppliedAPIPrimDefinition("SkelBindingAPI")
print(skel_bind_def.GetPropertyNames())
# Returns:
"""
['primvars:skel:geomBindTransform', 'primvars:skel:jointIndices',
 'primvars:skel:jointWeights', 'skel:blendShapes', 'skel:joints', 
 'skel:animationSource', 'skel:blendShapeTargets', 'skel:skeleton']
"""
#// ANCHOR_END: schemasRegistryToPrimDefinition

#// ANCHOR: schemasKind
from pxr import Plug, Sdf, Tf, Usd
### Check schema types ###
registry = Usd.SchemaRegistry()
## Typed Schemas ##
print(registry.IsTyped(UsdGeom.Cube))         # Returns: True
print(registry.IsTyped(UsdGeom.Imageable))    # Returns: True
print(registry.IsAbstract(UsdGeom.Imageable)) # Returns: True
print(registry.IsAbstract(UsdGeom.Cube))      # Returns: False
print(registry.IsConcrete(UsdGeom.Imageable)) # Returns: False
print(registry.IsConcrete(UsdGeom.Cube))      # Returns: True
# Also works with type name strings
print(registry.IsTyped("UsdGeomImageable"))   # Returns: True
print(registry.IsTyped("UsdGeomCube"))        # Returns: True
## API Schemas ##
print(registry.IsAppliedAPISchema("SkelBindingAPI"))      # Returns: True
print(registry.IsMultipleApplyAPISchema("CollectionAPI")) # Returns: True
## We can also ask by schema type name
print(registry.GetSchemaKind("Cube")) # Returns: pxr.Usd.SchemaKind.ConcreteTyped
print(registry.GetSchemaKind("Imageable")) # Returns: pxr.Usd.SchemaKind.AbstractTyped
#// ANCHOR_END: schemasKind


#// ANCHOR: schemasPluginCodelessTest
from pxr import Usd, Sdf
### High Level ###
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/myCoolCustomPrim")
prim = stage.DefinePrim(prim_path, "ComplexPrim")
prim.AddAppliedSchema("ParamsAPI") # Returns: True
# AddAppliedSchema does not check if the schema actually exists, 
# you have to use this for codeless schemas.
### Low Level ###
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/myCoolCustomPrim")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.typeName = "ComplexPrim"
schemas = Sdf.TokenListOp.Create(
    prependedItems=["ParamsAPI"]
)
prim_spec.SetInfo("apiSchemas", schemas)
#// ANCHOR_END: schemasPluginCodelessTest


#// ANCHOR: schemasPluginCompiledTest
from pxr import Usd, Sdf
### High Level ###
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/myCoolCustomPrim")
prim = stage.DefinePrim(prim_path, "ComplexPrim")
prim.AddAppliedSchema("ParamsAPI") # Returns: True
# AddAppliedSchema does not check if the schema actually exists, 
# you have to use this for codeless schemas.
### Low Level ###
from pxr import Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/myCoolCustomPrim")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.typeName = "ComplexPrim"
schemas = Sdf.TokenListOp.Create(
    prependedItems=["ParamsAPI"]
)
prim_spec.SetInfo("apiSchemas", schemas)

### Python Classes ###
stage = Usd.Stage.CreateInMemory()
prim = stage.GetPrimAtPath("/prim")
print(prim.GetTypeName())
print(prim.GetPrimTypeInfo().GetSchemaType().pythonClass)

# Schema Classes
import UsdExampleSchemas as schemas
print(schemas.Complex)
print(schemas.ParamsAPI)
print(schemas.Simple)
print(schemas.Tokens)
# Schema Get/Set/Create methods
schemas.Complex.CreateIntAttrAttr()
#// ANCHOR_END: schemasPluginCompiledTest


#// ANCHOR: propertyOverview
# Methods & Attributes of interest:
# 'IsDefined', 'IsAuthored'
# 'FlattenTo'
# 'GetPropertyStack'
from pxr import Usd, Sdf
### High Level ###
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Cube")
# Check if the attribute defined
attr = prim.CreateAttribute("height", Sdf.ValueTypeNames.Double)
print(attr.IsDefined()) # Returns: True
attr = prim.GetAttribute("someRandomName")
print(attr.IsDefined())
if not attr:
    prim.CreateAttribute("someRandomName", Sdf.ValueTypeNames.String)
# Check if the attribute has any written values in any layer
print(attr.IsAuthored()) # Returns: True
attr.Set("debugString")
# Flatten the attribute to another prim (with optionally a different name)
# This is quite usefull when you need to copy a specific attribute only instead
# of a certain prim.
prim_path = Sdf.Path("/box")
prim = stage.DefinePrim(prim_path, "Cube")
attr.FlattenTo(prim, "someNewName")
# Inspect the property value source layer stack.
# Note the method signature takes a time code as an input. If you supply a default time code
# value clips will be stripped from the result.
time_code = Usd.TimeCode(1001)
print(prim.GetPropertyStack(time_code))
### Low Level ###
# The low level API does not offer any "extras" worthy of noting.
#// ANCHOR_END: propertyOverview

#// ANCHOR: attributeInterpolation
from pxr import Sdf, Usd, UsdGeom
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
attr = prim.CreateAttribute("tire:size", Sdf.ValueTypeNames.Float)
attr.Set(10)
attr.SetMetadata("interpolation", UsdGeom.Tokens.constant)

### Low Level ###
from pxr import Sdf, UsdGeom
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.specifier = Sdf.SpecifierDef
prim_spec.typeName = "Xform"
attr_spec = Sdf.AttributeSpec(prim_spec, "tire:size", Sdf.ValueTypeNames.Double)
attr_spec.default = 10
attr_spec.interpolation = UsdGeom.Tokens.constant
# Or
attr_spec.SetInfo("interpolation", UsdGeom.Tokens.constant)
#// ANCHOR_END: attributeInterpolation

#// ANCHOR: attributeDataTypeRole
from pxr import Gf, Sdf, Usd
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
# When we create attributes, we have to specify the data type/role via a Sdf.ValueTypeName
attr = prim.CreateAttribute("tire:size", Sdf.ValueTypeNames.Float)
# We can then set the attribute to a value of that type.
# Python handles the casting to the correct precision automatically for base data types.
attr.Set(10)
# For attributes the `typeName` metadata specifies the data type/role.
print(attr.GetTypeName()) # Returns: Sdf.ValueTypeNames.Float
# Non-base data types
attr = prim.CreateAttribute("someArray", Sdf.ValueTypeNames.Half3Array)
attr.Set([Gf.Vec3h()]  *3)
attr = prim.CreateAttribute("someAssetPathArray", Sdf.ValueTypeNames.AssetArray)
attr.Set(Sdf.AssetPathArray(["testA.usd", "testB.usd"]))

### Low Level ###
from pxr import Gf, Sdf
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.specifier = Sdf.SpecifierDef
prim_spec.typeName = "Xform"
attr_spec = Sdf.AttributeSpec(prim_spec, "tire:size", Sdf.ValueTypeNames.Double)
# We can then set the attribute to a value of that type.
# Python handles the casting to the correct precision automatically for base data types.
attr_spec.default = 10
# For attributes the `typeName` metadata specifies the data type/role.
print(attr_spec.typeName) # Returns: Sdf.ValueTypeNames.Float
# Non-base data types
attr_spec = Sdf.AttributeSpec(prim_spec, "someArray", Sdf.ValueTypeNames.Half3Array)
attr_spec.default = ([Gf.Vec3h()] * 3)
attr_spec = Sdf.AttributeSpec(prim_spec, "someAssetPathArray", Sdf.ValueTypeNames.AssetArray)
attr_spec.default = Sdf.AssetPathArray(["testA.usd", "testB.usd"])
# Creating an attribute spec with the same data type as an existing attribute (spec)
# is as easy as passing in the type name from the existing attribute (spec)
same_type_attr_spec = Sdf.AttributeSpec(prim_spec, "tire:size", attr.GetTypeName())
# Or
same_type_attr_spec = Sdf.AttributeSpec(prim_spec, "tire:size", attr_spec.typeName)
#// ANCHOR_END: attributeDataTypeRole


#// ANCHOR: animationDefaultTimeSampleBlock
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Cube")
size_attr = prim.GetAttribute("size")
## Set default value
time_code = Usd.TimeCode.Default()
size_attr.Set(10, time_code)
# Or:
size_attr.Set(10) # The default is to set `default` (non-per-frame) data.
## Set per frame value
for frame in range(1001, 1005):
    time_code = Usd.TimeCode(frame)
    size_attr.Set(frame, time_code)
# Or
# As with Sdf.Path implicit casting from strings in a lot of places in the USD API,
# the time code is implicitly casted from a Python float. 
# It is recommended to do the above, to be more future proof of 
# potentially encoding time unit based samples.
for frame in range(1001, 1005):
    size_attr.Set(frame, frame)
## Block the value. This makes the attribute look to USD as if no value was written.
# For attributes from schemas with default values, this will make it fallback to the default value.
height_attr = prim.CreateAttribute("height", Sdf.ValueTypeNames.Float)
height_attr.Set(Sdf.ValueBlock())
#// ANCHOR_END: animationDefaultTimeSampleBlock


#// ANCHOR: attributeReauthor
from pxr import Sdf, Usd
# Spawn reference data
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.specifier = Sdf.SpecifierDef
prim_spec.typeName = "Cube"
attr_spec = Sdf.AttributeSpec(prim_spec, "size", Sdf.ValueTypeNames.Double)
for frame in range(1001, 1010):
    value = float(frame - 1001)
    layer.SetTimeSample(attr_spec.path, frame, value)
# Reference data
stage = Usd.Stage.CreateInMemory()
ref = Sdf.Reference(layer.identifier, "/bicycle")
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path)
ref_api = prim.GetReferences()
ref_api.AddReference(ref)

# Now if we try to read and write the data at the same time,
# we overwrite the (layer composition) value source. In non USD speak:
# We change the layer the data is coming from. Therefore we won't see
# the original data after setting the first time sample.
size_attr = prim.GetAttribute("size")
for time_sample in size_attr.GetTimeSamples():
    size_attr_value = size_attr.Get(time_sample)
    print(time_sample, size_attr_value)
    size_attr.Set(size_attr_value, time_sample)
# Prints:
"""
1001.0 0.0
1002.0 0.0
1003.0 0.0
1004.0 0.0
1005.0 0.0
1006.0 0.0
1007.0 0.0
1008.0 0.0
1009.0 0.0
"""

# Let's undo the previous edit.
prim.RemoveProperty("size") # Removes the local layer attribute spec
# Collect data first ()
data = {}
size_attr = prim.GetAttribute("size")
for time_sample in size_attr.GetTimeSamples():
    size_attr_value = size_attr.Get(time_sample)
    print(time_sample, size_attr_value)
    data[time_sample] = size_attr_value
# Prints:
"""
1001.0 0.0
1002.0 1.0
1003.0 2.0
1004.0 3.0
1005.0 4.0
1006.0 5.0
1007.0 6.0
1008.0 7.0
1009.0 8.0
"""
# Then write it
for time_sample, value in data.items():
    size_attr_value = size_attr.Get(time_sample)
    size_attr.Set(value + 10, time_sample)
#// ANCHOR_END: attributeReauthor


#// ANCHOR: attributeReauthorPerLayer
from pxr import Sdf, Usd
# Spawn example data, this would be a file on disk
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.specifier = Sdf.SpecifierDef
prim_spec.typeName = "Cube"
attr_spec = Sdf.AttributeSpec(prim_spec, "size", Sdf.ValueTypeNames.Double)
for frame in range(1001, 1010):
    value = float(frame - 1001)
    layer.SetTimeSample(attr_spec.path, frame, value)

# Edit content
layer_identifiers = [layer.identifier]
for layer_identifier in layer_identifiers:
    prim_path = Sdf.Path("/bicycle")
    ### High Level ###
    stage = Usd.Stage.Open(layer_identifier)
    prim = stage.GetPrimAtPath(prim_path)
    size_attr = prim.GetAttribute("size")
    for frame in size_attr.GetTimeSamples():
        size_attr_value = size_attr.Get(frame)
        # .Set() takes args in the .Set(<value>, <frame>) format
        size_attr.Set(size_attr_value + 125, frame)
    ### Low Level ###
    # Note that this edits the same layer as the stage above.
    layer = Sdf.Layer.FindOrOpen(layer_identifier)
    prim_spec = layer.GetPrimAtPath(prim_path)
    attr_spec = prim_spec.attributes["size"]
    for frame in layer.ListTimeSamplesForPath(attr_spec.path):
        value = layer.QueryTimeSample(attr_spec.path, frame)
        layer.SetTimeSample(attr_spec.path, frame, value + 125)
#// ANCHOR_END: attributeReauthorPerLayer


#// ANCHOR: attributeReauthorTimeSampleToStatic
from pxr import Sdf, Usd
# Spawn example data, this would be a file on disk
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.specifier = Sdf.SpecifierDef
prim_spec.typeName = "Cube"
attr_spec = Sdf.AttributeSpec(prim_spec, "size", Sdf.ValueTypeNames.Double)
for frame in range(1001, 1010):
    value = float(frame - 1001)
    layer.SetTimeSample(attr_spec.path, frame, value)
# Reference data
stage = Usd.Stage.CreateInMemory()
ref = Sdf.Reference(layer.identifier, "/bicycle")
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path)
ref_api = prim.GetReferences()
ref_api.AddReference(ref)

# Freeze content
freeze_frame = 1001
attrs = []
for prim in stage.Traverse():
    ### High Level ###
    for attr in prim.GetAuthoredAttributes():      
        # attr.Set(attr.Get(freeze_frame))
        ### Low Level ###
        attrs.append(attr)

### Low Level ###
active_layer = stage.GetEditTarget().GetLayer()
with Sdf.ChangeBlock():
    for attr in attrs:
        attr_spec =  active_layer.GetAttributeAtPath(attr.GetPath())
        if not attr_spec:
            prim_path = attr.GetPrim().GetPath()
            prim_spec = active_layer.GetPrimAtPath(prim_path)
            if not prim_spec:
                prim_spec = Sdf.CreatePrimInLayer(active_layer, prim_path)
            attr_spec = Sdf.AttributeSpec(prim_spec, attr.GetName(),attr.GetTypeName())
        attr_spec.default = attr.Get(freeze_frame)
#// ANCHOR_END: attributeReauthorTimeSampleToStatic


#// ANCHOR: attributePrimvarAPI
## UsdGeom.PrimvarsAPI(prim)
# Has: 'HasPrimvar',
# Get: 'GetAuthoredPrimvars', 'GetPrimvar',
#      'GetPrimvars', 'GetPrimvarsWithAuthoredValues', 'GetPrimvarsWithValues', 
# Set: 'CreatePrimvar', 'CreateIndexedPrimvar', 'CreateNonIndexedPrimvar', 
# Clear: 'RemovePrimvar', 'BlockPrimvar',
## UsdGeom.Primvar(attribute)
# This is the same as Usd.Attribute, but exposes extra
# primvar related methods, mainly:
# Has/Is: 'IsIndexed', 'IsPrimvar'
# Get: 'GetPrimvarName', 'GetIndicesAttr', 'GetIndices'
# Set: 'CreateIndicesAttr', 'ComputeFlattened'
# Remove: 'BlockIndices'
from pxr import Sdf, Usd, UsdGeom, Vt
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Cube")
size_attr = prim.GetAttribute("size")
# Manually define primvar
attr = prim.CreateAttribute("width", Sdf.ValueTypeNames.Float)
print(UsdGeom.Primvar.IsPrimvar(attr)) # Returns: False
attr = prim.CreateAttribute("primvars:depth", Sdf.ValueTypeNames.Float)
print(UsdGeom.Primvar.IsPrimvar(attr)) # Returns: True
# Use primvar API
# This returns an instance of UsdGeom.Primvar
primvar_api = UsdGeom.PrimvarsAPI(prim)
primvar = primvar_api.CreatePrimvar("height", Sdf.ValueTypeNames.StringArray)
print(UsdGeom.Primvar.IsPrimvar(primvar))  # Returns: False
print(primvar.GetPrimvarName()) # Returns: "height"
primvar.Set(["testA", "testB"])
print(primvar.ComputeFlattened()) # Returns: ["testA", "testB"]
# In this case flattening does nothing, because it is not indexed.
# This will fail as it is expected to create indices on primvar creation.
primvar_indices = primvar.CreateIndicesAttr()
# So let's do that
values = ["testA", "testB"]
primvar = primvar_api.CreateIndexedPrimvar("height",
                                           Sdf.ValueTypeNames.StringArray,
                                           Vt.StringArray(values),
                                           Vt.IntArray([0,0,0, 1,1, 0]),
                                           UsdGeom.Tokens.constant, 
                                           time=1001)
print(primvar.GetName(), primvar.GetIndicesAttr().GetName(), primvar.IsIndexed())
# Returns: primvars:height primvars:height:indices True
print(primvar.ComputeFlattened())
# Returns:
# ["testA", "testA", "testA", "testB", "testB", "testA"]
#// ANCHOR_END: attributePrimvarAPI


#// ANCHOR: attributePrimvarInherited
## UsdGeom.PrimvarsAPI(prim)
# To detect inherited primvars, the primvars API offers helper methods:
# 'HasPossiblyInheritedPrimvar', 
# 'FindIncrementallyInheritablePrimvars', 
# 'FindInheritablePrimvars', 
# 'FindPrimvarWithInheritance', 
# 'FindPrimvarsWithInheritance',

from pxr import Sdf, Usd, UsdGeom
stage = Usd.Stage.CreateInMemory()
bicycle_prim = stage.DefinePrim(Sdf.Path("/set/garage/bicycle"), "Cube")
car_prim = stage.DefinePrim(Sdf.Path("/set/garage/car"), "Cube")
set_prim = stage.GetPrimAtPath("/set")
garage_prim = stage.GetPrimAtPath("/set/garage")
tractor_prim = stage.DefinePrim(Sdf.Path("/set/yard/tractor"), "Cube")

# Setup hierarchy primvars
primvar_api = UsdGeom.PrimvarsAPI(set_prim)
size_primvar = primvar_api.CreatePrimvar("size", Sdf.ValueTypeNames.Float)
size_primvar.Set(10)
primvar_api = UsdGeom.PrimvarsAPI(garage_prim)
size_primvar = primvar_api.CreatePrimvar("size", Sdf.ValueTypeNames.Float)
size_primvar.Set(5)
size_primvar = primvar_api.CreatePrimvar("point_scale", Sdf.ValueTypeNames.Float)
size_primvar.Set(9000)
primvar_api = UsdGeom.PrimvarsAPI(bicycle_prim)
size_primvar = primvar_api.CreatePrimvar("size", Sdf.ValueTypeNames.Float)
size_primvar.Set(2.5)

# Get (non-inherited) primvars on prim
primvar_api = UsdGeom.PrimvarsAPI(bicycle_prim)
print([p.GetAttr().GetPath() for p in primvar_api.GetPrimvars()])
# Returns:
# [Sdf.Path('/set/garage/bicycle.primvars:displayColor'),
#  Sdf.Path('/set/garage/bicycle.primvars:displayOpacity'),
#  Sdf.Path('/set/garage/bicycle.primvars:size')]
# Check for inherited primvar on prim
primvar_api = UsdGeom.PrimvarsAPI(bicycle_prim)
print(primvar_api.FindPrimvarWithInheritance("test").IsDefined())
# Returns: False

# Get inherited primvar
# This is expensive to compute, as prim prim where you call this,
# the ancestors have to be checked.
primvar_api = UsdGeom.PrimvarsAPI(bicycle_prim)
print([p.GetAttr().GetPath() for p in primvar_api.FindInheritablePrimvars()])
# Returns: [Sdf.Path('/set/garage/bicycle.primvars:size'), Sdf.Path('/set/garage.primvars:point_scale')]

# Instead we should populate our own stack:
# This is fast to compute!
print("----")
primvars_current = []
for prim in stage.Traverse():
    primvar_api = UsdGeom.PrimvarsAPI(prim)
    primvars_current = primvar_api.FindIncrementallyInheritablePrimvars(primvars_current)
    print(prim.GetPath(), [p.GetAttr().GetPath().pathString for p in primvars_current])
# Returns:
"""
/set ['/set.primvars:size']
/set/garage ['/set/garage.primvars:size', '/set/garage.primvars:point_scale']
/set/garage/bicycle ['/set/garage/bicycle.primvars:size', '/set/garage.primvars:point_scale']
/set/garage/car []
/set/yard []
/set/yard/traktor []
"""
print("----")
# This is wrong if you might have noticed!
# We should be seeing our '/set.primvars:size' primvar on the yard prims to!
# If we look at the docs, we see the intended use: 
# FindIncrementallyInheritablePrimvars returns a new list if it gets re-populated.
# So the solution is to track the lists with pre/post visits.
primvar_stack = [[]]
iterator = iter(Usd.PrimRange.PreAndPostVisit(stage.GetPseudoRoot()))
for prim in iterator:
    primvar_api = UsdGeom.PrimvarsAPI(prim)
    if not iterator.IsPostVisit():
        before = hex(id(primvar_stack[-1]))
        primvars_iter = primvar_api.FindIncrementallyInheritablePrimvars(primvar_stack[-1])
        primvar_stack.append(primvars_iter)
        print(before, hex(id(primvars_iter)), prim.GetPath(), [p.GetAttr().GetPath().pathString for p in primvars_iter], len(primvar_stack))
    else:
        primvar_stack.pop(-1)
# This also doesn't work as it seems to clear the memory address for some reason (Or do I have a logic error?)
# Let's write it ourselves:
primvar_stack = [{}]
iterator = iter(Usd.PrimRange.PreAndPostVisit(stage.GetPseudoRoot()))
for prim in iterator:
    primvar_api = UsdGeom.PrimvarsAPI(prim)
    if not iterator.IsPostVisit():
        before_hash = hex(id(primvar_stack[-1]))
        parent_primvars = primvar_stack[-1]
        authored_primvars = {p.GetPrimvarName(): p for p in primvar_api.GetPrimvarsWithAuthoredValues()} 
        if authored_primvars and parent_primvars:
            combined_primvars = {name: p for name, p in parent_primvars.items()}
            combined_primvars.update(authored_primvars)
            primvar_stack.append(combined_primvars)
        elif authored_primvars:
            primvar_stack.append(authored_primvars)
        else:
            primvar_stack.append(parent_primvars)
        after_hash = hex(id(primvar_stack[-1]))
        print(before_hash, after_hash, prim.GetPath(), [p.GetAttr().GetPath().pathString for p in primvar_stack[-1].values()], len(primvar_stack))
    else:
        primvar_stack.pop(-1)
# Returns:
""" This works :)
0x7fea12b349c0 0x7fea12b349c0 / [] 2
0x7fea12b349c0 0x7fea12b349c0 /HoudiniLayerInfo [] 3
0x7fea12b349c0 0x7fea12bfe980 /set ['/set.primvars:size'] 3
0x7fea12bfe980 0x7fea12a89600 /set/garage ['/set/garage.primvars:size', '/set/garage.primvars:point_scale'] 4
0x7fea12a89600 0x7fea367b87c0 /set/garage/bicycle ['/set/garage/bicycle.primvars:size', '/set/garage.primvars:point_scale'] 5
0x7fea12a89600 0x7fea12a89600 /set/garage/car ['/set/garage.primvars:size', '/set/garage.primvars:point_scale'] 5
0x7fea12bfe980 0x7fea12bfe980 /set/yard ['/set.primvars:size'] 4
0x7fea12bfe980 0x7fea12bfe980 /set/yard/tractor ['/set.primvars:size'] 5
"""
#// ANCHOR_END: attributePrimvarInherited


#// ANCHOR: attributePrimvarIndexed
from pxr import Sdf, Usd, UsdGeom, Vt
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Cube")
# So let's do that
value_set = ["testA", "testB"]
value_indices = [0,0,0, 1,1, 0]
primvar = primvar_api.CreateIndexedPrimvar("height",
                                           Sdf.ValueTypeNames.StringArray,
                                           Vt.StringArray(value_set),
                                           Vt.IntArray(value_indices),
                                           UsdGeom.Tokens.constant, 
                                           time=1001)
print(primvar.ComputeFlattened())
# Returns:
# ["testA", "testA", "testA", "testB", "testB", "testA"]
#// ANCHOR_END: attributePrimvarIndexed


#// ANCHOR: attributeConnections
from pxr import Sdf, Usd
### High Level ###
# Has: 'HasAuthoredConnections', 
# Get: 'GetConnections',
# Set: 'AddConnection', 'SetConnections'
# Clear:  'RemoveConnection', 'ClearConnections'
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/box")
prim = stage.DefinePrim(prim_path, "Cube")
width_attr = prim.CreateAttribute("width", Sdf.ValueTypeNames.Double)
height_attr = prim.CreateAttribute("height", Sdf.ValueTypeNames.Double)
depth_attr = prim.CreateAttribute("depth", Sdf.ValueTypeNames.Double)
width_attr.AddConnection(height_attr.GetPath(), Usd.ListPositionBackOfAppendList)
width_attr.AddConnection(depth_attr.GetPath(), Usd.ListPositionFrontOfAppendList)
print(width_attr.GetConnections())
# Returns: [Sdf.Path('/box.depth'), Sdf.Path('/box.height')]
width_attr.RemoveConnection(depth_attr.GetPath())
print(width_attr.GetConnections())
# Returns: [Sdf.Path('/box.height')]
### Low Level ###
# Connections are managed via the `connectionPathList` AttributeSpec attribute.
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/box")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.typeName = "Cube"
width_attr_spec = Sdf.AttributeSpec(prim_spec, "width", Sdf.ValueTypeNames.Double)
height_attr_spec = Sdf.AttributeSpec(prim_spec, "height", Sdf.ValueTypeNames.Double)
depth_attr_spec = Sdf.AttributeSpec(prim_spec, "depth", Sdf.ValueTypeNames.Double)
width_attr_spec.connectionPathList.Append(height_attr_spec.path)
width_attr_spec.connectionPathList.Append(depth_attr_spec.path)
print(width_attr_spec.connectionPathList.GetAddedOrExplicitItems())
# Returns: (Sdf.Path('/box.height'), Sdf.Path('/box.depth'))
width_attr_spec.connectionPathList.Erase(depth_attr_spec.path)
print(width_attr_spec.connectionPathList.GetAddedOrExplicitItems())
# Returns: (Sdf.Path('/box.height'),)
## This won't work as the connectionPathList attribute can only be edited in place
path_list = Sdf.PathListOp.Create(appendedItems=[height_attr_spec.path])
# width_attr_spec.connectionPathList = path_list
#// ANCHOR_END: attributeConnections


#// ANCHOR: attributePurpose
### High Level ###
from pxr import Sdf, Usd, UsdGeom
stage = Usd.Stage.CreateInMemory()
cube_prim = stage.DefinePrim(Sdf.Path("/bicycle/RENDER/cube"), "Cube")
render_prim = cube_prim.GetParent()
render_prim.SetTypeName("Xform")
UsdGeom.Imageable(render_prim).GetPurposeAttr().Set(UsdGeom.Tokens.render)
sphere_prim = stage.DefinePrim(Sdf.Path("/bicycle/PROXY/sphere"), "Sphere")
proxy_prim = sphere_prim.GetParent()
proxy_prim.SetTypeName("Xform")
UsdGeom.Imageable(proxy_prim).GetPurposeAttr().Set(UsdGeom.Tokens.proxy)
# We can also query the inherited purpose:
imageable_api = UsdGeom.Imageable(cube_prim)
print(imageable_api.ComputePurpose()) # Returns: 'render'

### Low Level ###
from pxr import Sdf, UsdGeom
layer = Sdf.Layer.CreateAnonymous()
prim_path = Sdf.Path("/bicycle")
prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
prim_spec.specifier = Sdf.SpecifierDef
prim_spec.typeName = "Cube"
attr_spec = Sdf.AttributeSpec(prim_spec, "purpose", Sdf.ValueTypeNames.Token)
attr_spec.default = UsdGeom.Tokens.render
#// ANCHOR_END: attributePurpose

#// ANCHOR: attributeVisibility
### High Level ###
# UsdGeom.Imageable()
# Get: 'ComputeVisibility'
# Set: 'MakeVisible', 'MakeInvisible'
from pxr import Sdf, Usd, UsdGeom
stage = Usd.Stage.CreateInMemory()
cube_prim = stage.DefinePrim(Sdf.Path("/set/yard/bicycle"), "Cube")
sphere_prim = stage.DefinePrim(Sdf.Path("/set/garage/bicycle"), "Sphere")
set_prim = cube_prim.GetParent().GetParent()
set_prim.SetTypeName("Xform")
cube_prim.GetParent().SetTypeName("Xform")
sphere_prim.GetParent().SetTypeName("Xform")
UsdGeom.Imageable(set_prim).GetVisibilityAttr().Set(UsdGeom.Tokens.invisible)
# We can also query the inherited visibility:
# ComputeEffectiveVisibility -> This handles per purpose visibility
imageable_api = UsdGeom.Imageable(cube_prim)
print(imageable_api.ComputeVisibility()) # Returns: 'invisible'
# Make only the cube visible. Notice how this automatically sparsely
# selects only the needed parent prims (garage) and makes them invisible.
# How cool is that!
imageable_api.MakeVisible()

### Low Level ###
from pxr import Sdf, UsdGeom
layer = Sdf.Layer.CreateAnonymous()
bicycle_prim_path = Sdf.Path("/set/bicycle")
bicycle_prim_spec = Sdf.CreatePrimInLayer(layer, prim_path)
bicycle_prim_spec.specifier = Sdf.SpecifierDef
bicycle_prim_spec.typeName = "Cube"
bicycle_vis_attr_spec = Sdf.AttributeSpec(prim_spec, "visibility", Sdf.ValueTypeNames.Token)
bicycle_vis_attr_spec.default = UsdGeom.Tokens.inherited
#// ANCHOR_END: attributeVisibility


#// ANCHOR: attributeExtent
### High Level ###
# UsdGeom.Boundable()
# Get: 'GetExtentAttr', 'CreateExtentAttr'
# Set: 'ComputeExtent '
from pxr import Sdf, Usd, UsdGeom
stage = Usd.Stage.CreateInMemory()
cube_prim = stage.DefinePrim(Sdf.Path("/bicycle/cube"), "Cube")
bicycle_prim = cube_prim.GetParent()
bicycle_prim.SetTypeName("Xform")
# If we change the size, we have to re-compute the bounds
cube_prim.GetAttribute("size").Set(10)
boundable_api = UsdGeom.Boundable(cube_prim)
print(boundable_api.GetExtentAttr().Get()) # Returns:  [(-1, -1, -1), (1, 1, 1)]
extent = boundable_api.ComputeExtent(Usd.TimeCode.Default())
boundable_api.GetExtentAttr().Set(extent)
print(boundable_api.GetExtentAttr().Get()) # Returns: [(-5, -5, -5), (5, 5, 5)]
# Author extentsHint
# The bbox cache has to be specified with what frame and purpose to query
bbox_cache = UsdGeom.BBoxCache(1001, [UsdGeom.Tokens.default_, UsdGeom.Tokens.render])
model_api = UsdGeom.ModelAPI(bicycle_prim)
extentsHint = model_api.ComputeExtentsHint(bbox_cache)
model_api.SetExtentsHint(extentsHint)
# Or model_api.SetExtentsHint(extentsHint, <frame>)
### Low Level ###
from pxr import Sdf, UsdGeom, Vt
layer = Sdf.Layer.CreateAnonymous()
cube_prim_path = Sdf.Path("/bicycle/cube")
cube_prim_spec = Sdf.CreatePrimInLayer(layer, cube_prim_path)
cube_prim_spec.specifier = Sdf.SpecifierDef
cube_prim_spec.typeName = "Cube"
bicycle_prim_path = Sdf.Path("/bicycle")
bicycle_prim_spec = Sdf.CreatePrimInLayer(layer, cube_prim_path)
bicycle_prim_spec.specifier = Sdf.SpecifierDef
bicycle_prim_spec.typeName = "Xform"
# The querying should be done via the high level API.
extent_attr_spec = Sdf.AttributeSpec(cube_prim_spec, "extent", Sdf.ValueTypeNames.Vector3fArray)
extent_attr_spec.default = Vt.Vec3fArray([(-1, -1, -1), (1, 1, 1)])
site_attr_spec = Sdf.AttributeSpec(cube_prim_spec, "size", Sdf.ValueTypeNames.Float)
site_attr_spec.default = 10
extent_attr_spec.default = Vt.Vec3fArray([(-5, -5, -5), (5, 5, 5)])
# Author extentsHint
extents_hint_attr_spec = Sdf.AttributeSpec(bicycle_prim_spec, "extentsHint", Sdf.ValueTypeNames.Vector3fArray)
extents_hint_attr_spec.default = Vt.Vec3fArray([(-5, -5, -5), (5, 5, 5)])
#// ANCHOR_END: attributeExtent


#// ANCHOR: relationshipMaterialBinding
## UsdShade.MaterialBindingAPI(<boundable prim>)
# This handles all the binding get and setting
## These classes can inspect an existing binding
# UsdShade.MaterialBindingAPI.DirectBinding()
# UsdShade.MaterialBindingAPI.CollectionBinding()
### High Level ###
from pxr import Sdf, Usd, UsdGeom, UsdShade
stage = Usd.Stage.CreateInMemory()
render_prim = stage.DefinePrim(Sdf.Path("/bicycle/RENDER/render"), "Cube")
material_prim = stage.DefinePrim(Sdf.Path("/bicycle/MATERIALS/example_material"), "Material")
bicycle_prim = render_prim.GetParent().GetParent()
bicycle_prim.SetTypeName("Xform")
render_prim.GetParent().SetTypeName("Xform")
material_prim.GetParent().SetTypeName("Xform")
# Bind materials via direct binding
material = UsdShade.Material(material_prim)
mat_bind_api = UsdShade.MaterialBindingAPI(render_prim)
# Unbind all
mat_bind_api.UnbindAllBindings()
# Bind via collection
collection_name = "material_example"
collection_api = Usd.CollectionAPI.Apply(bicycle_prim, collection_name)
collection_api.GetIncludesRel().AddTarget(material_prim.GetPath())
collection_api.GetExpansionRuleAttr().Set(Usd.Tokens.expandPrims)
mat_bind_api.Bind(collection_api, material, "material_example")

### Low Level ###
from pxr import Sdf, UsdGeom
layer = Sdf.Layer.CreateAnonymous()
render_prim_spec = Sdf.CreatePrimInLayer(layer, Sdf.Path("/render"))
render_prim_spec.specifier = Sdf.SpecifierDef
render_prim_spec.typeName = "Cube"
material_prim_spec = Sdf.CreatePrimInLayer(layer, Sdf.Path("/material"))
material_prim_spec.specifier = Sdf.SpecifierDef
material_prim_spec.typeName = "Material"
## Direct binding
material_bind_rel_spec = Sdf.RelationshipSpec(render_prim_spec, "material:binding")
material_bind_rel_spec.targetPathList.Append(Sdf.Path("/render"))
# Applied Schemas
schemas = Sdf.TokenListOp.Create(
    prependedItems=["MaterialBindingAPI"]
)
render_prim_spec.SetInfo("apiSchemas", schemas)
#// ANCHOR_END: relationshipMaterialBinding

#// ANCHOR: collectionOverview
# Usd.CollectionAPI.Apply(prim, collection_name)
# collection_api = Usd.CollectionAPI(prim, collection_nam)
# collection_query = collection_api.ComputeMembershipQuery()
### High Level ###
from pxr import Sdf, Usd, UsdUtils
stage = Usd.Stage.CreateInMemory()
bicycle_prim = stage.DefinePrim(Sdf.Path("/set/yard/biycle"), "Cube")
car_prim = stage.DefinePrim(Sdf.Path("/set/garage/car"), "Sphere")
tractor_prim = stage.DefinePrim(Sdf.Path("/set/garage/tractor"), "Cylinder")
helicopter_prim = stage.DefinePrim(Sdf.Path("/set/garage/helicopter"), "Cube")
boat_prim = stage.DefinePrim(Sdf.Path("/set/garage/boat"), "Cube")
set_prim = bicycle_prim.GetParent().GetParent()
set_prim.SetTypeName("Xform")
bicycle_prim.GetParent().SetTypeName("Xform")
car_prim.GetParent().SetTypeName("Xform")
# Create collection
collection_name = "vehicles"
collection_api = Usd.CollectionAPI.Apply(set_prim, collection_name)
collection_api.GetIncludesRel().AddTarget(set_prim.GetPath())
collection_api.GetExcludesRel().AddTarget(bicycle_prim.GetPath())
collection_api.GetExpansionRuleAttr().Set(Usd.Tokens.expandPrims)
print(Usd.CollectionAPI.GetAllCollections(set_prim)) # Returns: [Usd.CollectionAPI(Usd.Prim(</set>), 'vehicles')]
print(Usd.CollectionAPI.GetCollection(set_prim, "vehicles")) # Returns: Usd.CollectionAPI(Usd.Prim(</set>), 'vehicles')
collection_query = collection_api.ComputeMembershipQuery()
print(collection_api.ComputeIncludedPaths(collection_query, stage))
# Returns: [Sdf.Path('/set'), Sdf.Path('/set/garage'), Sdf.Path('/set/garage/car'), Sdf.Path('/set/yard')]
# Set it to explicit only
collection_api.GetExpansionRuleAttr().Set(Usd.Tokens.explicitOnly)
collection_query = collection_api.ComputeMembershipQuery()
print(collection_api.ComputeIncludedPaths(collection_query, stage))
# Returns: [Sdf.Path('/set')]

# To help speed up collection creation, USD also ships with util functions:
# UsdUtils.AuthorCollection(<collectionName>, prim, [<includePathList>], [<excludePathList>])
collection_api = UsdUtils.AuthorCollection("two_wheels", set_prim, [set_prim.GetPath()], [car_prim.GetPath()])
collection_query = collection_api.ComputeMembershipQuery()
print(collection_api.ComputeIncludedPaths(collection_query, stage))
# Returns:
# [Sdf.Path('/set'), Sdf.Path('/set/garage'), Sdf.Path('/set/yard'), Sdf.Path('/set/yard/biycle')]
# UsdUtils.ComputeCollectionIncludesAndExcludes() gives us the possibility to author 
# collections more sparse, that the include to exclude ratio is kept at an optimal size.
# The Python signature differs from the C++ signature:
"""
include_paths, exclude_paths = UsdUtils.ComputeCollectionIncludesAndExcludes(
    target_paths,
    stage,
    minInclusionRatio = 0.75,
    maxNumExcludesBelowInclude = 5,
	minIncludeExcludeCollectionSize = 3,
    pathsToIgnore = [] # This ignores paths from computation (this is not the exclude list)
)		
"""
target_paths = [tractor_prim.GetPath(), car_prim.GetPath(), helicopter_prim.GetPrimPath()]
include_paths, exclude_paths = UsdUtils.ComputeCollectionIncludesAndExcludes(target_paths,stage, minInclusionRatio=.9)
print(include_paths, exclude_paths)
# Returns:
# [Sdf.Path('/set/garage/car'), Sdf.Path('/set/garage/tractor'), Sdf.Path('/set/garage/helicopter')] []
include_paths, exclude_paths = UsdUtils.ComputeCollectionIncludesAndExcludes(target_paths,stage, minInclusionRatio=.1)
print(include_paths, exclude_paths)
# Returns: [Sdf.Path('/set/garage')] [Sdf.Path('/set/garage/boat')]
# Create a collection from the result
collection_api = UsdUtils.AuthorCollection("optimized", set_prim, include_paths, exclude_paths)
#// ANCHOR_END: collectionOverview

#// ANCHOR: relationshipOverview
### High Level ###
# Get: 'GetForwardedTargets', 'GetTargets',
# Set: 'AddTarget', 'SetTargets'
# Clear: 'RemoveTarget', 'ClearTargets'
from pxr import Sdf, Usd, UsdGeom
stage = Usd.Stage.CreateInMemory()
cube_prim = stage.DefinePrim(Sdf.Path("/cube_prim"), "Cube")
sphere_prim = stage.DefinePrim(Sdf.Path("/sphere_prim"), "Sphere")
myFavoriteSphere_rel = cube_prim.CreateRelationship("myFavoriteSphere")
myFavoriteSphere_rel.AddTarget(sphere_prim.GetPath())
print(myFavoriteSphere_rel.GetForwardedTargets()) # Returns:[Sdf.Path('/sphere_prim')]
# myFavoriteSphere_rel.ClearTargets()
# We can also forward relationships to other relationships.
cylinder_prim = stage.DefinePrim(Sdf.Path("/sphere_prim"), "Cylinder")
myFavoriteSphereForward_rel = cylinder_prim.CreateRelationship("myFavoriteSphereForward")
myFavoriteSphereForward_rel.AddTarget(myFavoriteSphere_rel.GetPath())
# GetForwardedTargets: This gives us the final fowarded paths. We'll use this most of the time.
# GetTargets: Gives us the paths set on the relationship, forwarded paths are not baked down.
print(myFavoriteSphereForward_rel.GetForwardedTargets()) # Returns:[Sdf.Path('/sphere_prim')]
print(myFavoriteSphereForward_rel.GetTargets()) # Returns: [Sdf.Path('/cube_prim.myFavoriteSphere')]

### Low Level ###
from pxr import Sdf, UsdGeom
layer = Sdf.Layer.CreateAnonymous()
cube_prim_spec = Sdf.CreatePrimInLayer(layer, Sdf.Path("/cube_prim"))
cube_prim_spec.specifier = Sdf.SpecifierDef
cube_prim_spec.typeName = "Cube"
sphere_prim_spec = Sdf.CreatePrimInLayer(layer, Sdf.Path("/sphere_prim"))
sphere_prim_spec.specifier = Sdf.SpecifierDef
sphere_prim_spec.typeName = "Cube"
rel_spec = Sdf.RelationshipSpec(cube_prim_spec, "proxyPrim")
rel_spec.targetPathList.Append(sphere_prim_spec.path)
# The targetPathList is a list editable Sdf.PathListOp.
# Forwarded rels can only be calculated via the high level API.
#// ANCHOR_END: relationshipOverview


#// ANCHOR: relationshipProxyPrim
### High Level ###
from pxr import Sdf, Usd, UsdGeom
stage = Usd.Stage.CreateInMemory()
render_prim = stage.DefinePrim(Sdf.Path("/bicycle/RENDER/render"), "Cube")
proxy_prim = stage.DefinePrim(Sdf.Path("/bicycle/PROXY/proxy"), "Sphere")
bicycle_prim = render_prim.GetParent().GetParent()
bicycle_prim.SetTypeName("Xform")
render_prim.GetParent().SetTypeName("Xform")
proxy_prim.GetParent().SetTypeName("Xform")
imageable_api = UsdGeom.Imageable(render_prim)
imageable_api.SetProxyPrim(proxy_prim)
# Query the proxy prim
print(imageable_api.ComputeProxyPrim()) # Returns: None
# Why does this not work? We have to set the purpose!
UsdGeom.Imageable(render_prim).GetPurposeAttr().Set(UsdGeom.Tokens.render)
UsdGeom.Imageable(proxy_prim).GetPurposeAttr().Set(UsdGeom.Tokens.proxy)
print(imageable_api.ComputeProxyPrim()) # Returns: (Usd.Prim(</bicycle/PROXY/proxy>), Usd.Prim(</bicycle/RENDER/render>))

### Low Level ###
from pxr import Sdf, UsdGeom
layer = Sdf.Layer.CreateAnonymous()
render_prim_spec = Sdf.CreatePrimInLayer(layer, Sdf.Path("/render"))
render_prim_spec.specifier = Sdf.SpecifierDef
render_prim_spec.typeName = "Cube"
proxy_prim_spec = Sdf.CreatePrimInLayer(layer, Sdf.Path("/proxy"))
proxy_prim_spec.specifier = Sdf.SpecifierDef
proxy_prim_spec.typeName = "Cube"
proxyPrim_rel_spec = Sdf.RelationshipSpec(render_prim_spec, "proxyPrim")
proxyPrim_rel_spec.targetPathList.Append(Sdf.Path("/proxy"))
#// ANCHOR_END: relationshipProxyPrim


#// ANCHOR: collectionInvert
from pxr import Sdf, Usd, UsdUtils
stage = Usd.Stage.CreateInMemory()
# Create hierarchy
prim_paths = [
    "/set/yard/biycle",
    "/set/yard/shed/shovel",
    "/set/yard/shed/flower_pot",
    "/set/yard/shed/lawnmower",
    "/set/yard/shed/soil",
    "/set/yard/shed/wood",
    "/set/garage/car",
    "/set/garage/tractor",
    "/set/garage/helicopter",
    "/set/garage/boat",
    "/set/garage/key_box",
    "/set/garage/key_box/red",
    "/set/garage/key_box/blue",
    "/set/garage/key_box/green",
    "/set/people/mike",
    "/set/people/charolotte"
]
for prim_path in prim_paths:
    prim = stage.DefinePrim(prim_path, "Cube")
print("<< hierarchy >>")
for prim in stage.Traverse():
    print(prim.GetPath())
    parent_prim = prim.GetParent()
    while True:
        if parent_prim.IsPseudoRoot():
            break
        parent_prim.SetTypeName("Xform")
        parent_prim = parent_prim.GetParent()
# Returns:
"""
<< hierarchy >>
/HoudiniLayerInfo
/set
/set/yard
/set/yard/biycle
/set/yard/shed
/set/yard/shed/shovel
/set/yard/shed/flower_pot
/set/yard/shed/lawnmower
/set/yard/shed/soil
/set/yard/shed/wood
/set/garage
/set/garage/car
/set/garage/tractor
/set/garage/helicopter
/set/garage/boat
/set/garage/key_box
/set/garage/key_box/red
/set/garage/key_box/blue
/set/garage/key_box/green
/set/people
/set/people/mike
/set/people/charolotte
"""
# Collections
collection_prim = stage.DefinePrim("/collections")
storage_include_prim_paths = ["/set/garage/key_box", "/set/yard/shed"]
storage_exclude_prim_paths = ["/set/yard/shed/flower_pot"]
collection_api = UsdUtils.AuthorCollection("storage", collection_prim, storage_include_prim_paths, storage_exclude_prim_paths)
collection_query = collection_api.ComputeMembershipQuery()
included_paths = collection_api.ComputeIncludedPaths(collection_query, stage)
# print(included_paths)
# Prune inverse:
print("<< hierarchy pruned >>")
iterator = iter(Usd.PrimRange(stage.GetPseudoRoot()))
for prim in iterator:
    if prim.IsPseudoRoot():
        continue
    if prim.GetPath() not in included_paths and not len(prim.GetAllChildrenNames()):
        iterator.PruneChildren()
        prim.SetActive(False)
    else:    
        print(prim.GetPath())
# Returns:
"""
<< hierarchy pruned >>
/set
/set/yard
/set/yard/shed
/set/yard/shed/shovel
/set/yard/shed/lawnmower
/set/yard/shed/soil
/set/yard/shed/wood
/set/garage
/set/garage/key_box
/set/garage/key_box/red
/set/garage/key_box/blue
/set/garage/key_box/green
/set/people
"""
#// ANCHOR_END: collectionInvert


#// ANCHOR: dataTypeRoleOverview
from pxr import Sdf, Vt
##### Value Type Names - pxr.Sdf.ValueTypeNames #####
### Looking at TexCoord2fArray as an example
value_type_name = Sdf.ValueTypeNames.TexCoord2fArray
print("Value Type Name", value_type_name) # Returns: Sdf.ValueTypeName("texCoord2f[]")
## Aliases and cpp names
print("Value Type Name Alias", value_type_name.aliasesAsStrings)    # ['texCoord2f[]']
print("Value Type Name Cpp Type Name", value_type_name.cppTypeName) # 'VtArray<GfVec2f>'
print("Value Type Name Role", value_type_name.role)                 # Returns: 'TextureCoordinate'
## Array vs Scalar (Single Value)
print("Value Type Name IsArray", value_type_name.isArray)          # Returns: True
print("Value Type Name IsArray", value_type_name.isScalar)         # Returns: False
## Convert type between Scalar <-> Array
print("Value Type Name -> Get Array Type", value_type_name.arrayType)   # Returns: Sdf.ValueTypeName("texCoord2f[]") (Same as type_name in this case)
print("Value Type Name -> Get Scalar Type", value_type_name.scalarType) # Returns: Sdf.ValueTypeName("texCoord2f")
### Type (Actual type definiton, holds data about container format
### like C++ type name and the Python class
value_type = value_type_name.type
print(value_type) # Returns: Tf.Type.FindByName('VtArray<GfVec2f>')
### Get the Python Class
cls = value_type.pythonClass
# Or (for base types like float, int)
default_value = value_type_name.defaultValue
cls = default_value.__class__
instance = cls()

##### Types - pxr.Vt.Type Registry #####
from pxr import Vt
# For Python usage, the only thing of interest for data types in the Vt.Type module are the `*Array`ending classes.`
# You will only use these array types to handle the auto conversion
# form buffer protocol arrays like numpy arrays, the rest is auto converted and you don't need
# to worry about it. Normal Python lists do not support the buffer protocol.
from array import array
Vt.Vec3hArray.FromBuffer(array("f", [1,2,3]))
# Returns:
# Vt.Vec3hArray(1, (Gf.Vec3h(1.0, 2.0, 3.0),))
# From Numpy
import numpy as np
vt_array = Vt.Vec3hArray.FromNumpy(np.ones((10, 3)))
Vt.Vec3hArray.FromBuffer(np.ones((10, 3))) # Numpy also supports the buffer protocol.
# Returns:
"""
Vt.Vec3hArray(10, (Gf.Vec3h(1.0, 1.0, 1.0), Gf.Vec3h(1.0, 1.0, 1.0), Gf.Vec3h(1.0, 1.0, 1.0), Gf.Vec3h(1.0, 1.
0, 1.0), Gf.Vec3h(1.0, 1.0, 1.0), Gf.Vec3h(1.0, 1.0, 1.0), Gf.Vec3h(1.0, 1.0, 1.0), Gf.Vec3h(1.0, 1.0, 1.0), G
f.Vec3h(1.0, 1.0, 1.0), Gf.Vec3h(1.0, 1.0, 1.0)))
"""
# We can also go the other way:
np.array(vt_array)
#// ANCHOR_END: dataTypeRoleOverview

#// ANCHOR: tfTypeRegistry
##### Types - pxr.Vt.Type Registry #####
# All registered types (including other plugin types, so not limited to data types)
# for type_def in Tf.Type.GetRoot().derivedTypes:
#    print(type_def)
type_def = Tf.Type.FindByName(Sdf.ValueTypeNames.TexCoord2fArray.cppTypeName)
print(type_def.typeName) # Returns: VtArray<GfVec2f> # The same as value_type_name.cppTypeName
# Root/Base/Derived Types
type_def.GetRoot(), type_def.baseTypes, type_def.derivedTypes
#// ANCHOR_END: tfTypeRegistry