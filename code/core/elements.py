"""This file contains all code examples for the 'Core Elements' section.
The following mdBook syntax allows us to sparsely import content:
#// ANCHOR: contentId
def example():
    print("here")
#// ANCHOR_END: contentId
"""

"""Path.md"""
#// ANCHOR: pathBasics
from pxr import Sdf
path = Sdf.Path("/set/bicycle")
path_name = path.name     # Similar to os.path.basename(), returns the last element of the path
path_empty = path.isEmpty # Property to check if path is empty
path_startswith = path.HasPrefix(Sdf.Path("/set")) # Same as Python Str's .startswith
path = Sdf.Path(Sdf.childDelimiter.join(["set", "bicycle"])) # Manually join individual path elements
# Do not use this is performance critical loops
# See for more info: https://openusd.org/release/api/_usd__page__best_practices.html
# This gives you a standard python string
path_str = path.pathString
#// ANCHOR_END: pathBasics

#// ANCHOR: pathSpecialPaths
from pxr import Sdf
# Shortcut for Sdf.Path("/")
root_path = Sdf.Path.absoluteRootPath
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
property_name = path.name # Be aware, this will return "size" (last element)
# Properties can also be namespaced with ":" (Sdf.Path.namespaceDelimiter)
path = Sdf.Path("/set/bicycle.tire:size")
# Convenience methods
path = Sdf.Path("/set/bicycle").AppendProperty(Sdf.Path.JoinIdentifier(["tire", "size"]))
namespaced_elements = Sdf.Path.TokenizeIdentifier("tire:size") # Returns: ["tire", "size"]
#// ANCHOR_END: pathProperties




Sdf.Path.emptyPath
Sdf.Path.propertyDelimiter
Sdf.Path.namespaceDelimiter
Sdf.Path.childDelimiter
Sdf.Path.absoluteIndicator
Sdf.Path.parentPathElement


'AncestorsRange',
'AppendChild', 
'AppendElementString',
'AppendExpression', 
'AppendMapper', 
'AppendMapperArg', 
'AppendPath', 
'AppendProperty',
'AppendRelationalAttribute', 
'AppendTarget', 
'AppendVariantSelection', 
'ContainsPrimVariantSelection',
'ContainsPropertyElements',
'ContainsTargetPath',
'FindLongestPrefix', 
'FindLongestStrictPrefix', 
'FindPrefixedRange', 
'GetAbsoluteRootOrPrimPath', 
'GetAllTargetPathsRecursively',
'GetAncestorsRange', 
'GetCommonPrefix', 
'GetConciseRelativePaths', 
'GetParentPath',
'GetPrefixes',
'GetPrimOrPrimVariantSelectionPath',
'GetPrimPath',
'GetVariantSelection',
'HasPrefix',
'IsAbsolutePath',
'IsAbsoluteRootOrPrimPath', 
'IsAbsoluteRootPath', 
'IsExpressionPath', 
'IsMapperArgPath',
'IsMapperPath',
'IsNamespacedPropertyPath', 
'IsPrimPath', 
'IsPrimPropertyPath', 
'IsPrimVariantSelectionPath', 
'IsPropertyPath',
IsRelationalAttributePath',
'IsRootPrimPath',
'IsTargetPath',
'IsValidIdentifier',
'IsValidNamespacedIdentifier',
'IsValidPathString', 
'MakeAbsolutePath',
'MakeRelativePath', 
'RemoveAncestorPaths', 
'RemoveCommonSuffix',
'RemoveDescendentPaths', 
'ReplaceName',
'ReplacePrefix', 
'ReplaceTargetPath', 
'StripAllVariantSelections',
'StripNamespace', 
'StripPrefixNamespace',


'expressionIndicator',

'mapperArgDelimiter',
'mapperIndicator',

'reflexiveRelativePath',
'relationshipTargetEnd', 
'relationshipTargetStart', 
'targetPath']