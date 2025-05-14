bl_info = {
    "name": "Clothica Pattern Generator",
    "blender": (4, 2, 0),
    "category": "3D View",
    "author": "Your Name",
    "version": (0, 1),
    "description": "Generate basic garment pattern pieces (tops, skirts, sleeves, etc.) as editable mesh objects."
}

import bpy
import bmesh
from bpy.props import EnumProperty
from bpy.types import Operator, Panel, PropertyGroup

# プロパティ格納用
class CLOTHICA_PatternProperties(PropertyGroup):
    pattern_type: EnumProperty(
        name="Pattern Type",
        items=[
            ('TOPS', "TOPS", "Generate a top pattern"),
            ('SLEEVE', "SLEEVE", "Generate a sleeve pattern"),
            ('SKIRT', "TIGHT SKIRT", "Generate a tight skirt pattern"),
            ('PANTS_STRAIGHT', "STRAIGHT PANTS", "Generate a straight pants pattern"),
            ('PANTS_SLIM', "SLIM PANTS", "Generate a slim pants pattern"),
        ],
        default='TOPS'
    ) # type: ignore

# オブジェクト生成ロジック
class CLOTHICA_OT_generate_pattern(Operator):
    bl_idname = "clothica.generate_pattern"
    bl_label = "Generate Pattern"

    def execute(self, context):
        props = context.scene.clothica_pattern_props

        verts = [
            (-0.5, -0.5, 0), (0.5, -0.5, 0.0),
            (-0.5, 0.5, 0.0), (0.5, 0.5, 0.0)
        ]

        mesh = bpy.data.meshes.new("mesh")
        obj  = bpy.data.objects.new(f"{props.pattern_type}_Pattern", mesh)
        context.scene.collection.objects.link(obj)

        bm = bmesh.new()
        bm_verts = [bm.verts.new(v) for v in verts]
        bm.faces.new([bm_verts[0], bm_verts[2], bm_verts[1]])
        bm.faces.new([bm_verts[1], bm_verts[2], bm_verts[3]])

        bm.to_mesh(mesh)
        bm.free()

        return {'FINISHED'}

# パネルUI
class CLOTHICA_PT_pattern_panel(Panel):
    bl_label = "Clothica Pattern Generator"
    bl_idname = "CLOTHICA_PT_pattern_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Clothica'

    def draw(self, context):
        layout = self.layout
        props = getattr(context.scene, "clothica_pattern_props", None)
        if not props:
            layout.label(text="(Pattern properties not initialized)")
            return
        layout.label(text="Generate Pattern")
        layout.prop(props, "pattern_type")
        layout.operator("clothica.generate_pattern")

# 登録・解除
classes = [
    CLOTHICA_PatternProperties,
    CLOTHICA_OT_generate_pattern,
    CLOTHICA_PT_pattern_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    if hasattr(bpy.types.Scene, "clothica_pattern_props"):
        del bpy.types.Scene.clothica_pattern_props
    bpy.types.Scene.clothica_pattern_props = bpy.props.PointerProperty(type=CLOTHICA_PatternProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.clothica_pattern_props

if __name__ == "__main__":
    register()

