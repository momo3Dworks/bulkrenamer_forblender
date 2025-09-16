bl_info = {
    "name": "Naming Ruler",
    "author": "ChatGPT",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "3D View > Sidebar > Naming Ruler",
    "description": "Addon para renombrar objetos en lotes aplicando reglas de numeración o letras ascendentes",
    "category": "Object",
}

import bpy


def int_to_letters(n):
    """Convierte un número (0=A) a letras tipo Excel (A, B, ..., Z, AA, AB, ...)"""
    result = ""
    while True:
        n, r = divmod(n, 26)
        result = chr(65 + r) + result
        if n == 0:
            break
        n -= 1
    return result


def letters_to_int(s):
    """Convierte una letra (A=0, B=1, ..., Z=25, AA=26, ...) a número"""
    s = s.upper()
    result = 0
    for char in s:
        result = result * 26 + (ord(char) - ord("A") + 1)
    return result - 1


def rename_object(obj, prefix, suffix, numbering_mode, fixed_number, start_number, padding, floor_letter, start_letter, index):
    if numbering_mode == "FIXED":
        num_str = str(fixed_number).zfill(padding) if padding > 0 else str(fixed_number)
        return f"{prefix}{num_str}_{suffix.strip('_')}"

    elif numbering_mode == "ASCENDING":
        num_str = str(start_number + index).zfill(padding) if padding > 0 else str(start_number + index)
        return f"{prefix}{num_str}_{suffix.strip('_')}"

    elif numbering_mode == "LETTERS":
        base_index = letters_to_int(start_letter)
        apt_letter = int_to_letters(base_index + index)
        return f"{prefix}{floor_letter}_{apt_letter}_{suffix.strip('_')}"

    return obj.name


class NAMINGRULER_OT_rename(bpy.types.Operator):
    bl_idname = "object.namingruler_rename"
    bl_label = "Apply Naming Rule"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.namingruler_props

        if props.mode == "SELECTION":
            objs = [o for o in context.view_layer.objects if o.select_get() and o.type == 'MESH']
        else:
            objs = []
            if props.collection:
                def collect_recursive(coll):
                    for o in coll.objects:
                        if o.type == 'MESH':
                            objs.append(o)
                        for c in coll.children:
                            collect_recursive(c)
                collect_recursive(props.collection)

        objs.sort(key=lambda o: o.name)

        for i, obj in enumerate(objs):
            new_name = rename_object(
                obj,
                props.prefix,
                props.suffix,
                props.numbering_mode,
                props.fixed_number,
                props.start_number,
                props.padding,
                props.floor_letter,
                props.start_apartment_letter,
                i
            )

            if new_name not in bpy.data.objects:
                obj.name = new_name
            else:
                self.report({'WARNING'}, f"Saltado {obj.name}, '{new_name}' ya existe.")

        return {"FINISHED"}


class NAMINGRULER_PT_panel(bpy.types.Panel):
    bl_label = "Naming Ruler"
    bl_idname = "OBJECT_PT_namingruler"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Naming Ruler"

    def draw(self, context):
        layout = self.layout
        props = context.scene.namingruler_props

        layout.prop(props, "mode", expand=True)

        if props.mode == "COLLECTION":
            layout.prop(props, "collection")

        layout.prop(props, "prefix")
        layout.prop(props, "suffix")

        layout.prop(props, "numbering_mode", expand=True)

        if props.numbering_mode == "FIXED":
            layout.prop(props, "fixed_number")
            layout.prop(props, "padding")

        elif props.numbering_mode == "ASCENDING":
            layout.prop(props, "start_number")
            layout.prop(props, "padding")

        elif props.numbering_mode == "LETTERS":
            box = layout.box()
            box.label(text="Letters Mode Settings", icon="FONT_DATA")
            box.prop(props, "floor_letter", text="Floor Letter (Fixed)")
            box.prop(props, "start_apartment_letter", text="Start Apartment Letter (Ascending)")

        layout.operator("object.namingruler_rename", text="Apply Rule")


class NamingRulerProps(bpy.types.PropertyGroup):
    mode: bpy.props.EnumProperty(
        name="Mode",
        items=[
            ("SELECTION", "Selection", "Renombrar objetos seleccionados"),
            ("COLLECTION", "Collection", "Renombrar objetos dentro de una colección"),
        ],
        default="SELECTION"
    )

    prefix: bpy.props.StringProperty(name="Prefix", default="apt_")
    suffix: bpy.props.StringProperty(name="Suffix", default="south")

    numbering_mode: bpy.props.EnumProperty(
        name="Numbering",
        items=[
            ("FIXED", "Fixed", "Usar un número fijo"),
            ("ASCENDING", "Ascending", "Usar números ascendentes"),
            ("LETTERS", "Letters", "Usar letras ascendentes"),
        ],
        default="FIXED"
    )

    fixed_number: bpy.props.IntProperty(name="Fixed Number", default=1, min=0)
    start_number: bpy.props.IntProperty(name="Start Number", default=1, min=0)
    padding: bpy.props.IntProperty(name="Padding", default=0, min=0, max=5)

    floor_letter: bpy.props.StringProperty(name="Floor Letter", default="A", maxlen=2)
    start_apartment_letter: bpy.props.StringProperty(name="Start Apartment Letter", default="A", maxlen=2)

    collection: bpy.props.PointerProperty(name="Collection", type=bpy.types.Collection)


classes = (
    NamingRulerProps,
    NAMINGRULER_OT_rename,
    NAMINGRULER_PT_panel,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.namingruler_props = bpy.props.PointerProperty(type=NamingRulerProps)


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.namingruler_props


if __name__ == "__main__":
    register()
