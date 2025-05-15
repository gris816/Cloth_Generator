bl_info = {
    "name": "Clothica Pattern Generator",
    "blender": (4, 2, 0),
    "category": "3D View",
    "author": "Your Name",
    "version": (1, 0, 0),
    "description": "Generate basic garment pattern pieces (tops, skirts, sleeves, etc.) as editable mesh objects."
}

import bpy
import bmesh
from bpy.types import Operator, Panel
from bpy.props import StringProperty

# メッシュ形状の定義関数
def get_pattern_shape(pattern_type):
    shapes = {
        'TOPS': [(-0.2475, 0.185, 0), (-0.2475, 0.105, 0), (-0.2475, -0.025, 0), (-0.2475, -0.185, 0),
                    (-0.155, 0.105, 0),
                    (-0.0645, 0.185, 0),(-0.0645, 0.105, 0),(-0.0645, 0.035, 0),(-0.0645, -0.025, 0),
                    (-0.0075, -0.025, 0),(-0.0075, -0.185, 0),
                    (0.0495, 0.035, 0),(0.0495, -0.025, 0),
                    (0.07, 0.035, 0),
                    (0.0765, 0.232, 0),(0.0765, -0.025, 0),
                    (0.2475, 0.232, 0),(0.2475, -0.025, 0),(0.2475, -0.185, 0)
                    ],
        'SLEEVE': [(-0.3, -0.2, 0), (0.3, -0.2, 0), (-0.2, 0.6, 0), (0.2, 0.6, 0)],
        'SKIRT': [
                      ],
        'PANTS_STRAIGHT': [(-0.3, -0.8, 0), (0.3, -0.8, 0), (-0.3, 0.8, 0), (0.3, 0.8, 0)],
        'PANTS_SLIM': [(-0.2, -0.8, 0), (0.2, -0.8, 0), (-0.1, 0.8, 0), (0.1, 0.8, 0)],
        }
    return shapes.get(pattern_type, [])

#面＋辺構成定義関数
def get_faces_and_edges(pattern_type):
    mapping = {
        'TOPS': {
            'faces': [(0, 1, 4, 6, 5), (1, 2, 8, 7, 6, 4), (2, 3, 10, 9, 8),
                (9, 10, 18, 17, 15, 12), (14, 15, 17, 16),],
            'edges': [(6, 8), (9, 7), (11, 13), (14, 16), (15, 17), (17, 18)]
        },
        'SLEEVE': {
            'faces': [],
            'edges': []
        },
        'SKIRT': {
            'faces': [],
            'edges': []
        },
        'PANTS_STRAIGHT': {
            'faces': [],
            'edges': []
        },
        'PANTS_SLIM': {
            'faces': [],
            'edges': []
        },
    }
    return mapping.get(pattern_type, {'faces': [], 'edges': []})


# メッシュ生成オペレータ
class CLOTHICA_OT_generate_pattern(Operator):
    bl_idname = "clothica.generate_pattern"
    bl_label = "Generate Pattern"

    pattern_type: StringProperty()

    def execute(self, context):
        verts = get_pattern_shape(self.pattern_type)
        mesh = bpy.data.meshes.new(f"{self.pattern_type}_Mesh")
        obj  = bpy.data.objects.new(f"{self.pattern_type}_Pattern", mesh)
        context.scene.collection.objects.link(obj)

        bm = bmesh.new()
        bm_verts = [bm.verts.new(v) for v in verts]

        structure = get_faces_and_edges(self.pattern_type)
        for f in structure['faces']:
            try: bm.faces.new([bm_verts[i] for i in f])
            except: continue
        for e in structure['edges']:
            try: bm.edges.new([bm_verts[e[0]], bm_verts[e[1]]])
            except: continue      

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

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()