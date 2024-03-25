import os
import threading

import pymysql

from Package.space_group_cubic import match_space_group_cubic
from Package import real_space_parameters, match_plane_group
from Package.space_group_monoclinic_orthorhombic import match_space_group_monoclinic_orthorhombic
from Package.space_group_tetragonal import match_space_group_tetragonal
from Package.space_group_trigonal_hexagonal import match_space_group_trigonal_hexagonal
from Package.using_special_conditions import determine_using_other_conditions
from Package.calculate_mask import calculate_mask

lattice = ""
space_group_id = None


def get_space_group_result():
    return lattice, space_group_id


def show_space_group():
    threading.Thread(target=show_space_group_result).start()


def show_space_group_result():
    os.system(os.getcwd() + "\\ResultText\\MatchSpaceGroupResult.txt")


def __mask_equal_none(mask):
    raise ValueError("%s is/are None" % mask)


def __main_error():
    raise ValueError("Offered info is not enough to determine space group.")


def para_match(window, load_lattice, real_space_params_in=None, symmetry_in=None,
               directions_in=None, reciprocal_params_in=None):
    """
    匹配空间群
    :param load_lattice: 晶系
    :param real_space_params_in: 导入的实空间晶格参数
    :param reciprocal_params_in: 导入的倒易空间参数
    :param directions_in: 导入的特征方向
    :param symmetry_in: 导入的对称性信息
    :param window: 主窗口
    :return: 空间群对应的id
    """
    # 该函数先使用晶系、二维平面信息和mask确定空间群，若空间群数量不止一个则利用特殊条件确定
    window.start_label.config(text="Start To Determine Space Group")
    global lattice
    if real_space_params_in is not None:
        lattice = [real_space_params_in[0].lower()]
        r_s_para = [real_space_params_in[0].lower(), real_space_params_in[1],
                    real_space_params_in[2], real_space_params_in[3]]
        bravais = real_space_params_in[4]
        reciprocal_para = reciprocal_params_in
        directions = directions_in
        symmetry = symmetry_in
    else:
        bravais = real_space_parameters.get_real_space_parameter()[4]
        if bravais is None:
            bravais = match_plane_group.get_match_plane_group_result()[4]
        lattice = [real_space_parameters.get_real_space_parameter()[0]]
        if lattice[0] is None:
            lattice = [load_lattice]
        if len(lattice) != 1:
            raise ValueError("Need a lattice type, given %s" % len(lattice))
        symmetry = match_plane_group.get_match_plane_group_result()[0]
        if len(symmetry) > 3 or len(symmetry) < 1:
            raise ValueError("Plane groups are not satisfied, given %s" % len(symmetry))
        directions = match_plane_group.get_match_plane_group_result()[1]
        if len(directions) > 3 or len(directions) < 1:
            raise ValueError("Directions are not satisfied, given %s" % len(directions))
        r_s_para = real_space_parameters.get_real_space_parameter()
        if len(r_s_para) != 4:
            raise ValueError("Need 4 Real space parameters, given %s" % len(r_s_para))
        reciprocal_para = match_plane_group.get_match_plane_group_result()[2]
    all_mask = calculate_mask(r_s_para, reciprocal_para, directions)
    mask001, mask100, mask010 = all_mask[0], all_mask[1], all_mask[2]
    mask110, mask210, mask111 = all_mask[3], all_mask[4], all_mask[5]
    print(all_mask)
    connect = pymysql.connect(host='localhost', user='root', password='123456',
                              database='mybase', charset='utf8')
    cursor = connect.cursor()
    global space_group_id
    if lattice[0] == 'triclinic':
        sql = "select id from triclinic where sg001=%s and name=%s"
        cursor.execute(sql, (symmetry[0], bravais))
        space_group_id = cursor.fetchall()
        space_group_path = open("ResultText\\MatchSpaceGroupResult.txt", "w+")
        space_group_path.write("lattice " + str(lattice[0])
                               + "\n" + "id " + str(space_group_id[0][0]))
        space_group_path.close()
        window.end_label.config(text="Finish To Determine Plane Group")
        cursor.close()
        connect.close()
        return lattice, space_group_id
    if lattice[0] == 'cubic':
        space_group_id = match_space_group_cubic(mask001, mask111, mask110, directions, symmetry, bravais)
    if lattice[0] == 'trigonal' or lattice[0] == 'hexagonal':
        space_group_id = match_space_group_trigonal_hexagonal(mask001, mask100, mask210,
                                                              directions, symmetry, bravais, lattice)
    if lattice[0] == 'monoclinic' or lattice[0] == 'orthorhombic':
        space_group_id = match_space_group_monoclinic_orthorhombic(mask001, mask100, mask010,
                                                                   directions, symmetry, bravais, lattice)
    if lattice[0] == 'tetragonal':
        space_group_id = match_space_group_tetragonal(mask001, mask100, mask010,
                                                      directions, symmetry, bravais, lattice)
    cursor.close()
    connect.close()
    if len(space_group_id) < 1:
        __main_error()
    if len(space_group_id) > 1:
        space_group_id = determine_using_other_conditions(space_group_id, directions)
    space_group_path = open("ResultText\\MatchSpaceGroupResult.txt", "w+")
    space_group_path.write("lattice " + str(lattice[0]) + "\n" + "id " + str(space_group_id[0][0]))
    space_group_path.close()
    window.end_label.config(text="Finish To Determine Plane Group")
    return lattice, space_group_id
