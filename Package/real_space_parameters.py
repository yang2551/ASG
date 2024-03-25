import os
import threading
import tkinter

import numpy

from Package import basic_vector_calculate
from Package import find_niggli_cell

real_a = None
real_b = None
real_c = None
real_alpha = None
real_beta = None
real_theta = None
real_lattice = None
bravais = None
reciprocal_lattice = None
pixels_length = []


def load_pixels_length_to_calculate(window, error, text_font, menu):
    """
    :param menu: 菜单
    :param text_font: 文本格式
    :param error: 误差容限
    :param window: 主界面
    :return:
    """
    self = tkinter.Toplevel()
    self.title('Loading Pixels & Length')
    self.geometry("%dx%d" % (650, 100))
    self.config(menu=menu)
    self.resizable(height=False, width=False)
    tkinter.Label(self, text="Pixels Length", font=text_font).place(x=20, y=10)
    self.pixels_to_length = tkinter.StringVar()
    pixels_to_length = tkinter.Entry(self, width=25)
    pixels_to_length.place(x=20, y=35, height=30)

    def __get_params():
        real_space_params_length = pixels_to_length.get().split(" ")
        for i in range(len(real_space_params_length)):
            pixels_length.append(int(real_space_params_length[i]))

    tkinter.Label(self, text="Separate each params by blank space!",
                  font=("Times New Roman", 10, "bold", "underline")).place(x=20, y=70)

    global pixels_length
    pixels_length = []

    tkinter.Button(self, text="Confirm", command=__get_params, width=7,
                   font=text_font).place(x=400, y=35, height=30)
    tkinter.Button(self, text="Continue", width=7,
                   command=lambda: real_space_parameters_calculate(window, error, pixels_length),
                   font=text_font).place(x=500, y=35, height=30)
    self.mainloop()
    self.destroy()


def get_real_space_parameter():
    # real_a = 4.506
    # real_b = 2.899
    # real_c = 4.617
    # real_lattice = "triclinic"
    # bravais = "p"
    return [real_lattice, real_a, real_b, real_c, bravais]


def show_parameters():
    threading.Thread(target=real_space_parameters_result).start()


def real_space_parameters_result():
    os.system(os.getcwd() + "\\ResultText\\RealSpaceParametersResult.txt")


def real_space_parameters_calculate(window, tol_r_err, pixel_length):
    threading.Thread(target=real_space_parameters_thread, args=(window, tol_r_err, pixel_length)).start()


