#// ANCHOR: productionConceptsSdfBatchNamespaceMoveRenameDelete
### High Level / Low Level ###
# The Sdf.BatchNamespaceEdit() always runs only on an individual layer.
from pxr import Gf, Sdf, Usd
stage = Usd.Stage.CreateInMemory()
layer = stage.GetEditTarget().GetLayer()
bicycle_prim_path = Sdf.Path("/bicycle")
bicycle_prim = stage.DefinePrim(bicycle_prim_path, "Xform")
bicycle_color_attr = bicycle_prim.CreateAttribute("color", Sdf.ValueTypeNames.Color3h)
bicycle_color_attr.Set(Gf.Vec3h([0,1,2]))
car_prim_path = Sdf.Path("/car")
car_prim = stage.DefinePrim(car_prim_path, "Xform")
soccer_ball_prim_path = Sdf.Path("/soccer_ball")
soccer_ball_prim = stage.DefinePrim(soccer_ball_prim_path, "Xform")
soccer_ball_player_rel = soccer_ball_prim.CreateRelationship("player")
soccer_ball_player_rel.SetTargets([Sdf.Path("/players/mike")])

print(layer.ExportToString())
"""Returns:
#usda 1.0

def Xform "bicycle"
{
    custom color3h color = (0, 1, 2)
}

def Xform "car"
{
}

def Xform "soccer_ball"
{
    custom rel player = </players/mike>
}
"""
with Sdf.ChangeBlock():
    edit = Sdf.BatchNamespaceEdit()
    ## Important: Edits are run in the order they are added.
    # If we try to move and then remove, it will error.
    ## Prim Specs
    # Remove
    edit.Add(car_prim_path, Sdf.Path.emptyPath)
    # Move
    edit.Add(bicycle_prim_path, car_prim_path)
    # Rename
    basket_ball_prim_path = soccer_ball_prim_path.ReplaceName("basket_ball")
    edit.Add(soccer_ball_prim_path, basket_ball_prim_path)
    ## Property Specs
    edit.Add(car_prim_path.AppendProperty("color"), car_prim_path.AppendProperty("style"))
    soccer_ball_player_rel_path = basket_ball_prim_path.AppendProperty("player")
    edit.Add(soccer_ball_player_rel_path, soccer_ball_player_rel_path.ReplaceName("people"))
    
    # We can als 
    if not layer.Apply(edit):
        raise Exception("Failed to apply layer edit!")
        
print(layer.ExportToString())
"""Returns:
#usda 1.0
def Xform "car"
{
    custom color3h style = (0, 1, 2)
}

def Xform "basket_ball"
{
    custom rel people = </players/mike>
}
"""
#// ANCHOR_END: productionConceptsSdfBatchNamespaceMoveRenameDelete


#// ANCHOR: productionConceptsSdfBatchNamespaceEditVariant
### High Level / Low Level ###
# The Sdf.BatchNamespaceEdit() always runs only on an individual layer.
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
prim_path = Sdf.Path("/bicycle")
prim = stage.DefinePrim(prim_path, "Xform")
stage.DefinePrim(Sdf.Path("/bicycle/cube"), "Cube")

layer = stage.GetEditTarget().GetLayer()
with Sdf.ChangeBlock():
    edit = Sdf.BatchNamespaceEdit()
    prim_spec = layer.GetPrimAtPath(prim_path)
    # Move content into variant
    variant_set_spec = Sdf.VariantSetSpec(prim_spec, "model")
    variant_spec = Sdf.VariantSpec(variant_set_spec, "myCoolVariant")
    variant_prim_path = prim_path.AppendVariantSelection("model", "myCoolVariant")
    edit.Add(prim_path.AppendChild("cube"), variant_prim_path.AppendChild("cube"))
    # Variant selection
    prim_spec.SetInfo("variantSetNames", Sdf.StringListOp.Create(prependedItems=["model"]))
    prim_spec.variantSelections["model"] = "myCoolVariant"
        
    if not layer.Apply(edit):
        raise Exception("Failed to apply layer edit!")
#// ANCHOR_END: productionConceptsSdfBatchNamespaceEditVariant


#// ANCHOR: productionConceptsSdfCopySpecStandard
### High Level / Low Level ###
# The Sdf.BatchNamespaceEdit() always runs only on an individual layer.
from pxr import Gf, Sdf, Usd
stage = Usd.Stage.CreateInMemory()
layer = stage.GetEditTarget().GetLayer()
bicycle_prim_path = Sdf.Path("/bicycle")
bicycle_prim = stage.DefinePrim(bicycle_prim_path, "Xform")
bicycle_color_attr = bicycle_prim.CreateAttribute("color", Sdf.ValueTypeNames.Color3h)
bicycle_color_attr.Set(Gf.Vec3h([0,1,2]))
car_prim_path = Sdf.Path("/car")
car_prim = stage.DefinePrim(car_prim_path, "Xform")
soccer_ball_prim_path = Sdf.Path("/soccer_ball")
soccer_ball_prim = stage.DefinePrim(soccer_ball_prim_path, "Xform")
soccer_ball_player_rel = soccer_ball_prim.CreateRelationship("player")
soccer_ball_player_rel.SetTargets([Sdf.Path("/players/mike")])

