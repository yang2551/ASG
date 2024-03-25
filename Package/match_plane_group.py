# coding = UTF-8
import os
import threading
import time
import tkinter
from tkinter import messagebox

import cv2
import numpy
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from Package import real_space_parameters, analyse_origin_at
from Package import side_functions, initial_peaks
from Package import analyse_general_position

symmetry_list = []
plane_lattice_list = []
direction_list = []
paras_from_fig = []
points = []
positions_xy = []
path_list = []
center_p = None
first_p = None
second_p = None
final = None
center_one, center_two, first_one, first_two = None, None, None, None
second_one, second_two, final_one, final_two = None, None, None, None
c_point = []
f_point = []
s_point = []
final_point = []
moment = None
tag = 0
origin_at_result = []
correspond_directions = []
bravais = None
params = []


# 返回二维平面信息
def get_match_plane_group_result():
    # symmetry_list = ["p2"]
    # direction_list = ["001"]
    # paras_from_fig = [[4.506, 2.842]]
    return [symmetry_list, direction_list, paras_from_fig, plane_lattice_list, bravais]


# 返回origin_at
def get_origin_at():
    return origin_at_result


# 根据计算所得二维平面群将对称元素画到图像上
def draw_operators(flag, error=1):
    def __draw_outlines():
        # 根据点的位置画单胞边界
        plt.plot([points[flag][0], points[flag + 1][0]],
                 [points[flag][1], points[flag + 1][1]],
                 color='w')
        plt.plot([points[flag][0], points[flag + 2][0]],
                 [points[flag][1], points[flag + 2][1]],
                 color='w')
        plt.plot([points[flag + 1][0], points[flag + 3][0]],
                 [points[flag + 1][1], points[flag + 3][1]],
                 color='w')
        plt.plot([points[flag + 2][0], points[flag + 3][0]],
                 [points[flag + 2][1], points[flag + 3][1]],
                 color='w')

    def __two_fold(pos, size_two):
        # 画二次轴，二次轴和其它轴次大小相差过大时可使用marksize调节
        plt.plot(pos[0], pos[1],
                 marker='d', markersize=size_two + 2,
                 color=(41 / 255, 152 / 255, 229 / 255))

    def __three_fold(pos, size_three):
        # 画三次轴，某些三次轴可能出现的位置不准确需自行调节
        triangle = patches.RegularPolygon(
            (pos[0], pos[1]), 3, size_three,
            color=(41 / 255, 152 / 255, 229 / 255))
        return triangle

    def __four_fold(pos, size_four):
        # 四次轴
        cubic = patches.RegularPolygon(
            (pos[0], pos[1]), 4, size_four,
            color=(41 / 255, 152 / 255, 229 / 255))
        return cubic

    def __six_fold(pos, size_six):
        # 六次轴，某些三次轴可能出现的位置不准确需自行调节
        hexagon = patches.RegularPolygon(
            (pos[0], pos[1]), 6, size_six,
            color=(41 / 255, 152 / 255, 229 / 255))
        return hexagon

    def __draw_mirror(first_pos, second_pos):
        # 画镜面位置
        plt.plot([first_pos[0], second_pos[0]],
                 [first_pos[1], second_pos[1]],
                 color=(45 / 255, 177 / 255, 235 / 255))

    def __draw_normal_op_oc(size_op_oc):
        # 正交原始、正交底心点阵的基本外形
        __two_fold(points[flag], size_op_oc)
        __two_fold(points[flag + 1], size_op_oc)
        __two_fold(points[flag + 2], size_op_oc)
        __two_fold(points[flag + 3], size_op_oc)
        __two_fold((points[flag + 1] + points[flag]) / 2, size_op_oc)
        __two_fold((points[flag] + points[flag + 2]) / 2, size_op_oc)
        __two_fold((points[flag + 1] + points[flag + 3]) / 2, size_op_oc)
        __two_fold((points[flag + 3] + points[flag + 2]) / 2, size_op_oc)
        __two_fold((points[flag + 1] + points[flag + 2]) / 2, size_op_oc)

    def __draw_normal_tp(size_tp):
        # 四方点阵的基本外形
        ax.add_patch(__four_fold(points[flag], size_tp))
        ax.add_patch(__four_fold(points[flag + 1], size_tp))
        ax.add_patch(__four_fold(points[flag + 2], size_tp))
        ax.add_patch(__four_fold(points[flag + 3], size_tp))
        ax.add_patch(__four_fold((points[flag + 1] + points[flag + 2]) / 2, size_tp))
        __two_fold((points[flag] + points[flag + 1]) / 2, size_tp)
        __two_fold((points[flag] + points[flag + 2]) / 2, size_tp)
        __two_fold((points[flag + 1] + points[flag + 3]) / 2, size_tp)
        __two_fold((points[flag + 2] + points[flag + 3]) / 2, size_tp)

    def __draw_normal_hp_six(size_hp_six):
        # 六方点阵中轴次为6的基本外形
        # length_hp_x = abs(points[flag][0] - points[flag + 3][0])
        # length_hp_y = abs(points[flag][1] - points[flag + 3][1])
        ax.add_patch(__six_fold(points[flag], size_hp_six))
        ax.add_patch(__six_fold(points[flag + 1], size_hp_six))
        ax.add_patch(__six_fold(points[flag + 2], size_hp_six))
        ax.add_patch(__six_fold(points[flag + 3], size_hp_six))
        __two_fold((points[flag + 1] + points[flag]) / 2, size_hp_six)
        __two_fold((points[flag + 2] + points[flag]) / 2, size_hp_six)
        __two_fold((points[flag + 1] + points[flag + 3]) / 2, size_hp_six)
        __two_fold((points[flag + 2] + points[flag + 3]) / 2, size_hp_six)
        __two_fold((points[flag + 1] + points[flag + 2]) / 2, size_hp_six)
        length_zero_final = numpy.sqrt(
            numpy.square(points[0][0] - points[3][0]) + numpy.square(points[0][1] - points[3][1])
        )
        length_first_second = numpy.sqrt(
            numpy.square(points[1][0] - points[2][0]) + numpy.square(points[1][1] - points[2][1])
        )
        if length_zero_final > length_first_second:
            long_diagonal = [points[0][0] - points[3][0], points[0][1] - points[3][1]]
            ax.add_patch(__three_fold([points[0][0] - 1 / 3 * long_diagonal[0],
                                       points[0][1] - 1 / 3 * long_diagonal[1]], size_hp_six))
            ax.add_patch(__three_fold([points[0][0] - 2 / 3 * long_diagonal[0],
                                       points[0][1] - 2 / 3 * long_diagonal[1]], size_hp_six))
        else:
            long_diagonal = [points[1][0] - points[2][0], points[1][1] - points[2][1]]
            ax.add_patch(__three_fold([points[1][0] - 1 / 3 * long_diagonal[0],
                                       points[1][1] - 1 / 3 * long_diagonal[1]], size_hp_six))
            ax.add_patch(__three_fold([points[1][0] - 2 / 3 * long_diagonal[0],
                                       points[1][1] - 2 / 3 * long_diagonal[1]], size_hp_six))
        # zero_final = [abs(points[1][0] - points[2][0]), abs(points[1][1] - points[2][1])]
        # ax.add_patch(__three_fold([1 / 3 * zero_final[0] + points[2][0],
        #                            points[2][1] - 1 / 3 * zero_final[1]], size_hp_six))
        # ax.add_patch(__three_fold([2 / 3 * zero_final[0] + points[2][0],
        #                            points[2][1] - 2 / 3 * zero_final[1]], size_hp_six))
        # if abs(points[flag + 1][0] - points[flag + 2][0]) <= error:
        #     ax.add_patch(__three_fold([1 / 3 * length_hp_x + points[flag][0],
        #                                points[flag][1]], size_hp_six))
        #     ax.add_patch(__three_fold([points[flag][0] + 2 / 3 * length_hp_x,
        #                                points[flag][1]], size_hp_six))
        # else:
        #     if points[flag + 1][0] < points[flag + 2][0]:
        #         ax.add_patch(__three_fold([1 / 3 * length_hp_x + points[flag][0],
        #                                    (points[flag][1] + points[flag + 1][1]) / 2], size_hp_six))
        #         ax.add_patch(__three_fold([points[flag][0] + 2 / 3 * length_hp_x,
        #                                    (points[flag + 2][1] + points[flag + 3][1]) / 2], size_hp_six))
        #     if points[flag + 1][0] > points[flag + 2][0]:
        #         ax.add_patch(__three_fold([points[flag][0] + 1 / 3 * length_hp_x,
        #                                    (points[flag][1] + points[flag + 2][1]) / 2], size_hp_six))
        #         ax.add_patch(__three_fold([2 / 3 * length_hp_x + points[flag][0],
        #                                    (points[flag + 1][1] + points[flag + 3][1]) / 2], size_hp_six))

    def __draw_normal_hp_three(size_hp_three):
        # 六方点阵中轴次3的基本外形
        length = abs(points[flag][0] - points[flag + 3][0])
        ax.add_patch(__three_fold(points[flag], size_hp_three))
        ax.add_patch(__three_fold(points[flag + 1], size_hp_three))
        ax.add_patch(__three_fold(points[flag + 2], size_hp_three))
        ax.add_patch(__three_fold(points[flag + 3], size_hp_three))
        if abs(points[flag + 1][0] - points[flag + 2][0]) <= error:
            ax.add_patch(__three_fold([points[flag + 1][0] + 1 / 3 * length,
                                       points[flag + 1][1]], size_hp_three))
            ax.add_patch(__three_fold([points[flag + 1][0] + 2 / 3 * length,
                                       points[flag + 1][1]], size_hp_three))
        else:
            if abs(points[flag + 1][1] - points[flag + 2][1]) <= error:
                ax.add_patch(__three_fold([points[flag][0] + 1 / 3 * length,
                                           points[flag][1]], size_hp_three))
                ax.add_patch(__three_fold([points[flag][0] + 2 / 3 * length,
                                           points[flag][1]], size_hp_three))
            else:
                if points[flag + 1][0] < points[flag + 2][0]:
                    ax.add_patch(__three_fold([points[flag][0] + 1 / 3 * length,
                                               (points[flag][1] + points[flag + 1][1]) / 2], size_hp_three))
                    ax.add_patch(__three_fold([points[flag][0] + 2 / 3 * length,
                                               (points[flag + 2][1] + points[flag + 3][1]) / 2], size_hp_three))
                if points[flag + 1][0] > points[flag + 2][0]:
                    ax.add_patch(__three_fold([points[flag][0] + 1 / 3 * length,
                                               (points[flag][1] + points[flag + 2][1]) / 2], size_hp_three))
                    ax.add_patch(__three_fold([points[flag][0] + 2 / 3 * length,
                                               (points[flag + 1][1] + points[flag + 3][1]) / 2], size_hp_three))

    for i in range(len(symmetry_list)):
        size = params[len(params) - 1]
        image = cv2.imread(path_list[i], cv2.IMREAD_GRAYSCALE)
        figure, ax = plt.subplots()
        plt.imshow(image)
        for j in positions_xy:
            plt.plot(j[0], j[1], marker=".", color="g")
        if symmetry_list[i] == 'p1':
            figure.canvas.manager.set_window_title("p1")
            __draw_outlines()
        if symmetry_list[i] == 'p2':
            figure.canvas.manager.set_window_title("p2")
            __draw_outlines()
            __draw_normal_op_oc(size)
        if symmetry_list[i] == 'p1m1' or symmetry_list[i] == 'p11m':
            figure.canvas.manager.set_window_title("p1m1")
            __draw_outlines()
            __draw_mirror((points[flag] + points[flag + 1]) / 2,
                          (points[flag + 2] + points[flag + 3]) / 2)
        if symmetry_list[i] == 'p1g1' or symmetry_list[i] == 'p11g':
            figure.canvas.manager.set_window_title("p1g1")
            __draw_outlines()
        if symmetry_list[i] == 'c1m1' or symmetry_list[i] == 'c11m':
            figure.canvas.manager.set_window_title("c1m1")
            __draw_outlines()
            __draw_mirror((points[flag] + points[flag + 1]) / 2,
                          (points[flag + 2] + points[flag + 3]) / 2)
        if symmetry_list[i] == 'p2mm':
            figure.canvas.manager.set_window_title("p2mm")
            __draw_outlines()
            __draw_normal_op_oc(size)
            __draw_mirror((points[flag] + points[flag + 1]) / 2,
                          (points[flag + 2] + points[flag + 3]) / 2)
            __draw_mirror((points[flag + 2] + points[flag]) / 2,
                          (points[flag + 1] + points[flag + 3]) / 2)
        if symmetry_list[i] == 'p2mg' or symmetry_list[i] == 'p2gm':
            length_y = abs(points[flag + 1][1] - points[flag][1])
            figure.canvas.manager.set_window_title("p2mg")
            __draw_outlines()
            __draw_normal_op_oc(size)
            __draw_mirror([points[flag + 1][0], points[flag + 1][1] + length_y / 3],
                          [points[flag + 3][0], points[flag + 3][1] + length_y / 3])
            __draw_mirror([points[flag + 1][0], points[flag + 1][1] + length_y * 2 / 3],
                          [points[flag + 3][0], points[flag + 3][1] + length_y * 2 / 3])
        if symmetry_list[i] == 'p2gg':
            figure.canvas.manager.set_window_title("p2gg")
            __draw_outlines()
            __draw_normal_op_oc(size)
        if symmetry_list[i] == 'c2mm':
            # length_x = abs(points[flag + 2][0] - points[flag][0])
            # length_y = abs(points[flag + 1][1] - points[flag][1])
            figure.canvas.manager.set_window_title("c2mm")
            __draw_outlines()
            __draw_normal_op_oc(size)
            # two_fold([points[flag + 1][0] + 0.25 * length_x,
            #           points[flag + 1][1] + 0.25 * length_y])
            # two_fold([points[flag + 1][0] + 0.25 * length_x,
            #           points[flag + 1][1] + 0.75 * length_y])
            # two_fold([points[flag + 1][0] + 0.75 * length_x,
            #           points[flag + 1][1] + 0.25 * length_y])
            # two_fold([points[flag + 1][0] + 0.75 * length_x,
            #           points[flag + 1][1] + 0.75 * length_y])
            __draw_mirror((points[flag] + points[flag + 1]) / 2,
                          (points[flag + 2] + points[flag + 3]) / 2)
            __draw_mirror((points[flag] + points[flag + 2]) / 2,
                          (points[flag + 1] + points[flag + 3]) / 2)
        if symmetry_list[i] == 'p4':
            figure.canvas.manager.set_window_title("p4")
            __draw_outlines()
            __draw_normal_tp(size)
        if symmetry_list[i] == 'p4gm':
            figure.canvas.manager.set_window_title("p4mg")
            __draw_outlines()
            __draw_normal_tp(size)
            __draw_mirror((points[flag] + points[flag + 1]) / 2,
                          (points[flag] + points[flag + 2]) / 2)
            __draw_mirror((points[flag] + points[flag + 1]) / 2,
                          (points[flag + 1] + points[flag + 3]) / 2)
            __draw_mirror((points[flag + 2] + points[flag + 3]) / 2,
                          (points[flag + 1] + points[flag + 3]) / 2)
            __draw_mirror((points[flag + 2] + points[flag + 3]) / 2,
                          (points[flag] + points[flag + 2]) / 2)
        if symmetry_list[i] == 'p4mm':
            figure.canvas.manager.set_window_title("p4mm")
            __draw_outlines()
            __draw_normal_tp(size)
            __draw_mirror((points[flag] + points[flag + 1]) / 2,
                          (points[flag + 3] + points[flag + 2]) / 2)
            __draw_mirror((points[flag] + points[flag + 2]) / 2,
                          (points[flag + 1] + points[flag + 3]) / 2)
        if symmetry_list[i] == 'p6':
            figure.canvas.manager.set_window_title("p6")
            __draw_outlines()
            __draw_normal_hp_six(size)
        if symmetry_list[i] == 'p6mm':
            figure.canvas.manager.set_window_title("p6mm")
            __draw_outlines()
            __draw_normal_hp_six(size)
            __draw_mirror(points[flag + 1], points[flag + 2])
            __draw_mirror(points[flag], points[flag + 3])
        if symmetry_list[i] == 'p3':
            figure.canvas.manager.set_window_title("p3")
            __draw_outlines()
            __draw_normal_hp_three(size)
        if symmetry_list[i] == 'p3m1':
            figure.canvas.manager.set_window_title("p3m1")
            __draw_outlines()
            __draw_normal_hp_three(size)
            __draw_mirror(points[flag + 1], points[flag + 2])
            __draw_mirror(points[flag], (points[flag + 2] + points[flag + 3]) / 2)
            __draw_mirror(points[flag + 3], (points[flag] + points[flag + 1]) / 2)
        if symmetry_list[i] == 'p31m':
            figure.canvas.manager.set_window_title("p31m")
            __draw_outlines()
            __draw_normal_hp_three(size)
            __draw_mirror(points[flag], points[flag + 3])
        flag += 4
        plt.gray()
        plt.axis('off')
        plt.axis('equal')
        plt.show()


