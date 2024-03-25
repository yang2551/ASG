# coding = UTF-8
import os
import threading
import tkinter

import cv2
import matplotlib.pyplot as plt
import numpy
import pyperclip

from Package import side_functions, initial_peaks

basic_vector_result = []
real_space_params = []


# 其它函数调用可得到该类基本矢量的计算结果
def get_basic_vector():
    return basic_vector_result


# 启用新线程用记事本打开结果
def show_matrix():
    threading.Thread(target=basic_vector_cal_result).start()


# 获取导出基本矢量的文件路径
def basic_vector_cal_result():
    path = os.getcwd() + "\\ResultText\\BasicVectorCalculateResult.txt"
    pyperclip.copy(path)
    os.system(path)
    return path


def load_points_to_calculate_matrix(window, image_file_path, text_font, menu_bar):
    """
    :param window: 主界面
    :param image_file_path: 文件路径
    :param text_font: 文本格式
    :param menu_bar: 菜单栏
    :return:
    """
    self = tkinter.Toplevel()
    self.title('Loading Points')
    self.geometry("%dx%d" % (650, 100))
    self.config(menu=menu_bar)
    self.resizable(height=False, width=False)
    tkinter.Label(self, text="Center First Second", font=text_font).place(x=20, y=10)
    self.length_abc = tkinter.StringVar()
    length_abc = tkinter.Entry(self, width=25)
    length_abc.place(x=20, y=35, height=30)

    tkinter.Label(self, text="Separate each params by blank space!",
                  font=("Times New Roman", 10, "bold", "underline")).place(x=20, y=70)

    global real_space_params
    real_space_params = []

    def __set_params():
        # 返回用户输入的值
        real_space_params_length = length_abc.get().split(" ")
        for i in range(len(real_space_params_length)):
            real_space_params.append(int(real_space_params_length[i]))

    tkinter.Button(self, text="Confirm", command=__set_params, width=7,
                   font=text_font).place(x=400, y=35, height=30)
    tkinter.Button(self, text="Continue", width=7,
                   command=lambda: matrix_cal_thread(window, image_file_path, real_space_params),
                   font=text_font).place(x=500, y=35, height=30)
    self.mainloop()
    self.destroy()


# 计算 single crystal 或者实验图像的矩阵，也可以用于二维平面群确定时对 HAADF 像的操作
def matrix_cal_thread(window, image_file_path, center_first_second):
    """
    :param window: 获取窗口信息来改变窗口中空标签的文本来展示运行信息
    :param image_file_path: 文件路径
    :param center_first_second: 中心点、一号点、二号点
    :return: 基本矢量(数组类型)
    """
    window.start_label.config(text="Start to Calculate Basic Vector")
    center_p = int(center_first_second[0])
    first_p = int(center_first_second[1])
    second_p = int(center_first_second[2])
    print(center_p, first_p, second_p)
    cal_cx_cy = side_functions.get_refine_peaks()[0]  # 获取拟合的原子位置，为空时则使用初始位置
    if len(cal_cx_cy) == 0:
        cal_cx_cy = numpy.array(initial_peaks.get_initial_peaks()[0])
    cal_cx = cal_cx_cy[:, 0]  # x
    cal_cy = cal_cx_cy[:, 1]  # y

    cal_m = numpy.empty(shape=[0, 1])
    cal_n = numpy.empty(shape=[0, 1])
    basic_vec_f = numpy.array([[cal_cx[first_p] - cal_cx[center_p],
                                cal_cy[first_p] - cal_cy[center_p]],
                               [cal_cx[second_p] - cal_cx[center_p],
                                cal_cy[second_p] - cal_cy[center_p]]])
    basic_vec_f_inv = numpy.linalg.inv(basic_vec_f)
    center_m, center_n = numpy.dot([cal_cx[center_p], cal_cy[center_p]], basic_vec_f_inv)
    for element_d in range(0, cal_cx.size):
        m, n = numpy.dot([cal_cx[element_d], cal_cy[element_d]], basic_vec_f_inv)
        cal_m = numpy.append(cal_m, m)
        cal_n = numpy.append(cal_n, n)
    cal_mn = numpy.transpose(numpy.stack([cal_m, cal_n]))
    cal_xy = numpy.transpose(numpy.stack([cal_cx, cal_cy]))
    cal_mn_inv = numpy.dot(numpy.linalg.inv(numpy.dot(numpy.transpose(cal_mn), cal_mn)),
                           numpy.transpose(cal_mn))
    basic_vec_s = numpy.array(numpy.dot(cal_mn_inv, cal_xy))
    basic_vector = (basic_vec_s + basic_vec_f) / 2
    basic_vector[0][0] = round(basic_vector[0][0], 7)
    basic_vector[0][1] = round(basic_vector[0][1], 7)
    basic_vector[1][0] = round(basic_vector[1][0], 7)
    basic_vector[1][1] = round(basic_vector[1][1], 7)
    length_basic_vector_one = numpy.sqrt(numpy.square(basic_vector[0][0]) + numpy.square(basic_vector[0][1]))
    length_basic_vector_two = numpy.sqrt(numpy.square(basic_vector[1][0]) + numpy.square(basic_vector[1][1]))
    print(length_basic_vector_one)
    print(length_basic_vector_two)
    print(basic_vector)
    basic_vector_result.append(basic_vector[0])
    basic_vector_result.append(basic_vector[1])
    unit_cell_matrix = open("ResultText\\BasicVectorCalculateResult.txt", 'a+')
    unit_cell_matrix.seek(0)
    lines = len(unit_cell_matrix.readlines())
    if lines > 6:
        unit_cell_matrix.seek(0)
        unit_cell_matrix.truncate()
    unit_cell_matrix.write(str(basic_vector[0, :]).strip('[]'))
    unit_cell_matrix.write('\n')
    unit_cell_matrix.write(str(basic_vector[1, :]).strip('[]'))
    unit_cell_matrix.write('\n')
    unit_cell_matrix.close()
    image = cv2.imread(image_file_path, cv2.IMREAD_GRAYSCALE)
    fig = plt.figure()
    fig.canvas.manager.set_window_title("Basic Vector")
    plt.imshow(image)
    plt.gray()
    for i in range(0, cal_cx.size):
        plt.text(cal_cx[i] + 25, cal_cy[i],
                 (int(round(cal_m[i] - center_m, 0)),
                  int(round(cal_n[i] - center_n, 0))),
                 color='r')
        plt.axis('off')
    plt.show()
    window.end_label.config(text="Finish to Calculate Basic Vector")
    return basic_vector
