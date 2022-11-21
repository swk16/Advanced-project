# -*- coding: utf-8 -*-

import bpy, bmesh, math, mathutils
from bpy_extras import object_utils

def create_mesh_object(context, verts, edges, faces, name, operator=None):
  
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, edges, faces)
    mesh.validate(verbose=True)
    mesh.update(calc_edges=True)
    obj = object_utils.object_data_add(context, mesh, operator=None)
    return(obj)

def vertex_rotate_2d(start_x, start_y, center_x, center_y, angle):
    
    end_x = math.cos(angle) * (start_x - center_x) - math.sin(angle) * (start_y - center_y) + center_x
    end_y = math.sin(angle) * (start_x - center_x) + math.cos(angle) * (start_y - center_y) + center_y
    return(end_x, end_y)

def get_golden_ratio():
    '''黄金分割比例'''
    return((math.sqrt(5) - 1) / 2)

def calc_circle_symbols_loc_rot(count, radius, with_offset=False, reverse_offset=False):
    
    locations, rotations = [], []
    single_angle = math.pi * 2 / count
    for index in range(count):
        tmp_angle = single_angle * index
        if with_offset:
            if reverse_offset:
                tmp_angle -= single_angle / 2
            else:
                tmp_angle += single_angle / 2
        end_x, end_y = vertex_rotate_2d(0, -radius, 0, 0, -tmp_angle)
        locations.append([end_x, end_y, 0])
        rotations.append(mathutils.Euler((0, 0, math.pi-tmp_angle), 'XYZ'))
    return(locations, rotations)

def create_collection(context, name):
    
    tmp_col = bpy.data.collections.new(name)
    context.scene.collection.children.link(tmp_col)
    return(tmp_col)

def objects2collection(context, obj_list, collection):
    
    for tmp_obj in obj_list:
        for tmp_col in tmp_obj.users_collection:
            tmp_col.objects.unlink(tmp_obj)
        collection.objects.link(tmp_obj)

def set_parent(children, parent):
    
    for child in children:
        child.parent = parent
        child.matrix_parent_inverse = parent.matrix_world.inverted()