def show_plane_group():
    draw_operators(flag=tag)
    threading.Thread(target=result).start()


def result():
    if len(symmetry_list) == 0:
        messagebox.showerror(title='Error', message='Please determine plane group first')
    else:
        # os.getcwd()获取当前程序运行的目录
        os.system(os.getcwd() + "\\ResultText\\MatchPlaneGroupResult.txt")
        os.system(os.getcwd() + "\\ResultText\\CalculatePlaneGroupParameters.txt")


def load_info_to_calculate_plane_group(window, lattice, image_file_path, text_font, menu_bar):
    """
    用户输入参数界面，输入完成后点击Confirm确定参数；后续点击Continue调用平面群测定函数。
    :param lattice: 晶系
    :param window: 主界面
    :param image_file_path: 文件路径
    :param text_font: 文本格式
    :param menu_bar: 菜单栏
    :return: None
    """
    self = tkinter.Toplevel()
    self.title('Loading Info for Plane Group Determination')
    self.geometry("%dx%d" % (650, 250))
    self.config(menu=menu_bar)
    self.resizable(height=False, width=False)
    tkinter.Label(self, text="Bravais(p, f, c, i, r)", font=text_font).place(x=20, y=10)
    self.input_bravais = tkinter.StringVar()
    input_bravais = tkinter.Entry(self, width=15)
    input_bravais.place(x=20, y=35, height=30)

    tkinter.Label(self, text="ToleranceError", font=text_font).place(x=245, y=10)
    self.tolerance = tkinter.StringVar()
    tolerance = tkinter.Entry(self, width=15)
    tolerance.place(x=245, y=35, height=30)

    tkinter.Label(self, text="CDs", font=text_font).place(x=245, y=80)
    self.direction = tkinter.StringVar()
    direction = tkinter.Entry(self, width=15)
    direction.place(x=245, y=105, height=30)

    tkinter.Label(self, text="Pixels(=0.1nm)", font=text_font).place(x=20, y=80)
    self.pixels_to_length = tkinter.StringVar()
    pixels_to_length = tkinter.Entry(self, width=15)
    pixels_to_length.place(x=20, y=105, height=30)

    tkinter.Label(self, text="Points(4 or 8 points)", font=text_font).place(x=20, y=150)
    self.points_four_or_eight = tkinter.StringVar()
    points_four_or_eight = tkinter.Entry(self, width=40)
    points_four_or_eight.place(x=20, y=175, height=30)

    tkinter.Label(self, text="ElementSize", font=text_font).place(x=450, y=10)
    self.element_size = tkinter.StringVar()
    element_size = tkinter.Entry(self, width=15)
    element_size.place(x=450, y=35, height=30)

    tkinter.Label(self, text="MomentDiff", font=text_font).place(x=450, y=80)
    self.moment_diff = tkinter.StringVar()
    moment_diff = tkinter.Entry(self, width=15)
    moment_diff.place(x=450, y=105, height=30)

    global params
    params = []

    def __set_params():
        bravais_entry = input_bravais.get()
        params.append(bravais_entry)
        tolerance_entry = tolerance.get()
        params.append(float(tolerance_entry))
        pixels_entry = pixels_to_length.get()
        params.append(float(pixels_entry))
        direction_entry = direction.get()
        params.append(direction_entry)
        points_entry = points_four_or_eight.get().split(" ")
        for i in range(len(points_entry)):
            params.append(int(points_entry[i]))
        moment_diff_entry = moment_diff.get()
        params.append(float(moment_diff_entry))
        element_size_entry = element_size.get()
        params.append(int(element_size_entry))

    tkinter.Label(self, text="Separate each params by blank space!",
                  font=("Times New Roman", 10, "bold", "underline")).place(x=20, y=215)
    tkinter.Button(self, text="Confirm", command=__set_params, width=7,
                   font=text_font).place(x=450, y=175, height=30)
    tkinter.Button(self, text="Continue", width=7,
                   command=lambda: plane_group(window, lattice, image_file_path, params),
                   font=text_font).place(x=530, y=175, height=30)
    self.mainloop()
    self.destroy()