# 计算实空间的晶格参数，用于single crystal模拟图像、实验图像或者HAADF像
def real_space_parameters_thread(window, tol_r_err, pixel_length):
    """
    实空间晶格参数计算
    :param window: 主窗口
    :param tol_r_err: 误差
    :param pixel_length: 相对和实际长度的对应关系
    :return: 实空间晶格参数
    """
    # 参考Fortran程序
    window.start_label.config(text="Start To Calculate Real Space Parameters")
    # pixel = float(input('Pixel'))
    # to_length = float(input('Length'))  # 写入标尺和像素的关系
    # load_basic_vec = numpy.loadtxt('ResultText/BasicVectorCalculateResult.txt')
    pixel = float(pixel_length[0])
    to_length = float(pixel_length[1])
    load_basic_vec = basic_vector_calculate.get_basic_vector()
    load_basic_vec = load_basic_vec / pixel * to_length
    print("load_basic_vectors", load_basic_vec)
    mo_0 = numpy.sqrt(numpy.square(load_basic_vec[0][0]) + numpy.square(load_basic_vec[0][1]))
    mo_1 = numpy.sqrt(numpy.square(load_basic_vec[1][0]) + numpy.square(load_basic_vec[1][1]))
    mo_2 = numpy.sqrt(numpy.square(load_basic_vec[2][0]) + numpy.square(load_basic_vec[2][1]))
    mo_3 = numpy.sqrt(numpy.square(load_basic_vec[3][0]) + numpy.square(load_basic_vec[3][1]))
    mo_4 = numpy.sqrt(numpy.square(load_basic_vec[4][0]) + numpy.square(load_basic_vec[4][1]))
    mo_5 = numpy.sqrt(numpy.square(load_basic_vec[5][0]) + numpy.square(load_basic_vec[5][1]))
    print("mo", mo_0, mo_1, mo_2, mo_3, mo_4, mo_5)
    cal_stack_mo = numpy.stack([mo_0, mo_1, mo_2, mo_3, mo_4, mo_5])
    # 每张照片基矢弧长
    archway_one = numpy.arccos(
        numpy.dot(load_basic_vec[0, :],
                  load_basic_vec[1, :]) / (mo_0 * mo_1))
    archway_two = numpy.arccos(
        numpy.dot(load_basic_vec[2, :],
                  load_basic_vec[3, :]) / (mo_2 * mo_3))
    archway_three = numpy.arccos(
        numpy.dot(load_basic_vec[4, :],
                  load_basic_vec[5, :]) / (mo_4 * mo_5))
    # 每张照片中两个矢量的角度
    angle_one_reci = numpy.degrees(archway_one)
    angle_two_reci = numpy.degrees(archway_two)
    angle_three_reci = numpy.degrees(archway_three)
    print("angle_between_vectors", angle_one_reci, angle_two_reci, angle_three_reci)
    confirm_c = [0, 1, 2, 3, 4, 5]
    empty_temp_mat = numpy.empty(shape=[0, 1])
    empty_normal_abc = numpy.empty(shape=[0, 1])
    if abs(cal_stack_mo[0] - cal_stack_mo[1]) <= tol_r_err and abs(
            cal_stack_mo[2] - cal_stack_mo[3]) <= tol_r_err and abs(
        cal_stack_mo[4] - cal_stack_mo[5] <= tol_r_err):  # 三基矢相等时使用
        empty_normal_abc = numpy.append(empty_normal_abc,
                                        (cal_stack_mo[0] + cal_stack_mo[1]) / 2)
        empty_normal_abc = numpy.append(empty_normal_abc,
                                        (cal_stack_mo[2] + cal_stack_mo[3]) / 2)
        empty_normal_abc = numpy.append(empty_normal_abc,
                                        (cal_stack_mo[4] + cal_stack_mo[5]) / 2)
    else:
        for row in range(0, cal_stack_mo.size):  # 三基矢不相等时自动判别
            if row != 0:
                match_mat_a = cal_stack_mo[0] - cal_stack_mo[row]
                if abs(match_mat_a) <= tol_r_err:
                    empty_normal_abc = numpy.append(empty_normal_abc,
                                                    (cal_stack_mo[0] + cal_stack_mo[row]) / 2)
                    empty_temp_mat = numpy.append(empty_temp_mat, 0)
                    empty_temp_mat = numpy.append(empty_temp_mat, row)
                    pass
            if row != 0 and row != 1:
                match_mat_b = cal_stack_mo[1] - cal_stack_mo[row]
                if abs(match_mat_b) <= tol_r_err:
                    empty_normal_abc = numpy.append(empty_normal_abc,
                                                    (cal_stack_mo[1] + cal_stack_mo[row]) / 2)
                    empty_temp_mat = numpy.append(empty_temp_mat, 1)
                    empty_temp_mat = numpy.append(empty_temp_mat, row)
        for element_e in empty_temp_mat:
            for element_f in confirm_c:
                if element_e == element_f:
                    confirm_c.remove(element_e)
        empty_normal_abc = numpy.append(empty_normal_abc,
                                        (cal_stack_mo[confirm_c[0]] +
                                         cal_stack_mo[confirm_c[1]]) / 2)
    # empty_normal_abc = [(mo_0 + mo_5) / 2, (mo_1 + mo_3) / 2, (mo_2 + mo_4) / 2]
    normal_b = 0
    for item in empty_normal_abc:
        if max(empty_normal_abc) > item > min(empty_normal_abc):
            normal_b = item
    normal_a = min(empty_normal_abc)
    normal_c = max(empty_normal_abc)
    mat_abc_00 = normal_a ** 2
    mat_abc_11 = normal_b ** 2
    mat_abc_22 = normal_c ** 2
    mat_abc_01 = normal_a * normal_b * numpy.cos(archway_three)
    mat_abc_02 = normal_a * normal_c * numpy.cos(archway_two)
    mat_abc_12 = normal_b * normal_c * numpy.cos(archway_one)
    mat_abc_10 = mat_abc_01
    mat_abc_20 = mat_abc_02
    mat_abc_21 = mat_abc_12
    mat_abc = numpy.array(([mat_abc_00, mat_abc_01, mat_abc_02],
                           [mat_abc_10, mat_abc_11, mat_abc_12],
                           [mat_abc_20, mat_abc_21, mat_abc_22]))  # 利用模长计算
    print("normal_abc", normal_a, normal_b, normal_c)
    cal_value_emp = numpy.empty(shape=[0, 1])
    i_emp = numpy.empty(shape=[0, 1])
    j_emp = numpy.empty(shape=[0, 1])
    k_emp = numpy.empty(shape=[0, 1])
    i_final = numpy.empty(shape=[0, 1])
    j_final = numpy.empty(shape=[0, 1])
    k_final = numpy.empty(shape=[0, 1])

    for i in range(-5, 6):
        for j in range(-5, 6):
            for k in range(-5, 6):
                value = numpy.dot(numpy.dot([i, j, k], mat_abc),
                                  numpy.transpose([i, j, k]))
                if value != 0:
                    cal_value_emp = numpy.append(cal_value_emp, value)
                    i_emp = numpy.append(i_emp, i)
                    j_emp = numpy.append(j_emp, j)
                    k_emp = numpy.append(k_emp, k)

    unique_value, indices = numpy.unique(cal_value_emp, return_index=True)
    ijk = open('ResultText/ijk.txt', 'w+')
    for element_g in indices:
        i_final = numpy.append(i_final, i_emp[element_g])
        j_final = numpy.append(j_final, j_emp[element_g])
        k_final = numpy.append(k_final, k_emp[element_g])
        ijk.write(str(i_emp[element_g]))
        ijk.write(' ')
        ijk.write(str(j_emp[element_g]))
        ijk.write(' ')
        ijk.write(str(k_emp[element_g]))
        ijk.write(' ')
        ijk.write(str(cal_value_emp[element_g]))
        ijk.write('\n')
    ijk.close()

    ijk_stack = numpy.vstack((i_final, j_final, k_final))

    for element_h in range(1, i_final.size + 1):
        ijk_mat = numpy.stack((ijk_stack[:, 0], ijk_stack[:, 1], ijk_stack[:, element_h + 1]))
        if numpy.linalg.det(ijk_mat) != 0:
            print("ijk_mat", ijk_mat)
            # print('ijk[0]: ', i_final[0], j_final[0], k_final[0])
            # print('ijk[1]', i_final[1], j_final[1], k_final[1])
            # print('ijk[2]', i_final[element_h + 1], j_final[element_h + 1], k_final[element_h + 1])
            mat_for_cal = mat_abc
            ijk_mat_cal = ijk_mat
            v = numpy.empty(shape=[3, 3])
            w = numpy.empty(shape=[3, 3])
            for item1 in range(0, 3):
                for item2 in range(0, 3):
                    v[item1][item2] = 0
                    for item3 in range(0, 3):
                        v[item1][item2] = v[item1][item2] + mat_for_cal[item1][item3] * ijk_mat_cal[item2][item3]
            for obj1 in range(0, 3):
                for obj2 in range(0, 3):
                    w[obj1][obj2] = 0
                    for obj3 in range(0, 3):
                        w[obj1][obj2] = w[obj1][obj2] + ijk_mat_cal[obj1][obj3] * v[obj3][obj2]
            print("v", v)
            print("w", w)

            reci_a = numpy.sqrt(abs(w[0][0]))
            reci_b = numpy.sqrt(abs(w[1][1]))
            reci_c = numpy.sqrt(abs(w[2][2]))
            print("reciprocal_abc", reci_a, reci_b, reci_c)

            angle_temp12 = numpy.degrees(numpy.arccos(w[1][2] /
                                                      (numpy.sqrt(w[1][1] * w[2][2]))))
            angle_temp02 = numpy.degrees(numpy.arccos(w[0][2] /
                                                      (numpy.sqrt(w[0][0] * w[2][2]))))
            angle_temp01 = numpy.degrees(numpy.arccos(w[0][1] /
                                                      (numpy.sqrt(w[0][0] * w[1][1]))))
            print("reciprocal_angle_abc", angle_temp12, angle_temp02, angle_temp01)
            niggli_mat = numpy.array([[reci_a ** 2, reci_b ** 2, reci_c ** 2],
                                      [reci_b * reci_c * numpy.cos((numpy.pi / 180) * (180 - angle_temp12)),
                                       reci_a * reci_c * numpy.cos((numpy.pi / 180) * angle_temp02),
                                       reci_a * reci_b * numpy.cos((numpy.pi / 180) * angle_temp01)]],
                                     dtype=numpy.float32)
            print("Niggli", niggli_mat)
            reci_sub_ab = abs(reci_a - reci_b)
            reci_sub_ac = abs(reci_a - reci_c)
            reci_sub_bc = abs(reci_b - reci_c)
            angle_sub_12 = abs(angle_temp12 - 90)
            angle_sub_02 = abs(angle_temp02 - 90)
            angle_sub_01 = abs(angle_temp01 - 90)
            print("reci_sub_ab,ac,bc", reci_sub_ab, reci_sub_ac, reci_sub_bc)
            print("angle_sub12,02,01", angle_sub_12, angle_sub_01, angle_sub_02)
            global reciprocal_lattice
            if reci_sub_ab and reci_sub_bc and reci_sub_ac <= tol_r_err:
                if angle_sub_12 and angle_sub_02 and angle_sub_01 <= tol_r_err:
                    reciprocal_lattice = 'cubic'
                else:
                    reciprocal_lattice = 'trigonal'
            if reci_sub_ab and reci_sub_ac and reci_sub_bc >= tol_r_err:
                if angle_sub_12 and angle_sub_02 and angle_sub_01 <= tol_r_err:
                    reciprocal_lattice = 'orthorhombic'
                if angle_sub_12 and angle_sub_02 and angle_sub_01 >= tol_r_err:
                    reciprocal_lattice = 'triclinic'
                else:
                    reciprocal_lattice = 'monoclinic'
            if reci_sub_ab <= tol_r_err:
                if reci_sub_ac and reci_sub_bc >= tol_r_err:
                    if angle_sub_12 and angle_sub_02 and angle_sub_01 <= tol_r_err:
                        reciprocal_lattice = 'tetragonal'
                    else:
                        reciprocal_lattice = 'hexagonal'
            print(reciprocal_lattice)
            if angle_temp12 < 90 and angle_temp02 < 90 and angle_temp01 < 90:
                n_type = 'type 1'
            else:
                n_type = 'type 2'
            print("n_type", n_type)
            data = find_niggli_cell.niggli_cell(niggli_mat, tol_r_err, n_type)
            # data = ((11, '1 0 0 0 1 0 0 0 1', 'p'),)
            # reciprocal_lattice = "orthorhombic"
            reduced_id = data[0][0]
            transformation = data[0][1]
            global bravais
            bravais = data[0][2]
            transformation = transformation.split(" ")
            result_trans = []
            for i in range(len(transformation)):
                result_trans.append(int(transformation[i]))
            trans_m = numpy.array(result_trans).reshape(3, 3)
            # trans_m = numpy.array([[1, 0, 2],
            #                        [1, 0, 0],
            #                        [0, 1, 0]])  # Mg4Zn7
            reci_trans_a = numpy.sqrt(
                numpy.square(trans_m[0][0] * reci_a) +
                numpy.square(trans_m[0][1] * reci_b) +
                numpy.square(trans_m[0][2] * reci_c) +
                2 * trans_m[0][0] * trans_m[0][1] * niggli_mat[1][2] +
                2 * trans_m[0][0] * trans_m[0][2] * niggli_mat[1][1] +
                2 * trans_m[0][1] * trans_m[0][2] * niggli_mat[1][0])
            reci_trans_b = numpy.sqrt(
                numpy.square(trans_m[1][0] * reci_a) +
                numpy.square(trans_m[1][1] * reci_b) +
                numpy.square(trans_m[1][2] * reci_c) +
                2 * trans_m[1][0] * trans_m[1][1] * niggli_mat[1][2] +
                2 * trans_m[1][0] * trans_m[1][2] * niggli_mat[1][1] +
                2 * trans_m[1][1] * trans_m[1][2] * niggli_mat[1][0])
            reci_trans_c = numpy.sqrt(
                numpy.square(trans_m[2][0] * reci_a) +
                numpy.square(trans_m[2][1] * reci_b) +
                numpy.square(trans_m[2][2] * reci_c) +
                2 * trans_m[2][0] * trans_m[2][1] * niggli_mat[1][2] +
                2 * trans_m[2][0] * trans_m[2][2] * niggli_mat[1][1] +
                2 * trans_m[2][1] * trans_m[2][2] * niggli_mat[1][0])
            print(reci_trans_a, reci_trans_b, reci_trans_c)
            reci_angle_a = numpy.degrees(
                numpy.arccos(niggli_mat[1][0] / (reci_trans_b * reci_trans_c)))
            reci_angle_b = numpy.degrees(
                numpy.arccos(niggli_mat[1][1] / (reci_trans_a * reci_trans_c)))
            reci_angle_c = numpy.degrees(
                numpy.arccos(niggli_mat[1][2] / (reci_angle_a * reci_angle_b)))
            print(reci_angle_a, reci_angle_b, reci_angle_c)
            global real_a, real_b, real_c, real_alpha, real_beta, real_theta
            if reciprocal_lattice == 'monoclinic':
                real_a = 1 / (reci_trans_a * numpy.sin(reci_angle_b * numpy.pi / 180))
                real_b = 1 / reci_trans_b
                real_c = 1 / (reci_trans_c * numpy.sin(reci_angle_b * numpy.pi / 180))
                real_alpha = 90
                real_beta = 180 - reci_angle_b
                real_theta = 90
            if reciprocal_lattice == 'triclinic':
                pass
            if reciprocal_lattice == 'orthorhombic' or \
                    reciprocal_lattice == 'cubic' or reciprocal_lattice == 'tetragonal':
                real_a = 1 / reci_trans_a
                real_b = 1 / reci_trans_b
                real_c = 1 / reci_trans_c
                real_alpha = numpy.degrees(numpy.arccos(
                    numpy.sqrt(abs(niggli_mat[1][0])) / (real_a * real_b)))
                real_beta = numpy.degrees(numpy.arccos(
                    numpy.sqrt(abs(niggli_mat[1][1])) / (real_a * real_c)))
                real_theta = numpy.degrees(numpy.arccos(
                    numpy.sqrt(abs(niggli_mat[1][2])) / (real_b * real_c)))
            if reciprocal_lattice == 'trigonal':
                real_a = numpy.sin(reci_angle_a * numpy.pi / 180) / (
                        reci_trans_a * numpy.sqrt(
                    1 - 3 * pow(numpy.cos(reci_angle_a * numpy.pi / 180), 2) +
                    2 * pow(numpy.cos(reci_angle_a * numpy.pi / 180), 3)))
                real_b = real_a
                real_c = real_a
                real_alpha = numpy.degrees(numpy.arccos(
                    -numpy.cos(
                        reci_angle_a * numpy.pi / 180) / (1 + numpy.cos(
                        reci_angle_a * numpy.pi / 180))))
                real_beta = real_alpha
                real_theta = real_alpha
            # if reciprocal_lattice == 'tetragonal':
            #     real_a = 1 / reci_trans_a
            #     real_b = 1 / reci_trans_b
            #     real_c = 1 / reci_trans_c
            #     real_alpha = numpy.degrees(numpy.arccos(
            #         numpy.sqrt(abs(niggli_mat[1][0])) / (real_a * real_b)))
            #     real_beta = numpy.degrees(numpy.arccos(
            #         numpy.sqrt(abs(niggli_mat[1][1])) / (real_a * real_c)))
            #     real_theta = numpy.degrees(numpy.arccos(
            #         numpy.sqrt(abs(niggli_mat[1][2])) / (real_b * real_c)))
            if reciprocal_lattice == 'hexagonal':
                real_a = 1 / (reci_trans_a * numpy.sqrt(3))
                real_b = 1 / (reci_trans_a * numpy.sqrt(3))
                real_c = 1 / reci_trans_c
                real_alpha = numpy.degrees(numpy.arccos(
                    numpy.sqrt(abs(niggli_mat[1][0])) / (real_a * real_b)))
                real_beta = numpy.degrees(numpy.arccos(
                    numpy.sqrt(abs(niggli_mat[1][1])) / (real_a * real_c)))
                real_theta = numpy.degrees(numpy.arccos(
                    numpy.sqrt(abs(niggli_mat[1][2])) / (real_b * real_c)))
            # if reciprocal_lattice == 'cubic':
            #     real_a = 1 / reci_trans_a
            #     real_b = 1 / reci_trans_b
            #     real_c = 1 / reci_trans_c
            #     real_alpha = numpy.degrees(numpy.arccos(
            #         numpy.sqrt(abs(niggli_mat[1][0])) / (real_a * real_b)))
            #     real_beta = numpy.degrees(numpy.arccos(
            #         numpy.sqrt(abs(niggli_mat[1][1])) / (real_a * real_c)))
            #     real_theta = numpy.degrees(numpy.arccos(
            #         numpy.sqrt(abs(niggli_mat[1][2])) / (real_b * real_c)))
            print(real_a, real_b, real_c, real_alpha, real_beta, real_theta)

            reci_abc = numpy.hstack([empty_temp_mat[0][0], empty_temp_mat[1][1], empty_temp_mat[2][2]])
            result_mat = numpy.dot(reci_abc, trans_m)
            print(result_mat)
            # 实验
            real_a = 1 / (numpy.sqrt(result_mat[0]))
            real_b = 1 / (numpy.sqrt(result_mat[1]))
            real_c = 1 / (numpy.sqrt(result_mat[2]))
            # BaTiO
            # real_a = (1 / (numpy.sqrt(result_mat[0]) / 181.9 * 0.5)) * 2  # 181.9 和 0.5 以及是否 *2 应随用户输入而变化
            # real_b = (1 / (numpy.sqrt(result_mat[1]) / 182.3 * 0.5)) * 2  # 182.3 和 0.5 以及是否 *2 应随用户输入而变化
            # real_c = (1 / (numpy.sqrt(result_mat[2]) / 181.9 * 0.5)) * 2  # 181.9 和 0.5 以及是否 *2 应随用户输入而变化
            # HfO2
            # real_a = (1 / (numpy.sqrt(result_mat[0]) / 181.9 * 0.5)) * 2  # 181.9 和 0.5 以及是否 *4 应随用户输入而变化
            # real_b = (1 / (numpy.sqrt(result_mat[1]) / 181.9 * 0.5)) * 2  # 181.9 和 0.5 以及是否 *4 应随用户输入而变化
            # real_c = (1 / (numpy.sqrt(result_mat[2]) / 181.9 * 0.5)) * 2  # 181.9 和 0.5 以及是否 *4 应随用户输入而变化
            print(real_a, real_b, real_c)
            print('total', real_a + real_b + real_c)
            real_alpha = numpy.degrees(numpy.arccos(numpy.sqrt(abs(niggli_mat[1][0])) / (real_a * real_b)))
            real_beta = numpy.degrees(numpy.arccos(numpy.sqrt(abs(niggli_mat[1][1])) / (real_a * real_c)))
            real_theta = numpy.degrees(numpy.arccos(numpy.sqrt(abs(niggli_mat[1][2])) / (real_b * real_c)))
            print(real_alpha, real_beta, real_theta)
            # real_space_para = open('Text/map_real_space_para.txt', 'w+')
            # real_space_para.write(str(real_a) + ' ' + str(real_b) + ' ' + str(real_c) + ' '
            #                       + str(real_alpha) + ' ' + str(real_beta) + ' ' + str(real_theta))
            # real_space_para.close()
            # print('长度误差：', (abs(real_a - 5.114) + abs(real_b - 5.114) + abs(real_c - 5.114)) / 15.342)
            # print('角度误差：', (abs(real_alpha - 90) + abs(real_beta - 90) + abs(real_theta - 90)) / 270)  # HfO2
            # print('长度误差：', (abs(real_a - 17.062) + abs(real_b - 14.051) + abs(real_c - 9.862)) / 40.975)
            # print('角度误差：', (abs(real_alpha - 90) + abs(real_beta - 90) + abs(real_theta - 90)) / 270)  # Mg4Zn7
            error = 0.01
            real_length_ab = abs(real_a - real_b)
            real_length_bc = abs(real_b - real_c)
            alpha_error = abs(real_alpha - 90)
            beta_error = abs(real_beta - 90)
            theta_error = abs(real_theta - 90)
            lambda_error = abs(real_theta - 120)
            global real_lattice
            if real_length_ab > error:
                if alpha_error <= error and theta_error <= error:
                    if beta_error <= error:
                        real_lattice = 'orthorhombic'
                    else:
                        real_lattice = 'monoclinic'
                else:
                    real_lattice = 'triclinic'
            else:
                if real_length_bc > error:
                    if lambda_error < error:
                        real_lattice = 'hexagonal'
                    else:
                        real_lattice = 'tetragonal'
                else:
                    if theta_error > error:
                        real_lattice = 'trigonal'
                    else:
                        real_lattice = 'cubic'

            real_space_result = open("ResultText\\RealSpaceParametersResult.txt", 'a+')
            # 该文件应在文件头储存正空间晶系以供match_plane_group使用
            real_space_result.write('Reciprocal Space Info: ' + '\n')
            real_space_result.write(str(load_basic_vec[0, :]) + '\n')
            real_space_result.write(str(load_basic_vec[1, :]) + '\n')
            real_space_result.write(str(load_basic_vec[2, :]) + '\n')
            real_space_result.write(str(load_basic_vec[3, :]) + '\n')
            real_space_result.write(str(load_basic_vec[4, :]) + '\n')
            real_space_result.write(str(load_basic_vec[5, :]) + '\n')
            real_space_result.write('Length of Each Basic Vector (Pixel): ' + '\n')
            real_space_result.write(str("{:.5f}".format(mo_0)) + '\n')
            real_space_result.write(str("{:.5f}".format(mo_1)) + '\n')
            real_space_result.write(str("{:.5f}".format(mo_2)) + '\n')
            real_space_result.write(str("{:.5f}".format(mo_3)) + '\n')
            real_space_result.write(str("{:.5f}".format(mo_4)) + '\n')
            real_space_result.write(str("{:.5f}".format(mo_5)) + '\n')
            real_space_result.write('a: ' + "{:.5f}".format((mo_1 + mo_2) / 2) + '\n')
            real_space_result.write('b: ' + "{:.5f}".format((mo_0 + mo_4) / 2) + '\n')
            real_space_result.write('c: ' + "{:.5f}".format((mo_3 + mo_5) / 2) + '\n')
            real_space_result.write('Length of Each Basic Vector (1/nm): ' + '\n')
            real_space_result.write('a: ' + "{:.5f}".format((mo_1 + mo_2) / 2 / pixel * 10) + '\n')
            real_space_result.write('b: ' + "{:.5f}".format((mo_0 + mo_4) / 2 / pixel * 10) + '\n')
            real_space_result.write('c: ' + "{:.5f}".format((mo_3 + mo_5) / 2 / pixel * 10) + '\n')
            real_space_result.write('Angles (°): ' + '\n')
            real_space_result.write('alpha: ' + str("{:.5f}".format(angle_temp01)) + '\n')
            real_space_result.write('beta: ' + str("{:.5f}".format(angle_temp02)) + '\n')
            real_space_result.write('gamma: ' + str("{:.5f}".format(angle_temp12)) + '\n')
            real_space_result.write('Niggli Matrix: ' + str(niggli_mat) + '\n')
            real_space_result.write('Reduced Cell Number: ' + str(reduced_id) + '\n')
            real_space_result.write('Transformation: ' + trans_m + '\n')
            real_space_result.write('Real Space Info: ' + '\n')
            real_space_result.write(str("{:.5f}".format(real_a)) + '\n')
            real_space_result.write(str("{:.5f}".format(real_b)) + '\n')
            real_space_result.write(str("{:.5f}".format(real_c)) + '\n')
            real_space_result.write(str("{:.5f}".format(real_alpha)) + '\n')
            real_space_result.write(str("{:.5f}".format(real_beta)) + '\n')
            real_space_result.write(str("{:.5f}".format(real_theta)) + '\n')
            real_space_result.write('Lattice: ' + real_lattice)
            # print('长度误差：', format((abs(real_a - 17.062) + abs(real_b - 14.051) + abs(real_c - 9.862)) / 40.975,
            #                       '.5%'), filename=real_space_result)
            # print('长度误差：', format((abs(real_a - 5.114) + abs(real_b - 5.114) + abs(real_c - 5.114)) / 15.342,
            #                       '.5%'), filename=real_space_result)
            # print('角度误差：', format((abs(real_alpha - 90) + abs(real_beta - 90) + abs(real_theta - 90)) / 270,
            #                       '.5%'), filename=real_space_result)
            real_space_result.close()
        window.end_label.config(text="Finish To Calculate Real Space Parameters")
    else:
        pass
