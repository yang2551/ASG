# coding = UTF-8

from Package import real_space_parameters, match_plane_group, side_functions

"""
orthorhombic: [16,47] [21,65] [22,69] [23,71]
tetragonal: [89,123] [97,139]
trigonal: general_position = 3
"""

general_position = None
lattice, bravais = None, None


def get_general_position():
    return general_position


def calculate_general_position(real_lattice, four_points, direction, error):
    """
    该函数用于计算一般位置
    :param real_lattice: 晶系
    :param four_points: 所选顶点位置
    :param direction: 特征方向
    :param error: 误差
    :return: 一般位置 general_position
    """
    global lattice, bravais, general_position
    lattice = real_space_parameters.get_real_space_parameter()[0]
    if lattice is None:
        lattice = real_lattice
    bravais = real_space_parameters.get_real_space_parameter()[4]
    if bravais is None:
        bravais = match_plane_group.get_match_plane_group_result()[4]
    refine_positions, moments = side_functions.get_refine_peaks()
    center_position = [(four_points[0][0] + four_points[3][0]) / 2,
                       (four_points[0][1] + four_points[3][0]) / 2]
    max_x = max(four_points[0][0], center_position[0])
    min_x = min(four_points[0][0], center_position[0])
    max_y = max(four_points[0][1], center_position[1])
    min_y = max(four_points[0][1], center_position[1])
    if lattice == "orthorhombic":
        flag = False
        # 检验在单胞选取过程中的中心点到单胞中心区域内是否有原子判断一般位置
        for i in refine_positions:
            if i[0] in range(min_x + 0.5, max_x - 0.5) and i[1] in range(min_y + 0.5, max_y - 0.5):
                flag = True
        if bravais == "p":
            if flag is True:
                general_position = 4
            else:
                general_position = 8
        if bravais == "c":
            if flag is True:
                general_position = 8
            else:
                general_position = 16
        if bravais == "f":
            if flag is True:
                general_position = 16
            else:
                general_position = 32
        if bravais == "i":
            if flag is True:
                general_position = 8
            else:
                general_position = 16
    # 取[110]方向，单胞中心存在原子则为123，否则为89
    if lattice == "tetragonal":
        flag = False
        if direction == "110":
            for i in refine_positions:
                if abs(i[0] - center_position[0]) <= error and abs(i[1] - center_position[0]) <= error:
                    flag = True
            if bravais == "p":
                if flag is True:
                    general_position = 16
                else:
                    general_position = 8
            if bravais == "i":
                if flag is True:
                    general_position = 16
                else:
                    general_position = 32
        if bravais == "i":
            if direction == "001":
                for i in refine_positions:
                    if i[0] in range(min_x + 0.5, max_x - 0.5) and i[1] in range(min_y + 0.5, max_y - 0.5):
                        flag = True
                if flag is True:
                    general_position = 16
                else:
                    general_position = 32
    if lattice == "trigonal":
        general_position = 3
    return general_position