# 开新线程计算二维平面群
def plane_group(window, lattice, path, input_info):
    threading.Thread(target=plane_group_thread, args=(window, lattice, path, input_info)).start()


# 确定平面点群和二维空间群
def plane_group_thread(window, real_lattice, image, input_info, symmetry=""):
    """
    计算平面群
    :param real_lattice: 晶系
    :param window: 主窗口
    :param image: 图像路径
    :param input_info: 参数输入窗口传入的值
    :param symmetry: 对称性信息
    :return: 平面群
    """
    global path_list, center_p, first_p, second_p, final, positions_xy, bravais
    global moment, c_point, f_point, s_point, final_point, points, origin_at_result
    global center_one, center_two, first_one, first_two, second_one, second_two, final_one, final_two
    window.start_label.config(text="Start To Determine Plane Group")
    # bravais晶格类型
    bravais = real_space_parameters.get_real_space_parameter()[4]
    if bravais is None:
        # 输入以配合晶格类型确定最终布拉菲点阵类型
        bravais = str(input_info[0])
    # 输入误差容限
    # tol_error = float(input("ToleranceError"))
    tol_error = float(input_info[1])
    # 标尺
    pixel_to_length = float(input_info[2])
    # 输入特征方向
    characteristic_direction = str(input_info[3])
    # 同一张图同一方向重新测，则去除上一次该方向的测试值
    if characteristic_direction in direction_list and image in path_list:
        index = direction_list.index(characteristic_direction)
        del symmetry_list[index]
        del plane_lattice_list[index]
        del paras_from_fig[index]
        del path_list[index]
        del direction_list[index]
        points = []
        c_point = []
        f_point = []
        s_point = []
        final_point = []
    # 衬度差异
    moment_differ = float(input_info[len(input_info) - 2])
    positions_xy, moment = side_functions.get_refine_peaks()
    if len(positions_xy) == 0:
        positions_xy = initial_peaks.get_initial_peaks()[0]
        moment = initial_peaks.get_initial_peaks()[1]
    # confirm = str(input("Need 8 points to confirm vertexes? (y/n): "))
    confirm = len(input_info)
    if confirm == 14:
        center_one = int(input_info[4])
        center_two = int(input_info[5])
        c_point = (positions_xy[center_one, :] + positions_xy[center_two, :]) / 2
        first_one = int(input_info[6])
        first_two = int(input_info[7])
        f_point = (positions_xy[first_one, :] + positions_xy[first_two, :]) / 2
        second_one = int(input_info[8])
        second_two = int(input_info[9])
        s_point = (positions_xy[second_one, :] + positions_xy[second_two, :]) / 2
        final_one = int(input_info[10])
        final_two = int(input_info[11])
        final_point = (positions_xy[final_one, :] + positions_xy[final_two, :]) / 2
    else:
        # 四个点框出单胞
        center_p = int(input_info[4])
        first_p = int(input_info[5])
        second_p = int(input_info[6])
        final = int(input_info[7])
        c_point = positions_xy[center_p, :]
        f_point = positions_xy[first_p, :]
        s_point = positions_xy[second_p, :]
        final_point = positions_xy[final, :]
    points.append(c_point)
    points.append(f_point)
    points.append(s_point)
    points.append(final_point)
    direction_list.append(characteristic_direction)
    path_list.append(image)
    # 分离 x 和 y 轴
    positions_x = positions_xy[:, 0]
    positions_y = positions_xy[:, 1]
    # 导入正了空间得到的晶系
    lattice = [real_space_parameters.get_real_space_parameter()[0]]
    if lattice is None:
        lattice = real_lattice
    # lattice = ["orthorhombic"]
    print(c_point, f_point, s_point, final_point)
    length_fc_x = c_point[0] - f_point[0]
    length_fc_y = c_point[1] - f_point[1]
    length_sc_x = c_point[0] - s_point[0]
    length_sc_y = c_point[1] - s_point[1]
    total_length = [abs(length_fc_x), abs(length_fc_y), abs(length_sc_x), abs(length_sc_y)]
    print(length_fc_x, length_fc_y, length_sc_x, length_sc_y)
    # 分别计算第一个点和第二个点与中心点的距离
    para_a = numpy.sqrt(numpy.square(length_fc_x) + numpy.square(length_fc_y))
    para_b = numpy.sqrt(numpy.square(length_sc_x) + numpy.square(length_sc_y))
    para_c = numpy.sqrt(
        numpy.square(final_point[0] - c_point[0]) + numpy.square(
            final_point[1] - c_point[1]))
    paras_from_fig.append([para_a / pixel_to_length, para_b / pixel_to_length])
    # 第一个点和第二个点之间的夹角
    degrees = numpy.degrees(numpy.arccos(
        numpy.dot(f_point - c_point, s_point - c_point) / (para_a * para_b)))
    print(para_a, para_b, para_c, degrees)
    print("length_error", abs(para_a - para_b))
    plane_lattice = ""
    mirror_number = 0  # 0,1,2
    rotation_axis = 1
    # direction_mirror = [0, 0]  # x, y方向, 指向向下为x, 像右为y
    sort_x = [c_point[0], f_point[0], s_point[0]]
    sort_y = [c_point[1], f_point[1], s_point[1]]
    x_sort = sorted(sort_x)
    y_sort = sorted(sort_y)
    positions_in_range = []
    number_of_atom = []
    # 寻找在所选单胞内部出现的点
    if plane_lattice == 'mp' or plane_lattice == 'hp':
        for i in range(0, positions_x.shape[0]):
            if positions_x[i] - x_sort[0] >= 0 and x_sort[2] - positions_x[i] >= 1:
                if positions_y[i] - y_sort[1] + 0.5 >= 0 and y_sort[2] - positions_y[i] >= 1:
                    positions_in_range.append([positions_x[i], positions_y[i]])
                    number_of_atom.append(i)
    else:
        for i in range(0, positions_x.shape[0]):
            if positions_x[i] - x_sort[0] > 0.5 and x_sort[2] - positions_x[i] > 0.5:
                if positions_y[i] - y_sort[0] > 0.5 and y_sort[1] - positions_y[i] > 0.5:
                    positions_in_range.append([positions_x[i], positions_y[i]])
                    number_of_atom.append(i)
    # 去除边界上的点
    for i in positions_in_range:
        if (i == c_point).all():
            positions_in_range.remove(i)
    for i in positions_in_range:
        if (i == f_point).all():
            positions_in_range.remove(i)
    for i in positions_in_range:
        if (i == s_point).all():
            positions_in_range.remove(i)
    for i in positions_in_range:
        if (i == final_point).all():
            positions_in_range.remove(i)
    for j in number_of_atom:
        if j == center_p:
            number_of_atom.remove(j)
    for j in number_of_atom:
        if j == first_p:
            number_of_atom.remove(j)
    for j in number_of_atom:
        if j == second_p:
            number_of_atom.remove(j)
    for j in number_of_atom:
        if j == final:
            number_of_atom.remove(j)
    print(number_of_atom)
    print("pir", positions_in_range)
    print("lens", len(positions_in_range))
    virtue_heart = [(f_point[0] + final_point[0]) / 2, (f_point[1] + final_point[1]) / 2]
    print("virtue", virtue_heart)
    # 确定平面晶系
    if abs(para_a - para_b) <= tol_error:
        if abs(degrees - 90) <= tol_error:
            rotation_axis = 4
            plane_lattice = 'tp'  # 正方，a=b, degrees=90
        else:
            flag = True
            if len(positions_in_range) != 0:
                for i in positions_in_range:
                    for j in positions_xy:
                        if abs(i[0] + 2 * (virtue_heart[0] - i[0]) - j[0]) > tol_error or abs(
                                i[1] + 2 * (virtue_heart[1] - i[1]) - j[1]) > tol_error:
                            flag = False
            if flag is False:
                rotation_axis = 3
                plane_lattice = 'hp'  # 菱形，a=b, degrees=60
            else:
                rotation_axis = 6
                plane_lattice = 'hp'  # 菱形，a=b, degrees=60
    if abs(para_a - para_b) >= tol_error:
        if abs(degrees - 90) <= tol_error:
            plane_lattice = 'op'  # 无心矩形
            for item in number_of_atom:  # 利用顶点位置确定虚拟单胞中心并与所有原子位置比较，判断是否真实存在单胞中心
                if abs(virtue_heart[0] - positions_x[item]) <= tol_error and abs(
                        virtue_heart[1] - positions_y[item]) <= tol_error:
                    if abs(moment[item] - moment[center_p]) >= moment_differ:
                        print("moment", moment[item], moment[center_p])
                        plane_lattice = 'op'
                        break
                    else:
                        plane_lattice = 'oc'  # 有心矩形，a!=b, degrees=90
                        break
        elif abs(degrees - 90) >= tol_error:
            plane_lattice = 'mp'  # 平行四边形，a!=b, degrees任意
        else:
            messagebox.showerror(title='Error', message='Error, Please Check Your Data!')
    print(plane_lattice)
    short_diagonal_with_mirror = None
    mirror_horizontal = 0
    mirror_vertical = 0
    # 利用点之间的角度确定旋转轴; 对称性判断镜面数量; 如果原子排列具有方向性则通过胞内的原子信息进一步确定
    if plane_lattice == "tp":
        if confirm == 10:
            rotation_axis = 4
            # 根据四个顶点判断单胞的边是否为镜面
            for i in range(0, positions_x.shape[0]):
                if abs(f_point[0] + 2 * length_fc_x - positions_x[i]) <= tol_error:
                    if abs(f_point[1] + 2 * length_fc_y - positions_y[i]) <= tol_error:
                        mirror_number = 1
                        for j in range(0, positions_y.shape[0]):
                            if abs(s_point[0] + 2 * length_sc_x - positions_x[j]) <= tol_error:
                                if abs(s_point[1] + 2 * length_sc_y - positions_y[j]) <= tol_error:
                                    mirror_number = 2
                                    break
                                else:
                                    mirror_number = 1
                            else:
                                mirror_number = 1
                if mirror_number == 2:
                    break
            if mirror_number == 0:  # 第一个点没有找到相应点的情况，循环没有进入第二点的相关判断，需反向处理
                for j in range(0, positions_y.shape[0]):
                    if abs(s_point[0] + 2 * length_sc_x - positions_x[j]) <= tol_error:
                        if abs(s_point[1] + 2 * length_sc_y - positions_y[j]) <= tol_error:
                            mirror_number = 1
                            break
            if mirror_number == 2:  # 需要判断内部点与外部是否都有镜面匹配
                if len(positions_in_range) != 0:
                    # 判断内部点在单胞边上是否存在镜面
                    for i in range(0, len(positions_in_range)):
                        length = numpy.array(c_point) - numpy.array(positions_in_range[i])
                        for j in range(0, positions_x.shape[0]):
                            if abs(positions_in_range[i][0] + 2 * length[0] - positions_x[j]) <= tol_error:
                                if abs(positions_in_range[i][1] - positions_y[j]) <= tol_error:
                                    mirror_number = 2
                                    break
                                else:
                                    mirror_number = 1
                            if abs(positions_in_range[i][0] - positions_x[j]) <= tol_error:
                                if abs(positions_in_range[i][1] + 2 * length[1] - positions_y[j]) <= tol_error:
                                    mirror_number = 2
                                    break
                                else:
                                    mirror_number = 1
            # 判断两条相邻边的中点连接线是否存在镜面，不存在则镜面数量为 0，存在则为 1
            if mirror_number == 1:
                central_b = [(c_point[0] + s_point[0]) / 2, (c_point[1] + s_point[1]) / 2]
                for item in positions_in_range:
                    for j in positions_xy:
                        if abs(item[0] + 2 * (central_b[0] - item[0]) - j[0]) <= tol_error:
                            if abs(item[1] + 2 * (central_b[1] - item[1]) - j[1]) <= tol_error:
                                mirror_number = 1
                                break
                            else:
                                mirror_number = 0
                        else:
                            mirror_number = 0
        else:
            for item in positions_in_range:
                for i in positions_xy:
                    if abs(item[0] + 2 * (c_point[0] - item[0]) - i[0]) <= tol_error:
                        if abs(item[1] - i[1]) <= tol_error:
                            if abs(item[0] - i[0]) <= tol_error:
                                if abs(item[1] + 2 * (c_point[1] - item[1]) - i[1]) <= tol_error:
                                    mirror_number = 2
                                    break
                                else:
                                    mirror_number = 1
                            else:
                                mirror_number = 1
                        else:
                            mirror_number = 1
                    else:
                        mirror_number = 1
            if mirror_number == 1:
                central_b = [(c_point[0] + s_point[0]) / 2, (c_point[1] + s_point[1]) / 2]
                for item in positions_in_range:
                    for j in positions_xy:
                        if abs(2 * (central_b[0] - item[0]) - j[0] + item[0]) <= tol_error:
                            if abs(item[1] + 2 * (central_b[1] - item[1]) - j[1]) <= tol_error:
                                mirror_number = 1
                                break
                            else:
                                mirror_number = 0
                        else:
                            mirror_number = 0
    if plane_lattice == "op":
        flag = 1
        for i in range(0, positions_x.shape[0]):
            if abs(f_point[0] + 2 * length_fc_x - positions_x[i]) <= tol_error or abs(
                    s_point[0] + 2 * length_sc_x - positions_x[i]) <= tol_error:
                if abs(f_point[1] + 2 * length_fc_y - positions_y[i]) <= tol_error or abs(
                        s_point[1] + 2 * length_sc_y - positions_y[i]) <= tol_error:
                    rotation_axis = 2
                    flag = 2
                    break
        for item in positions_in_range:
            index = number_of_atom[positions_in_range.index(item)]
            for i in range(0, positions_y.shape[0]):
                if abs(item[0] + 2 * (c_point[0] - item[0]) - positions_x[i]) <= tol_error:
                    if abs(item[1] + 2 * (c_point[1] - item[1]) - positions_y[i]) <= tol_error:
                        if abs(moment[index] - moment[i]) <= moment_differ:
                            rotation_axis = 2
                            flag = 2
                            break
        if flag == 1:
            rotation_axis = 1
        if flag == 2:
            rotation_axis = 2
        if rotation_axis == 2:
            print(first_p, second_p)
            tempo_center = [c_point[0], c_point[1] - 0.25 * length_fc_y]
            print(tempo_center)
            for i in range(positions_xy.shape[0]):
                if abs(f_point[0] - positions_x[i]) <= tol_error:
                    if abs(f_point[1] + 2 * length_fc_y - positions_y[i]) <= tol_error:
                        print(i)
                        if abs(moment[first_p] - moment[i]) <= moment_differ:
                            mirror_horizontal = 1
                    if abs(f_point[1] + 2 * (tempo_center[1] - f_point[1]) - positions_y[i]) <= tol_error:
                        if abs(moment[first_p] - moment[i]) <= moment_differ:
                            mirror_horizontal = 1
                if abs(s_point[0] + 2 * length_sc_x - positions_x[i]) <= tol_error:
                    if abs(s_point[1] - positions_y[i]) <= tol_error:
                        print(i)
                        if abs(moment[second_p] - moment[i]) <= moment_differ:
                            mirror_vertical = 1
            for item in positions_in_range:
                index = number_of_atom[positions_in_range.index(item)]
                print(index)
                for i in range(positions_xy.shape[0]):
                    if abs(item[0] - positions_x[i]) <= tol_error:
                        if abs(item[1] + 2 * (tempo_center[1] - item[1]) - positions_y[i]) <= tol_error:
                            if abs(moment[index] - moment[i]) <= moment_differ:
                                mirror_horizontal = 1
                        if abs(item[1] + 2 * (tempo_center[1] - item[1]) - positions_y[i]) <= tol_error:
                            if abs(moment[index] - moment[i]) <= moment_differ:
                                mirror_horizontal = 1
                    if abs(item[0] + 2 * (tempo_center[0] - item[0]) - positions_x[i]) <= tol_error:
                        if abs(item[1] - positions_y[i]) <= tol_error:
                            if abs(moment[index] - moment[i]) <= moment_differ:
                                print(item, i)
                                mirror_vertical = 1
        if rotation_axis == 1:
            for i in range(positions_xy.shape[0]):
                if abs(f_point[0] - positions_x[i]) <= tol_error:
                    if abs(f_point[1] + 2 * length_fc_y - positions_y[i]) <= tol_error:
                        if abs(moment[first_p] - moment[i]) <= moment_differ:
                            mirror_horizontal = 1
                for item in positions_in_range:
                    index = number_of_atom[positions_in_range.index(item)]
                    if abs(item[0] - positions_x[0]) <= tol_error:
                        if abs(item[1] + 2 * (c_point[1] - item[1]) - positions_y[i]) <= tol_error:
                            if abs(moment[index] - moment[i]) <= moment_differ:
                                mirror_horizontal = 1
        if mirror_horizontal == 1 and mirror_vertical == 1:
            mirror_number = 2
        elif mirror_horizontal == 0 and mirror_vertical == 0:
            mirror_number = 0
        else:
            mirror_number = 1
        print(mirror_horizontal, mirror_vertical)
    if plane_lattice == "oc":
        flag = 0
        for i in range(0, positions_x.shape[0]):
            if abs(f_point[0] + 2 * length_fc_x - positions_x[i]) <= tol_error or abs(
                    s_point[0] + 2 * length_sc_x - positions_x[i]) <= tol_error:
                if abs(f_point[1] + 2 * length_fc_y - positions_y[i]) <= tol_error or abs(
                        s_point[1] + 2 * length_sc_y - positions_y[i]) <= tol_error:
                    rotation_axis = 2
        for item in positions_in_range:
            index = number_of_atom[positions_in_range.index(item)]
            for i in range(0, positions_y.shape[0]):
                if abs(item[0] + 2 * (c_point[0] - item[0]) - positions_x[i]) <= tol_error:
                    if abs(item[1] + 2 * (c_point[1] - item[1]) - positions_y[i]) <= tol_error:
                        if abs(moment[index] - moment[i]) <= moment_differ:
                            rotation_axis = 2
                        else:
                            rotation_axis = 1
                            flag = 1
                            break
                    else:
                        rotation_axis = 1
                        flag = 1
                        break
                else:
                    rotation_axis = 1
                    flag = 1
                    break
        if flag == 1:
            rotation_axis = 1
            mirror_number = 1
    if plane_lattice == "hp":
        if rotation_axis == 3:
            for i in range(0, positions_x.shape[0]):
                if abs(f_point[0] + 2 * length_fc_x - positions_x[i]) <= tol_error:
                    if abs(f_point[1] - positions_y[i]) <= tol_error:
                        mirror_number = 1
                        break
                if abs(s_point[0] - positions_x[i]) <= tol_error:
                    if abs(s_point[1] + 2 * length_sc_y - positions_y[i]) <= tol_error:
                        mirror_number = 1
                        break
            for item in positions_in_range:
                for i in range(positions_xy.shape[0]):
                    if abs(item[0] + 2 * (c_point[0] - item[0]) - positions_x[i]) <= tol_error:
                        if abs(item[1] - positions_y[i]) <= tol_error:
                            mirror_number = 1
                            break
                    if abs(item[0] - positions_x[i]) <= tol_error:
                        if abs(item[1] + 2 * (c_point[1] - item[1]) - positions_y[i]) <= tol_error:
                            mirror_number = 1
                            break
            if mirror_number == 1:
                for item in positions_in_range:
                    index = number_of_atom[positions_in_range.index(item)]
                    for i in range(positions_xy.shape[0]):
                        if abs(item[0] + 2 * (c_point[0] - item[0]) - positions_x[i]) <= tol_error:
                            if abs(item[1] - positions_y[i]) <= tol_error:
                                if abs(moment[index] - moment[i]) <= moment_differ:
                                    short_diagonal_with_mirror = 1
        if rotation_axis == 6:
            for i in range(0, positions_x.shape[0]):
                for item in positions_in_range:
                    if abs(f_point[0] + 2 * length_fc_x - positions_x[i]) <= tol_error or abs(
                            item[0] + 2 * (c_point[0] - item[0]) - positions_x[i]) <= tol_error:
                        if abs(f_point[1] - positions_y[i]) or abs(item[1] - positions_y[i]) <= tol_error:
                            mirror_number = 2
            for j in range(0, positions_y.shape[0]):
                for item in positions_in_range:
                    if abs(s_point[0] - positions_x[j]) or abs(item[0] - positions_x[j]) <= tol_error:
                        if abs(s_point[1] + 2 * length_sc_y - positions_y[j]) <= tol_error or abs(
                                item[1] + 2 * (c_point[1] - item[1]) - positions_y[j]) <= tol_error:
                            mirror_number = 2
                            break
            if mirror_number == 0:  # 第一个点没有找到相应点导致第二个点没有进行判断
                for j in range(0, positions_y.shape[0]):
                    if abs(s_point[0] + 2 * length_sc_x - positions_x[j]) <= tol_error:
                        if abs(s_point[1] + 2 * length_sc_y - positions_y[j]) <= tol_error:
                            mirror_number = 2
                            break
            # 判断内部原子是否影响镜面的分布
            if mirror_number == 2:
                for item in positions_in_range:
                    for i in range(positions_xy.shape[0]):
                        if abs(item[0] + 2 * (c_point[0] - item[0]) - positions_x[i]) <= tol_error:
                            if abs(item[1] - positions_y[i]) <= tol_error:
                                mirror_number = 2
                                break
                            else:
                                mirror_number = 0
                        if abs(item[0] - positions_x[i]) <= tol_error:
                            if abs(item[1] + 2 * (c_point[1] - item[1]) - positions_y[i]) <= tol_error:
                                mirror_number = 2
                                break
                            else:
                                mirror_number = 0
    if plane_lattice == "mp":
        if confirm == 10:
            for i in range(0, positions_x.shape[0]):
                if abs(2 * length_fc_x - positions_x[i] + f_point[0]) <= tol_error or abs(
                        s_point[0] + 2 * length_sc_x - positions_x[i]) <= tol_error:
                    if abs(f_point[1] + 2 * length_fc_y - positions_y[i]) <= tol_error or abs(
                            s_point[1] + 2 * length_sc_y - positions_y[i]) <= tol_error:
                        rotation_axis = 2
            if rotation_axis == 2:
                for item in positions_in_range:
                    for i in range(positions_xy.shape[0]):
                        if abs(item[0] + 2 * (c_point[0] - item[0]) - positions_x[i]) <= tol_error:
                            if abs(item[1] + 2 * (c_point[1] - item[1]) - positions_y[i]) <= tol_error:
                                rotation_axis = 2
                                break
        else:
            if len(positions_in_range) != 0:
                for j in positions_in_range:
                    for i in range(0, positions_x.shape[0]):
                        if abs(j[0] - 2 * (j[0] - c_point[0]) - positions_x[i]) <= tol_error:
                            if abs(j[1] - 2 * (j[1] - c_point[1]) - positions_y[i]) <= tol_error:
                                rotation_axis = 2
    # 利用晶面和滑移面数量确定平面群，但有时候对应多个平面群，此时应有其它的判断条件
    if plane_lattice == 'tp':
        if rotation_axis == 4:
            if mirror_number == 2:
                symmetry = 'p4mm'  # p4mm
            elif mirror_number == 1:
                symmetry = 'p4gm'  # p4gm
            else:
                symmetry = 'p4'  # p4
    if plane_lattice == 'op':
        if rotation_axis == 1:
            if mirror_number == 0:
                if lattice[0] == "monoclinic" or lattice[0] == "orthorhombic":
                    if characteristic_direction == "010":
                        symmetry = "p11g"
                    if characteristic_direction == "100":
                        symmetry = "p1g1"
                else:
                    symmetry = 'p1g1'
            if mirror_number == 1:
                if lattice[0] == "trigonal" or lattice[0] == "hexagonal" or lattice[0] == "monoclinic":
                    if mirror_horizontal == 1:
                        symmetry = "p1m1"
                    else:
                        symmetry = "p11m"
                elif lattice[0] == "orthorhombic":
                    if characteristic_direction == "010":
                        symmetry = "p11m"
                    if characteristic_direction == "100":
                        symmetry = "p1m1"
                else:
                    symmetry = "p11m"
        if rotation_axis == 2:
            if mirror_number == 2:
                symmetry = 'p2mm'  # p2mm
            elif mirror_number == 0:
                if lattice[0] == "trigonal":
                    symmetry = 'p2'
                else:
                    symmetry = 'p2gg'  # p2gg
            else:
                if lattice[0] == "cubic":
                    if characteristic_direction == "001":
                        symmetry = 'p2gm'
                    if characteristic_direction == "110":
                        if bravais == "i":
                            symmetry = "p2mg"
                        else:
                            symmetry = "p2gm"
                if lattice[0] == "hexagonal":
                    symmetry = "p2gm"
                if lattice[0] == "monoclinic":
                    if characteristic_direction == "100":
                        symmetry = "p2gm"
                    if characteristic_direction == "010":
                        symmetry = "p2mg"
                if lattice[0] == "trigonal":
                    symmetry = "p2gm"
                if lattice[0] == "tetragonal" or lattice[0] == "orthorhombic":
                    if mirror_horizontal == 1:
                        symmetry = "p2mg"
                    else:
                        symmetry = "p2gm"
    if plane_lattice == 'oc':
        if rotation_axis == 1:
            if lattice[0] == "orthorhombic":
                if characteristic_direction == "100":
                    symmetry = "c1m1"
                if characteristic_direction == "010":
                    symmetry = "c11m"
            if lattice[0] == "tetragonal":
                if characteristic_direction == "100":
                    symmetry = "c1m1"
                if characteristic_direction == "110":
                    symmetry = "c11m"
            if lattice[0] == "cubic":
                symmetry = "c1m1"
            if lattice[0] == "monoclinic":
                if characteristic_direction == "001":
                    symmetry = "c11m"
                if characteristic_direction == "100":
                    symmetry = "c1m1"
        # if direction_mirror[0] == 1:
        #     symmetry = 'c1m1'  # c1m1
        # else:
        #     symmetry = 'c11m'  # c11m
        if rotation_axis == 2:
            symmetry = 'c2mm'  # c2mm
    if plane_lattice == 'hp':
        if rotation_axis == 3:
            if mirror_number == 0:
                symmetry = 'p3'  # p3
            if mirror_number == 1:
                if short_diagonal_with_mirror is None:
                    symmetry = 'p3m1'  # p3m1
                else:
                    symmetry = 'p31m'  # p31m
        if rotation_axis == 6:
            if mirror_number == 0:
                symmetry = 'p6'  # p6
            else:
                symmetry = 'p6mm'  # p6mm
    if plane_lattice == 'mp':
        if rotation_axis == 1:
            symmetry = 'p1'  # p1
        else:
            symmetry = 'p2'  # p2
    print(symmetry)
    symmetry_list.append(symmetry)
    plane_lattice_list.append(plane_lattice)
    # 写入平面群，用户输入的特征方向信息
    with open("ResultText\\CalculatePlaneGroupParameters.txt", "r+") as all_paras:
        if center_p is None:
            # 分别写入时间、特征方向、单胞的4个顶点，单胞参数，二维平面晶系，二维平面群
            all_paras.writelines([time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n',
                                  "CDs: " + characteristic_direction + "\n",
                                  "Center (" + str([center_one, center_two]) + "): " + str(c_point.round(3)) + "\n",
                                  "First (" + str([first_one, first_two]) + "): " + str(f_point.round(3)) + "\n",
                                  "Second (" + str([second_one, second_two]) + "): " + str(s_point.round(3)) + "\n",
                                  "Final (" + str([final_one, final_two]) + "): " + str(final_point.round(3)) + "\n",
                                  "a: " + str(para_a.round(3)) + "\n", "b: " + str(para_b.round(3)) + "\n",
                                  "Length difference: " + str(abs(para_a - para_b).round(3)) + "\n",
                                  "Degrees: " + str(degrees.round(3)) + "\n",
                                  "Lattice: " + str(plane_lattice) + "\n",
                                  "2D space group: " + str(symmetry) + "\n"])
        else:
            all_paras.writelines([time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n',
                                  "CDs: " + characteristic_direction + "\n",
                                  "Center (" + str(center_p) + "): " + str(c_point.round(3)) + "\n",
                                  "First (" + str(first_p) + "): " + str(f_point.round(3)) + "\n",
                                  "Second (" + str(second_p) + "): " + str(s_point.round(3)) + "\n",
                                  "Final (" + str(final) + "): " + str(final_point.round(3)) + "\n",
                                  "a: " + str(para_a.round(3)) + "\n", "b: " + str(para_b.round(3)) + "\n",
                                  "Length difference: " + str(abs(para_a - para_b).round(3)) + "\n",
                                  "Degrees: " + str(degrees.round(3)) + "\n",
                                  "Lattice: " + str(plane_lattice) + "\n",
                                  "2D space group: " + str(symmetry) + "\n"])
    all_paras.close()
    with open("ResultText\\MatchPlaneGroupResult.txt", "r+") as text_plane_group:
        text_plane_group.seek(0, 0)
        text_plane_group.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        text_plane_group.write('\n')
        text_plane_group.write(characteristic_direction)
        text_plane_group.write(' ' + str(plane_lattice))
        text_plane_group.write(' ' + str(symmetry) + '\n')
    text_plane_group.close()
    window.end_label.config(text="Finish To Determine Plane Group")
    # 确定origin_at
    analyse_origin_at.origin_at(lattice, positions_xy, moment,
                                characteristic_direction, points, total_length, tol_error,
                                positions_in_range, number_of_atom, cv2.imread(image).shape)
    # 确定general_position
    analyse_general_position.calculate_general_position(lattice, points, characteristic_direction, tol_error)
    return symmetry