print(layer.ExportToString())
"""Returns:
#usda 1.0
def Xform "bicycle"
{
    custom color3h color = (0, 1, 2)
}

def Xform "car"
{
}

def Xform "soccer_ball"
{
    custom rel player = </players/mike>
}
"""
# When copying data, the target prim spec will be replaced by the source prim spec.
# The data will not be averaged
with Sdf.ChangeBlock():
    # Copy Prim Spec
    Sdf.CopySpec(layer, soccer_ball_prim_path, layer, car_prim_path.AppendChild("soccer_ball"))
    # Copy Property
    Sdf.CopySpec(layer, bicycle_color_attr.GetPath(), layer, car_prim_path.AppendChild("soccer_ball").AppendProperty("color"))
print(layer.ExportToString())
"""Returns:
#usda 1.0
def Xform "bicycle"
{
    custom color3h color = (0, 1, 2)
}

def Xform "car"
{
    def Xform "soccer_ball"
    {
        custom color3h color = (0, 1, 2)
        custom rel player = </players/mike>
    }
}

def Xform "soccer_ball"
{
    custom rel player = </players/mike>
}
"""
#// ANCHOR_END: productionConceptsSdfCopySpecStandard


#// ANCHOR: productionConceptsSdfCopySpecVariant
### High Level / Low Level ###
# The Sdf.CopySpec() always runs on individual layers.
from pxr import Sdf, Usd
stage = Usd.Stage.CreateInMemory()
bicycle_prim_path = Sdf.Path("/bicycle")
bicycle_prim = stage.DefinePrim(bicycle_prim_path, "Xform")
cube_prim_path = Sdf.Path("/cube")
cube_prim = stage.DefinePrim(cube_prim_path, "Cube")

layer = stage.GetEditTarget().GetLayer()
with Sdf.ChangeBlock():
    edit = Sdf.BatchNamespaceEdit()
    prim_spec = layer.GetPrimAtPath(bicycle_prim_path)
    # Copy content into variant
    variant_set_spec = Sdf.VariantSetSpec(prim_spec, "model")
    variant_spec = Sdf.VariantSpec(variant_set_spec, "myCoolVariant")
    variant_prim_path = bicycle_prim_path.AppendVariantSelection("model", "myCoolVariant")
    Sdf.CopySpec(layer, cube_prim_path, layer, variant_prim_path.AppendChild("cube"))
    # Variant selection
    prim_spec.SetInfo("variantSetNames", Sdf.StringListOp.Create(prependedItems=["model"]))
    prim_spec.variantSelections["model"] = "myCoolVariant"
print(layer.ExportToString())
"""Returns:
#usda 1.0

def Xform "bicycle" (
    variants = {
        string model = "myCoolVariant"
    }
    prepend variantSets = "model"
)
{
    variantSet "model" = {
        "myCoolVariant" {
            def Cube "cube"
            {
            }

        }
    }
}

def Cube "cube"
{
}
"""
#// ANCHOR_END: productionConceptsSdfCopySpecVariant



#// ANCHOR: productionConceptsSdfChangeBlock
from pxr import Sdf, Tf, Usd
def callback(notice, sender):
    print("Changed Paths", notice.GetResyncedPaths())
stage = Usd.Stage.CreateInMemory()
# Add
listener = Tf.Notice.Register(Usd.Notice.ObjectsChanged, callback, stage)
# Edit
layer = stage.GetEditTarget().GetLayer()
for idx in range(5):
    Sdf.CreatePrimInLayer(layer, Sdf.Path(f"/test_{idx}"))
# Remove
listener.Revoke()
# Returns:
"""
Changed Paths [Sdf.Path('/test_0')]
Changed Paths [Sdf.Path('/test_1')]
Changed Paths [Sdf.Path('/test_2')]
Changed Paths [Sdf.Path('/test_3')]
Changed Paths [Sdf.Path('/test_4')]
"""
stage = Usd.Stage.CreateInMemory()
# Add
listener = Tf.Notice.Register(Usd.Notice.ObjectsChanged, callback, stage)
with Sdf.ChangeBlock():
    # Edit
    layer = stage.GetEditTarget().GetLayer()
    for idx in range(5):
        Sdf.CreatePrimInLayer(layer, Sdf.Path(f"/test_{idx}"))
# Remove
listener.Revoke()
# Returns:
# Changed Paths [Sdf.Path('/test_0'), Sdf.Path('/test_1'), Sdf.Path('/test_2'), Sdf.Path('/test_3'), Sdf.Path('/test_4')]
#// ANCHOR_END: productionConceptsSdfChangeBlock