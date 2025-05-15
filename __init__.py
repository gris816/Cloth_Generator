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
# from bpy.props import EnumProperty
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import StringProperty

# オブジェクト生成ロジック
class CLOTHICA_OT_generate_pattern(Operator):
    bl_idname = "clothica.generate_pattern"
    bl_label = "Generate Pattern"

    def execute(self, context):
        props = context.scene.clothica_pattern_props

        pattern_shapes = {
            'TOPS': [(-0.2475, 0.185, 0), (-0.2475, 0.105, 0), (-0.2475, -0.025, 0), (-0.2475, -0.185, 0),
                    (-0.155, 0.105, 0),
                    (-0.0645, 0.185, 0),(-0.0645, 0.105, 0),(-0.0645, 0.035, 0),(-0.0645, -0.025, 0),
                    (-0.0075, -0.025, 0),(-0.0075, -0.185, 0),
                    (0.0495, 0.035, 0),(0.0495, -0.025, 0),
                    (0.07, 0.035, 0),
                    (0.0765, 0.232, 0),(0.0765, -0.025, 0),
                    (0.2475, 0.232, 0),(0.2475, -0.025, 0),(0.2475, -0.185, 0)
                    ],
            # ここからは仮の座標
            'SLEEVE': [(-0.3, -0.2, 0), (0.3, -0.2, 0), (-0.2, 0.6, 0), (0.2, 0.6, 0)],
            'SKIRT': [(-0.4, -0.6, 0), (0.4, -0.6, 0), (-0.2, 0.6, 0), (0.2, 0.6, 0)],
            'PANTS_STRAIGHT': [(-0.3, -0.8, 0), (0.3, -0.8, 0), (-0.3, 0.8, 0), (0.3, 0.8, 0)],
            'PANTS_SLIM': [(-0.2, -0.8, 0), (0.2, -0.8, 0), (-0.1, 0.8, 0), (0.1, 0.8, 0)],
        }
        
        
        verts = pattern_shapes.get(props.pattern_type, pattern_shapes['TOPS'])

        mesh = bpy.data.meshes.new("mesh")
        obj  = bpy.data.objects.new(f"{props.pattern_type}_Pattern", mesh)
        context.scene.collection.objects.link(obj)

        bm = bmesh.new()
        bm_verts = [bm.verts.new(v) for v in verts]

        if props.pattern_type == 'TOPS':
            # ポリゴンを手動で定義
            faces = [
                (0, 1, 4, 6, 5), (1, 2, 8, 7, 6, 4), (2, 3, 10, 9, 8),
                (9, 10, 18, 17, 15, 12), (14, 15, 17, 16),
            ]
            for idxs in faces:
                try:
                    bm.faces.new([bm_verts[i] for i in idxs])
                except:
                    continue
            edges_only = [(7, 11), (11, 13),(11, 12),]
            for e in edges_only:
                try:
                    bm.edges.new([bm_verts[e[0]], bm_verts[e[1]]])
                except:
                    continue

        else:
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
        layout.label(text="Select Pattern Type:")
        for label in ['TOP', 'SLEEVE', 'SKIRT', 'PANTS_STRAIGHT', 'PANTS_SLIM']:
            op = layout.operator("clothica.generate_pattern", text=label.replace("_", " ").title())
            op.pattern_type = label


# 登録・解除
classes = [
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