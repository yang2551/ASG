# coding = UTF-8

import numpy

from Package import real_space_parameters, match_plane_group

origin_at_result = []
correspond_directions = []
bravais = None


def get_origin_at():
    return origin_at_result


def length_calculate(vector_one, vector_two, heart):
    """
    计算两个向量的长度和夹角
    :param vector_one: 向量一
    :param vector_two: 向量二
    :param heart: 中心位置
    :return: 长度差异length_diff; 角度degrees
    """
    length_diff = numpy.sqrt(numpy.square(vector_one[0] - vector_two[0]) + numpy.square(vector_one[1] - vector_two[1]))
    length_fc_x = vector_one[0] - heart[0]
    length_fc_y = vector_one[1] - heart[1]
    length_sc_x = vector_two[0] - heart[0]
    length_sc_y = vector_two[1] - heart[1]
    para_a = numpy.sqrt(numpy.square(length_fc_x) + numpy.square(length_fc_y))
    para_b = numpy.sqrt(numpy.square(length_sc_x) + numpy.square(length_sc_y))
    degrees = numpy.degrees(numpy.arccos(
        numpy.dot(vector_one - heart, vector_two - heart) / (para_a * para_b)))
    return length_diff, degrees


def origin_at(lattice, positions, relate_moment, direction, four_points, total_length,
              error, positions_in_range, number_of_atom, shape):
    """
    计算origin_at
    :param lattice: 晶系
    :param positions: 原子位置
    :param relate_moment: 振幅
    :param direction: 特征方向
    :param four_points: 顶点
    :param total_length: first-center; second-center间距离
    :param error: 误差
    :param positions_in_range: 惯用胞范围内的原子
    :param number_of_atom: 惯用胞范围内的原子序号
    :param shape: 图像大小，用于计算时判断计算过程中的位置是否超出图像范围
    :return: 起始位置 origin_at
    """
    # 按方向保存，如 [001]--["0,0,z"]
    # 有循环的地方需要判断是否超出图像的界限shape，超出界限则直接跳出循环
    image_height = shape[0]
    image_width = shape[1]
    global bravais
    bravais = real_space_parameters.get_real_space_parameter()[4]
    if bravais is None:
        bravais = match_plane_group.get_match_plane_group_result()[4]
    global origin_at_result, correspond_directions
    if lattice[0] == "orthorhombic":
        # 该晶系唯一需要origin_at判断的组合:[23,24,71]；单胞整体右移1/2, 24矩形中心维持有原子, 23和71则没有
        positions_after_moving = [[four_points[0][0] + 0.5 * total_length[2], four_points[0][1]],
                                  [four_points[1][0] + 0.5 * total_length[2], four_points[1][1]],
                                  [four_points[2][0] + 0.5 * total_length[2], four_points[2][1]],
                                  [four_points[3][0] + 0.5 * total_length[2], four_points[3][1]]]
        heart = [(positions_after_moving[0][0] + positions_after_moving[3][0]) / 2,
                 (positions_after_moving[0][1] + positions_after_moving[3][1]) / 2]
        for i in range(positions.shape[0]):
            if abs(heart[0] - positions[i][0]) <= error and abs(heart[1] - positions[i][1]) <= error:
                if direction == "001":
                    origin_at_result.append(["1/4,0,z"])
                    correspond_directions.append(["001"])
                if direction == "100":
                    origin_at_result.append(["x,1/4,0"])
                    correspond_directions.append(["100"])
                if direction == "010":
                    origin_at_result.append(["0,y,1/4"])
                    correspond_directions.append(["010"])
            else:
                if direction == "001":
                    origin_at_result.append(["0,0,z"])
                    correspond_directions.append(["001"])
                if direction == "100":
                    origin_at_result.append(["x,0,0"])
                    correspond_directions.append(["100"])
                if direction == "010":
                    origin_at_result.append(["0,y,0"])
                    correspond_directions.append(["010"])
    if lattice[0] == "tetragonal":
        """需要判断的组合：[79,80,82]、[85,86]、[90,94]、[91,95]、[92,96]、[89,93,123]、[97,98,139]；
        [001]方向上：
            [0.25,0.25,z]位置处存在四次轴，则origin_at为[1/4,1/4,z]；
            [0.25,0.25,z]位置处不存在四次轴，在中心存在四次轴则origin_at为[0,0,z]，存在二次轴[0,1/2,z]
        [100]方向上：
            二次轴存在的位置则为origin_at：bc, ef为一组
            a:[x,0,0] default
            b:[x,1/4,0]
            c:[x,1/4,1/4]
            d:[x,0,1/4]
            e:[x,1/4,1/8]
            f:[x,1/4,3/8]
            g:[x,0,3/8]
        [110]方向上：
            二次轴存在的位置则为origin_at：ce为一组
            a:[x,x,0] default
            b:[x,x,1/4]
            c:[x,x,1/8]
            e:[x,x,3/8]
        """
        if direction == "001":
            exact_position = [four_points[0][0] + 0.25 * total_length[2],
                              four_points[0][1] - 0.25 * total_length[1]]
            heart = [(four_points[0][0] + four_points[3][0]) / 2,
                     (four_points[0][1] + four_points[3][1]) / 2]
            length_exact_heart = [abs(exact_position[0] - heart[0]),
                                  abs(exact_position[1] - heart[1])]
            flag = 0
            for i in range(positions.shape[0]):
                if abs(heart[0] - 2 * length_exact_heart[0] - positions[i][0]) < error and abs(
                        heart[0] - positions[i][1]) < error:
                    flag = 1
                if abs(heart[0] - positions[i][0]) < error and abs(
                        heart[1] - 2 * length_exact_heart[1] - positions[i][1]) < error:
                    flag = 2
            if flag == 2:
                origin_at_result.append(["1/4,1/4,z"])
            else:
                left_top = []
                right_top = []
                index_left_top, index_right_top = None, None
                for i in positions_in_range:
                    if i[0] <= heart[0] and i[1] <= heart[1]:
                        left_top = numpy.array([i[0], i[1]])
                        index_left_top = number_of_atom[positions_in_range.index(i)]
                    if i[0] >= heart[0] and i[1] <= heart[1]:
                        right_top = numpy.array([i[0], i[1]])
                        index_right_top = number_of_atom[positions_in_range.index(i)]
                    length_diff, degrees = length_calculate(left_top, right_top, heart)
                    if abs(length_diff) <= error and abs(degrees - 90) <= error:
                        if abs(relate_moment[index_left_top] - relate_moment[index_right_top]) <= error + 50:
                            origin_at_result.append(["0,1/2,z"])
                        else:
                            origin_at_result.append(["0,0,z"])
                    else:
                        origin_at_result.append(["0,0,z"])
        if direction == "100":
            position_b = [four_points[0][0], four_points[0][1] - 0.25 * total_length[1]]
            position_d = [four_points[0][0] + 0.25 * total_length[2], four_points[0][1]]
            position_f = [four_points[0][0] + 3 / 8 * total_length[2], four_points[0][1] - 0.25 * total_length[1]]
            position_g = [four_points[0][0] + 3 / 8 * total_length[2], four_points[0][1]]
            for i in positions:
                for j in positions:
                    if abs(i[0] - j[0] + 2 * abs(i[0] - position_b[0])) > image_width or abs(
                            i[1] + 2 * abs(position_b[1] - i[1]) - j[1]) > image_height:
                        break
                    else:
                        if abs(i[0] - j[0] + 2 * abs(i[0] - position_b[0])) <= error and abs(
                                i[1] + 2 * abs(position_b[1] - i[1]) - j[1]) <= error:
                            index_b = positions.index(i)
                            index_match_b = positions.index(j)
                            if abs(relate_moment[index_match_b] - relate_moment[index_b]) <= error + 50:
                                if ["x,1/4,0"] not in origin_at_result:
                                    origin_at_result.append(["x,1/4,0"])
                            else:
                                if ["x,1/4,1/4"] not in origin_at_result:
                                    origin_at_result.append(["x,1/4,1/4"])
                        else:
                            if ["x,1/4,1/4"] not in origin_at_result:
                                origin_at_result.append(["x,1/4,1/4"])
            for i in positions:
                for j in positions:
                    if abs(i[0] + 2 * abs(i[0] - position_d[0]) - j[0]) > image_width or abs(
                            i[1] + 2 * abs(i[1] - position_d[1]) - j[1]) > image_height:
                        break
                    else:
                        if abs(i[0] + 2 * abs(i[0] - position_d[0]) - j[0]) <= error and abs(
                                i[1] + 2 * abs(i[1] - position_d[1]) - j[1]) <= error:
                            index_d = positions.index(i)
                            index_match_d = positions.index(j)
                            if abs(relate_moment[index_match_d] - relate_moment[index_d]) <= error + 50:
                                if ["x,0,1/4"] not in origin_at_result:
                                    origin_at_result.append(["x,0,1/4"])
                            else:
                                if ["x,0,0"] not in origin_at_result:
                                    origin_at_result.append(["x,0,0"])
                        else:
                            if ["x,0,0"] not in origin_at_result:
                                origin_at_result.append(["x,0,0"])
            for i in positions:
                for j in positions:
                    if abs(2 * abs(i[0] - position_f[0]) - j[0] + i[0]) > image_width or abs(
                            i[1] + 2 * abs(i[1] - position_f[1]) - j[1]) > image_height:
                        break
                    else:
                        if abs(2 * abs(i[0] - position_f[0]) - j[0] + i[0]) <= error and abs(
                                i[1] + 2 * abs(i[1] - position_f[1]) - j[1]) <= error:
                            index_f = positions.index(i)
                            index_match_f = positions.index(j)
                            if abs(relate_moment[index_match_f] - relate_moment[index_f]) <= error + 50:
                                if ["x,1/4,3/8"] not in origin_at_result:
                                    origin_at_result.append(["x,1/4,3/8"])
                            else:
                                if ["x,1/4,1/8"] not in origin_at_result:
                                    origin_at_result.append(["x,1/4,1/8"])
                        else:
                            if ["x,1/4,1/8"] not in origin_at_result:
                                origin_at_result.append(["x,1/4,1/8"])
            for i in positions:
                for j in positions:
                    if abs(i[0] + 2 * abs(i[0] - position_g[0]) - j[0]) > image_width or abs(
                            i[1] - j[1] + 2 * abs(i[1] - position_g[1])) > image_height:
                        break
                    else:
                        if abs(i[0] + 2 * abs(i[0] - position_g[0]) - j[0]) <= error and abs(
                                i[1] - j[1] + 2 * abs(i[1] - position_g[1])) <= error:
                            index_g = positions.index(i)
                            index_match_g = positions.index(j)
                            if abs(relate_moment[index_match_g] - relate_moment[index_g]) <= error + 50:
                                if ["x,0,3/8"] not in origin_at_result:
                                    origin_at_result.append(["x,0,3/8"])
                            else:
                                if ["x,0,0"] not in origin_at_result:
                                    origin_at_result.append(["x,0,0"])
                        else:
                            if ["x,0,0"] not in origin_at_result:
                                origin_at_result.append(["x,0,0"])
        if direction == "110":
            position_b = [four_points[0][0], four_points[0][1] - 0.25 * total_length[1]]
            position_c = [four_points[0][0], four_points[0][1] - 1 / 8 * total_length[1]]
            for i in positions:
                if ["x,x,0"] in origin_at_result:
                    break
                for j in positions:
                    if abs(i[0] + 2 * (position_b[0] - i[0]) - j[0]) <= error and abs(
                            i[1] + 2 * (position_b[1] - i[1]) - j[1]) <= error:
                        index_b = positions.index(i)
                        index_match_b = positions.index(j)
                        if abs(relate_moment[index_match_b] - relate_moment[index_b]) <= error + 50:
                            if ["x,x,1/4"] not in origin_at_result:
                                origin_at_result.append(["x,x,1/4"])
                        else:
                            if ["x,x,0"] not in origin_at_result:
                                origin_at_result.append(["x,x,0"])
                    else:
                        if ["x,x,0"] not in origin_at_result:
                            origin_at_result.append(["x,x,0"])
            for i in positions:
                if ["x,x,1/8"] in origin_at_result:
                    break
                for j in positions:
                    if abs(i[0] - j[0] + 2 * (position_c[0] - i[0])) > image_width or abs(
                            i[1] + 2 * (position_c[1] - i[1]) - j[1]) > image_height:
                        break
                    else:
                        if abs(i[0] - j[0] + 2 * (position_c[0] - i[0])) <= error and abs(
                                i[1] + 2 * (position_c[1] - i[1]) - j[1]) <= error:
                            index_c = positions.index(i)
                            index_match_c = positions.index(j)
                            if abs(relate_moment[index_match_c] - relate_moment[index_c]) <= error + 50:
                                if ["x,x,3/8"] not in origin_at_result:
                                    origin_at_result.append(["x,x,3/8"])
                            else:
                                if ["x,x,1/8"] not in origin_at_result:
                                    origin_at_result.append(["x,x,1/8"])
                        else:
                            if ["x,x,1/8"] not in origin_at_result:
                                origin_at_result.append(["x,x,1/8"])
    if lattice[0] == "trigonal":
        """
        需要判断的组合：[150,152,154]、[149,151,153]
        [001]方向: 无需判断,六个空间群一致
        [100]方向:仅使用该方向就可全部判断六个空间群
            a:["x,0,0"] default
            b:["x,0,1/6"], c:["x,0,1/3"]
        [210]方向：该方向的origin_at非必须
        """
        if direction == "100":
            position_b = [four_points[0][0], four_points[0][1] + 1 / 3 * total_length[2]]
            position_c = [four_points[0][0], four_points[0][1] + 2 / 3 * total_length[2]]
            for i in positions:
                if ["x,0,0"] in origin_at_result:
                    break
                for j in positions:
                    if abs(i[0] - j[0] + 2 * (position_b[0] - i[0])) > image_width or abs(
                            i[1] - j[1] + 2 * (position_b[1] - i[1])) > image_height:
                        break
                    elif abs(i[0] + 2 * (position_c[0] - i[0]) - j[0]) > image_width or abs(
                            i[1] - j[1] + 2 * (position_c[1] - i[1])) > image_height:
                        break
                    else:
                        if abs(i[1] + 2 * (position_b[1] - i[1]) - j[1]) <= error and abs(
                                i[0] + 2 * (position_b[0] - i[0]) - j[0]) <= error:
                            index_b = positions.index(i)
                            index_match_b = positions.index(j)
                            if abs(relate_moment[index_match_b] - relate_moment[index_b]) <= error + 50:
                                if ["x,0,1/6"] not in origin_at_result:
                                    origin_at_result.append(["x,0,1/6"])
                            else:
                                if ["x,0,0"] not in origin_at_result:
                                    origin_at_result.append(["x,0,0"])
                        elif abs(i[1] + 2 * (position_c[1] - i[1]) - j[1]) <= error and abs(
                                i[0] - j[0] + 2 * (position_c[0] - i[0])) <= error:
                            index_c = positions.index(i)
                            index_match_c = positions.index(j)
                            if abs(relate_moment[index_match_c] - relate_moment[index_c]) <= error + 50:
                                if ["x,0,1/3"] not in origin_at_result:
                                    origin_at_result.append(["x,0,1/3"])
                            else:
                                if ["x,0,0"] not in origin_at_result:
                                    origin_at_result.append(["x,0,0"])
    if lattice[0] == "hexagonal":
        """
        需要判断的组合：[177,180,181]、[178,179,182]
        [001]和[100]都一致
        [210]方向：
            ["x,1/2x,0"] default, a:["x,1/2x,1/6"],  b:["x,1/2x,1/3"], 
            c:["x,1/2x,1/12"], default:["x,1/2x,5/12"], d:["x,1/2x,1/4"]
        """
        if direction == "210":
            position_a = [four_points[0][0] + 5 / 6 * total_length[2], four_points[0][1]]
            position_b = [four_points[0][0] + 2 / 3 * total_length[2], four_points[0][1]]
            for i in positions:
                if ["x,1/2x,0"] in origin_at_result:
                    break
                for j in positions:
                    if abs(i[0] - j[0] + 2 * (position_a[0] - i[0])) < image_width and abs(
                            i[1] - j[1] + 2 * (position_a[1] - i[1])) < image_height:
                        if abs(i[1] + 2 * (position_a[1] - i[1]) - j[1]) > error or abs(
                                i[0] + 2 * (position_a[0] - i[0]) - j[0]) > error:
                            if ["x,1/2x,0"] not in origin_at_result:
                                origin_at_result.append(["x,1/2x,0"])
                        else:
                            index_b = positions.index(i)
                            index_match_b = positions.index(j)
                            if abs(relate_moment[index_match_b] - relate_moment[index_b]) <= error + 50:
                                if ["x,1/2x,1/6"] not in origin_at_result:
                                    origin_at_result.append(["x,1/2x,1/6"])
                    elif abs(i[0] - j[0] + 2 * (position_b[0] - i[0])) < image_width and abs(
                            i[1] - j[1] + 2 * (position_b[1] - i[1])) < image_height:
                        if abs(i[1] + 2 * (position_b[1] - i[1]) - j[1]) > error or abs(
                                i[0] + 2 * (position_b[0] - i[0]) - j[0]) > error:
                            if ["x,1/2x,0"] not in origin_at_result:
                                origin_at_result.append(["x,1/2x,0"])
                        else:
                            index_c = positions.index(i)
                            index_match_c = positions.index(j)
                            if abs(relate_moment[index_match_c] - relate_moment[index_c]) <= error + 50:
                                if ["x,1/2x,1/3"] not in origin_at_result:
                                    origin_at_result.append(["x,1/2x,1/3"])
                    else:
                        break
            position_c = [four_points[0][0] + 11 / 12 * total_length[2], four_points[0][1]]
            position_d = [four_points[0][0] + 1 / 4 * total_length[2], four_points[0][1]]
            for i in positions:
                if ["x,1/2x,5/12"] in origin_at_result:
                    break
                for j in positions:
                    if abs(i[0] - j[0] + 2 * (position_c[0] - i[0])) < image_width and abs(
                            i[1] - j[1] + 2 * (position_c[1] - i[1])) < image_height:
                        if abs(i[1] + 2 * (position_c[1] - i[1]) - j[1]) > error or abs(
                                i[0] + 2 * (position_c[0] - i[0]) - j[0]) > error:
                            if ["x,1/2x,5/12"] not in origin_at_result:
                                origin_at_result.append(["x,1/2x,5/12"])
                        else:
                            index_c = positions.index(i)
                            index_match_c = positions.index(j)
                            if abs(relate_moment[index_match_c] - relate_moment[index_c]) <= error + 50:
                                if ["x,1/2x,1/12"] not in origin_at_result:
                                    origin_at_result.append(["x,1/2x,1/12"])
                    elif abs(i[0] - j[0] + 2 * (position_d[0] - i[0])) < image_width and abs(
                            i[1] - j[1] + 2 * (position_d[1] - i[1])) < image_height:
                        if abs(i[1] + 2 * (position_d[1] - i[1]) - j[1]) > error or abs(
                                i[0] + 2 * (position_d[0] - i[0]) - j[0]) > error:
                            if ["x,1/2x,5/12"] not in origin_at_result:
                                origin_at_result.append(["x,1/2x,5/12"])
                        else:
                            index_d = positions.index(i)
                            index_match_d = positions.index(j)
                            if abs(relate_moment[index_match_d] - relate_moment[index_d]) <= error + 50:
                                if ["x,1/2x,1/4"] not in origin_at_result:
                                    origin_at_result.append(["x,1/2x,1/4"])
                    else:
                        break
    if lattice[0] == "cubic":
        """
        需要判断的组合：[197,199]、[207,208]、[209,210]、[211,214]、[212,213]
        [001]方向:单个方向的origin_at信息即可区分
            ["0,0,z"] default
            ["1/4,0,z"]
            ["0,1/2,z"]
            ["1/4,1/2,z"]
        """
        if direction == "001":
            if bravais == "i":
                # 中心点上方1/4处存在二次轴则为["1/4,0,z"]，否则为["0,0,z"]
                position_i = [four_points[0][0] + total_length[0], four_points[0][0] - 1 / 4 * total_length[1]]
                for i in positions:
                    if ["0,0,z"] in origin_at_result or ["1/4,0,z"] in origin_at_result:
                        break
                    for j in positions:
                        if abs(i[0] - j[0] + 2 * (position_i[0] - i[0])) > image_width or abs(
                                i[1] - j[1] + 2 * (position_i[1] - i[1])) > image_height:
                            break
                        else:
                            if abs(i[1] + 2 * (position_i[1] - i[1]) - j[1]) <= error and abs(
                                    i[0] + 2 * (position_i[0] - i[0]) - j[0]) <= error:
                                index_i = positions.index(i)
                                index_match_i = positions.index(j)
                                if abs(relate_moment[index_match_i] - relate_moment[index_i]) <= error + 50:
                                    if ["1/4,0,z"] not in origin_at_result:
                                        origin_at_result.append(["1/4,0,z"])
                                else:
                                    if ["0,0,z"] not in origin_at_result:
                                        origin_at_result.append(["0,0,z"])
            if bravais == "f":
                # 中心点上方1/4处存在四次轴则为["0,0,z"]，否则为["1/4,0,z"]
                position_i = [four_points[0][0] + total_length[0], four_points[0][0] - 1 / 4 * total_length[1]]
                for i in positions:
                    if ["0,0,z"] in origin_at_result or ["1/4,0,z"] in origin_at_result:
                        break
                    length_from_i_first = numpy.sqrt(
                        numpy.square(position_i[0] - i[0]) + numpy.square(position_i[1] - i[1]))
                    index_i = positions.index(i)
                    for j in positions:
                        if abs(i[0] - j[0] + 2 * (position_i[0] - i[0])) > image_width or abs(
                                i[1] - j[1] + 2 * (position_i[1] - i[1])) > image_height:
                            break
                        else:
                            length_from_i_second = numpy.sqrt(
                                numpy.square(position_i[0] - j[0]) + numpy.square(position_i[1] - j[1]))
                            index_j = positions.index(j)
                            degrees = numpy.degrees(numpy.arccos(numpy.dot(i - position_i, j - position_i) / (
                                    length_from_i_first * length_from_i_second)))
                            if abs(length_from_i_first - length_from_i_second) <= error:
                                if abs(relate_moment[index_i] - relate_moment[index_j]) <= error + 50:
                                    if abs(degrees - 90) <= error:
                                        if ["0,0,z"] not in origin_at_result:
                                            origin_at_result.append(["0,0,z"])
                                    else:
                                        if ["1/4,0,z"] not in origin_at_result:
                                            origin_at_result.append(["1/4,0,z"])
                                else:
                                    if ["1/4,0,z"] not in origin_at_result:
                                        origin_at_result.append(["1/4,0,z"])
                            else:
                                break
                if len(origin_at_result) == 0:
                    origin_at_result.append(["0,0,z"])
            if bravais == "p":
                # 中心点上方1/2处存在四次轴则为["0,1/2,z"]，否则为["0,0,z"] -- position_first
                position_first = [four_points[0][0] + total_length[0], four_points[0][0] - 1 / 2 * total_length[1]]
                for i in positions:
                    if ["0,1/2,z"] in origin_at_result or ["0,0,z"] in origin_at_result:
                        break
                    length_i_first = numpy.sqrt(
                        numpy.square(position_first[0] - i[0]) + numpy.square(position_first[1] - i[1]))
                    index_i = positions.index(i)
                    for j in positions:
                        if abs(i[0] - j[0] + 2 * (position_first[0] - i[0])) > image_width or abs(
                                i[1] - j[1] + 2 * (position_first[1] - i[1])) > image_height:
                            break
                        else:
                            length_i_second = numpy.sqrt(
                                numpy.square(position_first[1] - j[1]) + numpy.square(position_first[0] - j[0]))
                            index_j = positions.index(j)
                            degrees = numpy.degrees(numpy.arccos(
                                numpy.dot(i - position_first, j - position_first) / (length_i_first * length_i_second)))
                            if abs(length_i_first - length_i_second) <= error:
                                if abs(relate_moment[index_i] - relate_moment[index_j]) <= error + 50:
                                    if abs(degrees - 90) <= error:
                                        if ["0,1/2,z"] not in origin_at_result:
                                            origin_at_result.append(["0,1/2,z"])
                                    else:
                                        if ["0,0,z"] not in origin_at_result:
                                            origin_at_result.append(["0,0,z"])
                                else:
                                    if ["0,0,z"] not in origin_at_result:
                                        origin_at_result.append(["0,0,z"])
                            else:
                                break
                if len(origin_at_result) == 0:
                    origin_at_result.append(["0,0,z"])
                # 中心点右侧1/4处存在四次轴则为["1/4,0,z"]，否则为["1/4,1/2,z"]  -- position_second
                position_second = [four_points[0][0] + 1 / 4 * total_length[0], four_points[0][0] - total_length[1]]
                for i in positions:
                    if ["1/4,0,z"] in origin_at_result or ["1/4,1/2,z"] in origin_at_result:
                        break
                    length_i_first = numpy.sqrt(
                        numpy.square(position_second[0] - i[0]) + numpy.square(position_second[1] - i[1]))
                    index_i = positions.index(i)
                    for j in positions:
                        if abs(i[0] - j[0] + 2 * (position_second[0] - i[0])) > image_width or abs(
                                i[1] - j[1] + 2 * (position_second[1] - i[1])) > image_height:
                            break
                        else:
                            length_i_second = numpy.sqrt(
                                numpy.square(position_second[1] - j[1]) + numpy.square(position_second[0] - j[0]))
                            degrees = numpy.degrees(numpy.arccos(
                                numpy.dot(i - position_second, j - position_second) / (
                                        length_i_first * length_i_second)))
                            index_j = positions.index(j)
                            if abs(length_i_first - length_i_second) <= error:
                                if abs(relate_moment[index_i] - relate_moment[index_j]) <= error + 50:
                                    if abs(degrees - 90) <= error:
                                        if ["1/4,0,z"] not in origin_at_result:
                                            origin_at_result.append(["1/4,0,z"])
                                    else:
                                        if ["1/4,1/2,z"] not in origin_at_result:
                                            origin_at_result.append(["1/4,1/2,z"])
                                else:
                                    if ["1/4,1/2,z"] not in origin_at_result:
                                        origin_at_result.append(["1/4,1/2,z"])
                            else:
                                break
                if len(origin_at_result) == 0:
                    origin_at_result.append(["1/4,1/2,z"])
    return origin_at_result
