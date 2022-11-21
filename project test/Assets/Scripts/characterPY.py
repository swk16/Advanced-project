# -*- coding: utf-8 -*-

import bpy, math, mathutils

def vertex_rotate_2d(start_x, start_y, center_x, center_y, angle):
    end_x = math.cos(angle) * (start_x - center_x) - math.sin(angle) * (start_y - center_y) + center_x
    end_y = math.sin(angle) * (start_x - center_x) + math.cos(angle) * (start_y - center_y) + center_y
    return(end_x, end_y)

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

def create_text_object(context, name, text, font, size, extrude):
    font_curve = bpy.data.curves.new(type='FONT', name=name)
    font_curve.body = text
    obj = bpy.data.objects.new(name, font_curve)
    obj.data.align_x = 'CENTER'
    obj.data.align_y = 'BOTTOM'
    obj.data.font = font
    obj.data.size = size
    obj.data.extrude = extrude
    return(obj)

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

def circle_text_from_list(context, radius, use_list, prefix, font, size, extrude):
    obj_list = []
    symbol_cnt = len(use_list)
    location_list, rotation_list = calc_circle_symbols_loc_rot(symbol_cnt, radius)
    for index, tmp_text in enumerate(use_list):
        if '' == tmp_text:
            continue
        tmp_obj = create_text_object(context, '{}_{}'.format(prefix, tmp_text), tmp_text, font, size, extrude)
        # tmp_obj.show_name = True
        tmp_obj.location = location_list[index]
        tmp_obj.rotation_euler = rotation_list[index]
        obj_list.append(tmp_obj)
    return(obj_list)

def func_circle_text_from_list(context, text_list, list_name, radius, font, font_size, font_extrude):
    obj_list = circle_text_from_list(context, radius, text_list, list_name, font, font_size, font_extrude)
    objects2collection(context, obj_list, create_collection(context, list_name))
    bpy.ops.object.empty_add(type='CIRCLE', radius=radius+font_size/2, align='WORLD', location=(0, 0, 0), rotation=(math.pi/2, 0, 0))
    tmp_obj = context.active_object
    tmp_obj.name = '空物体_' + list_name
    set_parent(obj_list, tmp_obj)
    objects2collection(context, [tmp_obj], context.collection)

if '__main__' == __name__:
    context = bpy.context
    font_data = bpy.data.fonts.load('C:\\Windows\\Fonts\\Alibaba-PuHuiTi-Regular.otf')

    XIANTIAN_GUA_8 = ['坤', '震', '离', '兑', '乾', '巽', '坎', '艮']
    func_circle_text_from_list(context, XIANTIAN_GUA_8, '先天八卦', 6, font_data, 2, 0.01)

    SOLAR_TERMS_24 = [
        '冬至', '小寒', '大寒', '立春', '雨水', '惊蛰', '春分', '清明', '谷雨', '立夏', '小满', '芒种',
        '夏至', '小暑', '大暑', '立秋', '处暑', '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪'
    ]
    func_circle_text_from_list(context, SOLAR_TERMS_24, '节气', 8, font_data, 1, 0.01)
