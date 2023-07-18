import pxr
import numpy as np

class Tokens():
    mode = "vfxSurvivalGuide:attributeKernel:mode"
    module_code = "vfxSurvivalGuide:attributeKernel:moduleCode"
    execute_code = "vfxSurvivalGuide:attributeKernel:executeCode"
    bindings = "vfxSurvivalGuide:attributeKernel:bindings"

class Binding():
    fallback_value_type_name = pxr.Sdf.ValueTypeNames.FloatArray
    def __init__(self):
        self.property_name = ""
        self.variable_name = ""
        self.value_type_name = ""

class Point():
    def __init__(self, bindings):
        self.ptnum = -1
        self.bindings = bindings
        for binding in self.bindings:
            setattr(self, binding.variable_name, None)
                
class Points():
    def __init__(self):
        self.bindings = []
        for binding in self.bindings:
            setattr(self, binding.variable_name, [])
          
def run_kernel(stage, frame):
    # Process
    for prim in stage.Traverse():
        attr = prim.GetAttribute(Tokens.bindings)
        if not attr:
            continue
        if not attr.HasValue():
            continue

        mode = prim.GetAttribute(Tokens.mode).Get(frame)
        module_code = prim.GetAttribute(Tokens.module_code).Get(frame)
        execute_code = prim.GetAttribute(Tokens.execute_code).Get(frame)
        bindings_serialized = eval(prim.GetAttribute(Tokens.bindings).Get(frame))
        
        # Bindings
        bindings = []
        for binding_dict in bindings_serialized:
            binding = Binding()
            binding.property_name = binding_dict["property_name"]
            binding.variable_name = binding_dict["variable_name"]
            binding.value_type_name = binding_dict["value_type_name"]
            bindings.append(binding)
        # Kernel
        module_code_compiled = compile(module_code, "module_code", "exec")
        execute_code_compiled = compile(execute_code, "code", "exec")
        exec(module_code_compiled)
        # Read data
        input_data = {}
        input_point_count = -1
        output_data = {}
        output_point_count = -1
        initialize_attrs = []
        for binding in bindings:
            # Read attribute or create default fallback value
            attr = prim.GetAttribute(binding.property_name)
            if not attr:   
                value_type_name_str = binding.fallback_value_type_name if binding.value_type_name == "automatic" else binding.value_type_name
                value_type_name = getattr(pxr.Sdf.ValueTypeNames, value_type_name_str)
                attr = prim.CreateAttribute(binding.property_name, value_type_name)
            if attr.HasValue():
                input_data[binding.property_name] = np.array(attr.Get(frame))
                input_point_count = max(input_point_count, len(input_data[binding.property_name]))
            else:
                initialize_attrs.append(attr)
            # Enforce interpolation to points
            attr.SetMetadata(pxr.UsdGeom.Tokens.interpolation, pxr.UsdGeom.Tokens.vertex)
            output_data[binding.property_name] = []
        for initialize_attr in initialize_attrs:
            input_data[initialize_attr.GetName()] = np.array([initialize_attr.GetTypeName().scalarType.defaultValue] * input_point_count)
        # Utils
        def npoints():
            return input_point_count
        # Modes
        if mode == "kernel":
            # Kernel Utils
            points_add = []
            points_remove = set()
            def create_point():
                point = Point(bindings)
                points_add.append(point)
            def copy_point(source_point):
                point = Point(source_point.bindings)
                for binding in point.bindings:
                    setattr(point, binding.variable_name, np.copy(getattr(source_point, binding.variable_name)))
                points_add.append(point)
                return point
            def remove_point(point):
                points_remove.add(point.ptnum)
            # Kernel
            point = Point(bindings)
            for elemnum in range(len(list(input_data.values())[0])):
                point.ptnum = elemnum
                for binding in bindings:
                    setattr(point, binding.variable_name, input_data[binding.property_name][elemnum])
                # User Kernel Start
                exec(execute_code_compiled)
                # User Kernel End
                if points_remove and point.ptnum in points_remove:
                    continue
                for binding in bindings:
                    output_data[binding.property_name].append(getattr(point, binding.variable_name))
            for binding in bindings:
                for point_add in points_add:
                    output_data[binding.property_name].append(getattr(point_add, binding.variable_name))
            for binding in bindings:
                output_data[binding.property_name] = np.array(output_data[binding.property_name])
                output_point_count = max(output_point_count, len(output_data[binding.property_name]))
        elif mode == "array":
            points = Points()
            for binding in bindings:
                setattr(points, binding.variable_name, input_data[binding.property_name])
            # User Kernel Start
            exec(execute_code_compiled)
            # User Kernel End
            for binding in bindings:
                output_data[binding.property_name] = getattr(points, binding.variable_name)
                output_point_count = max(output_point_count, len(output_data[binding.property_name]))
        # If the output is invalid, block it to prevent segfaults
        if input_point_count != output_point_count:
            for attr in prim.GetAttributes():
                if attr.GetName() in input_data.keys():
                    continue
                if not attr.HasValue():
                    continue
                if not attr.GetTypeName().isArray:
                    continue
                if len(attr.Get(frame)) == output_point_count:
                    continue
                attr.Set(pxr.Sdf.ValueBlock())
        # Write data
        for binding in bindings:
            attr = prim.GetAttribute(binding.property_name)
            if len(output_data[binding.property_name]) != output_point_count:
                attr.Set(pxr.Sdf.ValueBlock())
                continue
            attr_class = attr.GetTypeName().type.pythonClass
            attr.Set(attr_class.FromNumpy(output_data[binding.property_name]), frame)
        # Re-Compute extent hints
        boundable_api = pxr.UsdGeom.Boundable(prim)
        extent_attr = boundable_api.GetExtentAttr()
        extent_value = pxr.UsdGeom.Boundable.ComputeExtentFromPlugins(boundable_api, frame)
        if extent_value:
            extent_attr.Set(extent_value, frame)