class YiJingGuaSymbol(object):
    
    def __init__(self):
        self.golden_ratio = get_golden_ratio()
        self.width_yang = 0
        self.width_yin = 0
        self.height = 0
        self.offset = 0

    def __verts_yao(self, is_yang=True, offset_h=0, offset_v=0):
        
        width_half = self.width_yang / 2
        if is_yang:
            verts = [
                (width_half, offset_h, 0),
                (width_half, self.height+offset_h, 0),
                (-width_half, self.height+offset_h, 0),
                (-width_half, offset_h, 0),
            ]
            faces = [(offset_v, offset_v+1, offset_v+2, offset_v+3)]
        else:
            verts = [
                (width_half-self.width_yin, offset_h, 0),
                (width_half, offset_h, 0),
                (width_half, self.height+offset_h, 0),
                (width_half-self.width_yin, self.height+offset_h, 0),
                (-width_half+self.width_yin, offset_h, 0),
                (-width_half+self.width_yin, self.height+offset_h, 0),
                (-width_half, self.height+offset_h, 0),
                (-width_half, offset_h, 0),
            ]
            faces = [
                (offset_v, offset_v+1, offset_v+2, offset_v+3),
                (offset_v+4, offset_v+5, offset_v+6, offset_v+7)
            ]
        return(verts, faces)

    def __calc_symbols_loc_rot(self, count, radius, with_offset=True):
        
        right_locations, left_locations = [], []
        right_rotations, left_rotations = [], []
        use_num = int(count / 2)
        single_angle = math.pi / use_num
        for index in range(use_num):
            tmp_angle = single_angle * index
            if with_offset:
                tmp_angle += single_angle / 2
            end_x, end_y = vertex_rotate_2d(0, -radius, 0, 0, tmp_angle)
            right_locations.append([end_x, end_y, 0])
            right_rotations.append(mathutils.Euler((0, 0, -math.pi+tmp_angle), 'XYZ'))
            tmp_angle = single_angle * (index + 1) - single_angle / 2
            end_x, end_y = vertex_rotate_2d(0, -radius, 0, 0, -tmp_angle)
            left_locations.append([end_x, end_y, 0])
            left_rotations.append(mathutils.Euler((0, 0, math.pi-tmp_angle), 'XYZ'))

        location_list = right_locations + left_locations
        rotation_list = right_rotations + left_rotations
        return(location_list, rotation_list)

    def _create_symbol(self, context, is_8, gua_num):
        
        FUXI_GUA_8 = ['坤', '艮', '坎', '巽', '震', '离', '兑', '乾']
        FUXI_GUA_64 = [
            '坤', '剥', '比', '观', '豫', '晋', '萃', '否',
            '谦', '艮', '蹇', '渐', '小过', '旅', '咸', '遁',
            '师', '蒙', '坎', '涣', '解', '未济', '困', '讼',
            '升', '蛊', '井', '巽', '恒', '鼎', '大过', '姤',
            '复', '颐', '屯', '益', '震', '噬嗑', '随', '无妄',
            '明夷', '贲', '既济', '家人', '丰', '离', '革', '同人',
            '临', '损', '节', '中孚', '归妹', '睽', '兑', '履',
            '泰', '大畜', '需', '小畜', '大壮', '大有', '夬', '乾'
        ]

        verts, faces = [], []
        pref_name = '八卦符' if is_8 else '六十四卦符'
        bin_fmt = '{:03b}' if is_8 else '{:06b}'
        bin_str = bin_fmt.format(gua_num)
        for index, tmp_chr in enumerate(bin_str):
            is_yang = False if '0' == tmp_chr else True
            offset_h = index * (self.height + self.offset)
            offset_v = len(verts)
            tmp_verts, tmp_faces = self.__verts_yao(is_yang, offset_h, offset_v)
            verts += tmp_verts
            faces += tmp_faces

        gua_name = FUXI_GUA_8[gua_num] if is_8 else FUXI_GUA_64[gua_num]
        use_name = '{}_{:02d}_{}'.format(pref_name, gua_num, gua_name)
        obj = create_mesh_object(context, verts, [], faces, use_name)
        obj.name = obj.data.name = use_name
        return(obj)

    def _create_all_symbols(self, context, is_8, radius):
        
        obj_list = []
        symbol_cnt = 8 if is_8 else 64
        location_list, rotation_list = self.__calc_symbols_loc_rot(symbol_cnt, radius)
        for index in range(symbol_cnt):
            tmp_obj = self._create_symbol(context, is_8, index)
            # tmp_obj.show_name = True
            tmp_obj.location = location_list[index]
            tmp_obj.rotation_euler = rotation_list[index]
            obj_list.append(tmp_obj)
        col_name = '八卦符号' if is_8 else '六十四卦符号'
        objects2collection(context, obj_list, create_collection(context, col_name))
        bpy.ops.object.empty_add(type='CIRCLE', radius=radius+self.height*2, align='WORLD', location=(0, 0, 0), rotation=(math.pi/2, 0, 0))
        tmp_obj = context.active_object
        tmp_obj.name = '空物体_' + col_name
        set_parent(obj_list, tmp_obj)
        objects2collection(context, [tmp_obj], context.collection)
        return(obj_list)

class YiJingGua8Symbol(YiJingGuaSymbol):
    
    def __init__(self, base_size=2):
        super().__init__()
        self.base_size = base_size
        self.width_yang = self.base_size
        self.width_yin = self.width_yang * (1 - self.golden_ratio)
        self.height = self.offset = self.base_size / 5

    def create_symbol(self, context, gua_num):
        return(super()._create_symbol(context, True, gua_num))

    def create_all_symbols(self, context, radius):
        return(super()._create_all_symbols(context, True, radius))

class YiJingGua64Symbol(YiJingGuaSymbol):
    
    def __init__(self, base_size=2):
        super().__init__()
        self.base_size = base_size
        self.width_yang = self.base_size * self.golden_ratio
        self.width_yin = self.width_yang * (1 - self.golden_ratio)
        self.height = self.offset = self.base_size / 11

    def create_symbol(self, context, gua_num):
        return(super()._create_symbol(context, False, gua_num))

    def create_all_symbols(self, context, radius):
        return(super()._create_all_symbols(context, False, radius))

if '__main__' == __name__:
    context = bpy.context

    YiJingGua8Symbol = YiJingGua8Symbol()
    tmp_obj = YiJingGua8Symbol.create_symbol(context, 0)
    # tmp_objs = YiJingGua8Symbol.create_all_symbols(context, 4)

    '''
    YiJingGua64Symbol = YiJingGua64Symbol()
    tmp_obj = YiJingGua64Symbol.create_symbol(context, 0)
    tmp_objs = YiJingGua64Symbol.create_all_symbols(context, radius=27)
    '''

    '''
    for tmp_obj in tmp_objs:
        tmp_mod = tmp_obj.modifiers.new('实体化', 'SOLIDIFY')
        tmp_mod.offset = 0
        tmp_mod.thickness = 0.1
    '''
