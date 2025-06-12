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
        'TOPS': [(-0.2475, 0.185, 0),(-0.2237, 0.18653, 0), (-0.202035, 0.193, 0), (-0.1884, 0.19859, 0), (-0.176, 0.20883, 0),
                 (-0.15, 0.20045, 0), (-0.13499, 0.19562, 0), (-0.15, 0.105, 0), (-0.11701, 0.18982, 0), (-0.03578, 0.16364, 0),
                 (-0.057404, 0.10163, 0), (-0.062591, 0.055038, 0), (-0.0645, 0.035, 0), (-0.059229, 0.016968, 0), (-0.051355, 0.001874, 0), 
                 (-0.045018, -0.005729, 0), (-0.036695, -0.013234, 0),(-0.025898, -0.020157, 0),
                 (-0.0075, -0.025, 0), #ウエストダーツc頂点
                 (0.01001, -0.021848, 0),(0.022857, -0.016008, 0), (0.032592, -0.008092, 0), (0.039718, 0.001836, 0), (0.046103, 0.016426, 0),
                 (0.0495, 0.035, 0),
                 (0.0645, 0.02647, 0), #ウエストダーツb頂点
                 (0.155, -0.025, 0), (0.074536, 0.065862, 0), (0.076477, 0.07598, 0), (0.076507, 0.082521, 0), (0.073449, 0.12211, 0),
                 (0.066094, 0.1581, 0), (0.0585, 0.18402, 0),(0.0765, 0.19127, 0), (0.178, 0.232, 0), (0.18328, 0.20644, 0),
                 (0.18856, 0.19568, 0), (0.19864, 0.18279, 0), (0.2112, 0.17401, 0), (0.22114, 0.16906, 0), 
                 (0.2475, 0.162, 0), (0.2475, -0.025, 0), (0.2475, -0.185, 0), 
                 (0.162, -0.185, 0), (0.155, -0.185, 0),(0.148, -0.185, 0), #ウエストダーツa
                 (0.072, -0.185, 0), (0.0645, -0.185, 0), (0.057, -0.185, 0), #ウエストダーツb
                 (-0.002, -0.185, 0), (-0.0075, -0.185, 0), (-0.013, -0.185, 0), #ウエストダーツc
                 (-0.057, -0.185, 0), (-0.0745, -0.185, 0), (-0.092, -0.185, 0), #ウエストダーツd
                 (-0.146, -0.185, 0), (-0.155, -0.185, 0), (-0.164, -0.185, 0), #ウエストダーツe
                 (-0.241, -0.185, 0), (-0.2475, -0.185, 0), #ウエストダーツf
                 (-0.2475, -0.025, 0), 
                 (-0.2475, 0.105, 0), #ウエストダーツf頂点
                 (-0.155, -0.005, 0), #ウエストダーツe頂点
                 (-0.0745, 0.035, 0), #ウエストダーツd頂点
                 (0.155, -0.045, 0)   #ウエストダーツa頂点
                  ],

        'SLEEVE': [(-0.3, -0.2, 0), (0.3, -0.2, 0), (-0.2, 0.6, 0), (0.2, 0.6, 0)],
        'SKIRT': [(-0.2825, -0.1, 0), (-0.2825,-0.3, 0),
                  (-0.2425, 0.295, 0), (-0.2425, 0.12, 0), (-0.2425, 0.09, 0), (-0.2425, -0.1, 0), (-0.2425, -0.3, 0),
                  (-0.165, 0.30055, 0), (-0.165, 0.12, 0),
                  (-0.14979, 0.30121, 0),
                  (-0.14479, 0.17081, 0),
                  (-0.13458, 0.3025, 0),
                  (-0.10271, 0.3049, 0),
                  (-0.0875, 0.12, 0), (-0.0875, 0.30607, 0),
                  (-0.082867, 0.1865, 0),
                  (-0.072292, 0.30723, 0),
                  (-0.035719, 0.31, 0),
                  (-0.031666, 0.3, 0),
                  (-0.020833, 0.24, 0),
                  (-0.01, 0.12, 0), (-0.01, -0.3, 0),
                  (0.000833, 0.24, 0),
                  (0.011666, 0.3, 0),
                  (0.015719, 0.31, 0),
                  (0.074167, 0.3061, 0), (0.074167, 0.12, 0),
                  (0.086, 0.30538, 0), (0.086, 0.2075, 0),
                  (0.097833, 0.30462, 0),
                  (0.13966, 0.30186, 0),
                  (0.149, 0.30125, 0), (0.149, 0.2075, 0),
                  (0.15833, 0.12, 0),
                  (0.15839, 0.30062, 0),
                  (0.2425, 0.295, 0), (0.2425, 0.2075, 0), (0.2425, 0.12, 0), (0.2425, -0.3, 0)
                  ],
        'PANTS_STRAIGHT': [(-0.3, -0.8, 0), (0.3, -0.8, 0), (-0.3, 0.8, 0), (0.3, 0.8, 0)],
        'PANTS_SLIM': [(-0.2, -0.8, 0), (0.2, -0.8, 0), (-0.1, 0.8, 0), (0.1, 0.8, 0)],
        }
    return shapes.get(pattern_type, [])

#面＋辺構成定義関数
def get_faces_and_edges(pattern_type):
    mapping = {
        'TOPS': {
           'faces': [(0, 61, 60, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1),
                      (60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 50, 18),
                      (18, 19, 20, 21, 22, 23, 24, 25, 26),(27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 26),
                      (18, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41)],
            'edges': [(61, 58), 
                      (62, 55), (62, 56), (62, 57), 
                      (63, 52), (63, 53), (63, 54), 
                      (18, 49), (18, 50), (18, 51), 
                      (25, 46), (25, 47), (25, 48), 
                      (64, 43), (64, 44), (64, 45)]
        },
        'SLEEVE': {
            'faces': [],
            'edges': []
        },
        'SKIRT': {
            'faces': [(0, 1, 6, 5), (3, 4, 5, 6, 21, 20, 13, 8), (20, 21, 38, 37, 33, 26), 
                      (2, 3, 8, 13, 20, 19, 18, 17, 16, 15, 12, 11, 10, 7), 
                      (24, 23, 22, 20, 26, 33, 37, 36, 35, 34, 32, 30, 29, 28, 25)],
            'edges': [(7, 9), (9, 11), (9, 10),
                      (12, 14), (14, 16,), (14, 15),
                      (25, 27), (27, 29), (27, 28),
                      (30, 31), (31, 34), (31, 32)]
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
        
        for label in ['TOPS', 'SLEEVE', 'SKIRT', 'PANTS_STRAIGHT', 'PANTS_SLIM']:
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