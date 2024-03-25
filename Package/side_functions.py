# coding = UTF-8
import os
import threading
import time
import tkinter
from tkinter import messagebox

import numpy
from atomap.api import Sublattice, get_atom_positions
import cv2

import matplotlib.pyplot as plt

from Package import initial_peaks

"""site function is used to refine positions 
which obtained from initial peaks finders, 
and the refine procedure is from atomap"""

refine_positions = []
positions = []
moment = []


def get_refine_peaks():
    """
    :return: refine_positions, moment
    """
    return refine_positions, moment


def refine_peaks():
    threading.Thread(target=side_function_result).start()


def side_function_result():
    """打开写出的本地拟合位置文件"""
    os.startfile(os.getcwd() + "\\ResultText\\RefinePeaks.txt")


def plot(image):
    """
    显示拟合结果
    :param image: 图像路径
    :return: 拟合位置
    """
    if len(refine_positions) == 0:
        return messagebox.showerror(title="Plotting Error", message="Find No Peaks!")
    refine_peaks_path = open("ResultText\\RefinePeaks.txt", "w+")
    for i in range(numpy.array(refine_positions).shape[0]):
        refine_peaks_path.write(str(refine_positions[i, :]).strip("[").strip("]"))
        refine_peaks_path.write("\n")
    refine_peaks_path.close()
    image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title("Positions-Refine")
    plt.imshow(image)
    plt.axis("off")
    i = 0
    for item in refine_positions:
        # if item[0] < 190 and item[1] > 440:
        #     pass
        # else:
        # 原子序号显示
        plt.text(item[0], item[1], i, color="r")
        # 原子点位置标记
        plt.plot(item[0], item[1], marker=".", color="g")
        i += 1
    plt.gray()
    plt.plot()
    plt.show()
    return refine_positions


def site_func_thread(image, window, params):
    threading.Thread(target=site_func_cal, args=(image, window, params)).start()


def site_func(image, window, menu_bar, text_font):
    self = tkinter.Toplevel()
    self.title('Loading Info for Positions Refinement')
    self.geometry("%dx%d" % (600, 100))
    self.config(menu=menu_bar)
    self.resizable(height=False, width=False)

    tkinter.Label(self, text="Separation", font=text_font).place(x=20, y=10)
    self.input_separation = tkinter.StringVar()
    input_separation = tkinter.Entry(self, width=15)
    input_separation.place(x=20, y=35, height=30)

    tkinter.Label(self, text="Threshold", font=text_font).place(x=220, y=10)
    self.threshold = tkinter.StringVar()
    threshold = tkinter.Entry(self, width=15)
    threshold.place(x=200, y=35, height=30)
    params = []

    def __set_params():
        params.append(int(input_separation.get()))
        params.append(float(threshold.get()))

    tkinter.Button(self, text="Confirm", command=__set_params, width=7,
                   font=text_font).place(x=380, y=35, height=30)
    tkinter.Button(self, text="Continue", width=7,
                   command=lambda: site_func_thread(image, window, params),
                   font=text_font).place(x=490, y=35, height=30)
    self.mainloop()
    self.destroy()


# 高斯拟合
def site_func_cal(image, window, params):
    """
    高斯拟合实际计算函数
    :param params: [原子之间的最小间隔, 阈值]
    :param image: 图像路径
    :param window: 主窗口
    :return: 拟合结果
    """
    window.start_label.config(text="Start To Refine Positions")
    global positions, moment
    global refine_positions
    if len(params) != 2:
        params = [5, 0.02]
    try:
        positions = get_atom_positions(image, separation=params[0],
                                       threshold_rel=params[1],
                                       pca=True,
                                       subtract_background=True,
                                       normalize_intensity=True,
                                       remove_too_close_atoms=True)
        start = time.time()
        # positions = initial_peaks.get_initial_peaks()[0]
        sub = Sublattice(positions, image.data)
        sub.find_nearest_neighbors()
        sub.refine_atom_positions_using_center_of_mass(show_progressbar=False)
        sub.refine_atom_positions_using_2d_gaussian(show_progressbar=False)
        refine_positions = sub.atom_positions
        end = time.time()
        moment_result = sub.atom_amplitude_gaussian2d
        for i in range(len(moment_result)):
            moment.append(moment_result[i])
        with open("ResultText/RefinementMoment.txt", "w+") as amplitudes_file:
            for i in range(len(moment_result)):
                amplitudes_file.write(str(i) + " " + str(moment_result[i]) + "\n")
        amplitudes_file.close()
        print('time: ', round((end - start) / 60, 3))
        print('positions_length: ', len(refine_positions))
    finally:
        # 若拟合完成后positions仍为空则使用初始位置
        if len(positions) == 0:
            refine_positions = initial_peaks.get_initial_peaks()[0]
            moment = initial_peaks.get_initial_peaks()[1]
    window.end_label.config(text="Finished, Consuming Time: %s min" % round((end - start) / 60, 3))
