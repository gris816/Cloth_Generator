
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
from bpy.props import EnumProperty, FloatProperty
from bpy.types import Operator, Panel

# オブジェクト生成ロジック
class CLOTHICA_OT_generate_pattern(Operator):
    bl_idname = "clothica.generate_pattern"
    bl_label = "Generate Pattern"

    pattern_type: EnumProperty(
        name="Pattern Type",
        items=[
            ('TOP', "Top", "Generate a top pattern"),
            ('SKIRT', "Skirt", "Generate a skirt pattern"),
            ('PANTS', "Pants", "Generate a pants pattern"),
            ('SLEEVE', "Sleeve", "Generate a sleeve pattern"),
        ],
        default='TOP'
    )

    width: FloatProperty(name="Width", default=0.4, min=0.1, max=2.0)
    height: FloatProperty(name="Height", default=0.6, min=0.1, max=3.0)

    def execute(self, context):
        verts = [(-0.5, -0.5, 0), (0.5, -0.5, 0.0),(-0.5,0.5, 0.0),(0.5,0.5,0.0)]

        # Create Empty Mesh & Object
        mesh = bpy.data.meshes.new("mesh")
        obj  = bpy.data.objects.new("ItaPoly", mesh)

        # Add Object
        scene = bpy.context.scene
        scene.collection.objects.link(obj)

        # Create Bmesh
        bm = bmesh.new()

        bm_verts = []
        for v in verts:
            b_v = bm.verts.new(v)
            bm_verts.append(b_v)

        v1 = bm_verts[0]
        v2 = bm_verts[1]
        v3 = bm_verts[2]
        v4 = bm_verts[3]

        bm.faces.new([v1,v3,v2])
        bm.faces.new([v2,v3,v4])

        # QUAD
        # bm.faces.new([v1,v2,v3,v4])

        bm.to_mesh(mesh)
        bm.free() # Release Bmesh
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
        layout.label(text="Generate Pattern")
        layout.operator("clothica.generate_pattern")

# 登録・解除
classes = [
    CLOTHICA_OT_generate_pattern,
    CLOTHICA_PT_pattern_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()