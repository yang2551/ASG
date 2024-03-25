import copy
import os
import threading
from tkinter import messagebox

import cv2
import imutils
import matplotlib.pyplot as plt
import numpy
import scipy.ndimage as ndi
from skimage.feature import blob_log, peak_local_max, blob_dog

import Package

initial_peaks = []
moment = []


def get_initial_peaks():
    """程序中调用该函数获取初始位置和振幅"""
    return initial_peaks, moment


def show_initial_peaks():
    """初始位置展示"""
    threading.Thread(target=initial_peaks_result).start()


def write_initial_peaks():
    """
    将初始位置写出到本地
    :return: No Return
    """
    if len(initial_peaks) == 0:
        return messagebox.showerror(title="Plotting Error", message="Find No Peaks!")
    initial_peaks_path = open("ResultText\\InitialPeaks.txt", "w+")
    for i in range(numpy.array(initial_peaks).shape[0]):
        initial_peaks_path.write(str(initial_peaks[i, :]).strip("[").strip("]"))
        initial_peaks_path.write("\n")
    initial_peaks_path.close()


def initial_peaks_result():
    """打开写出的本地初始位置文件"""
    os.system(os.getcwd() + "\\ResultText\\InitialPeaks.txt")


# 6个函数均通过新线程启动以避免初始位置获取时主界面无响应
def center_of_mass(file, window, mode, threshold):
    threading.Thread(target=center_of_mass_cal, args=(file, window, mode, threshold)).start()


def peak_maximum(self, window, alpha=3.0, distance=10):
    threading.Thread(target=peak_maximum_cal, args=(self, window, alpha, distance)).start()


def peak_minimum(self, window, distance=5.0, threshold=10.0):
    threading.Thread(target=peak_minimum_cal, args=(self, window, distance, threshold)).start()


def difference_gaussian(self, window, minimum_sigma=1, maximum_sigma=20,
                        sigma_ratio=1.6, threshold=0.2, overlap=0.5):
    threading.Thread(target=difference_gaussian_cal, args=(self, window, minimum_sigma, maximum_sigma,
                                                           sigma_ratio, threshold, overlap)).start()


def laplacian_gaussian(self, window, minimum_sigma=1, maximum_sigma=20,
                       number_of_sigma=10, threshold=0.2, overlap=0.5):
    threading.Thread(target=laplacian_gaussian_cal, args=(self, window, minimum_sigma, maximum_sigma,
                                                          number_of_sigma, threshold, overlap)).start()


def local_max(self, window, min_distance=1, threshold=0.02):
    threading.Thread(target=local_max_cal, args=(self, window, min_distance, threshold)).start()


def peaks_plot(image):
    """
    初始位置展示
    :param image: 图像的路径
    :return: No Return
    """
    peaks = initial_peaks
    self = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    if len(peaks) == 0:
        return messagebox.showerror(title="Plotting Error", message="Find No Peaks!")
    plt.ion()
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title("Positions-Initial")
    plt.imshow(self)
    plt.gray()
    plt.axis("off")
    i = 0
    for item in peaks:
        plt.text(item[0], item[1], i, color="r")
        plt.plot(item[0], item[1], marker=".", color="g")
        i += 1
    plt.plot()
    plt.ioff()
    plt.show()
    return peaks


def peak_maximum_cal(self, window, alpha=3.0, distance=10):
    """
    Maximum方法
    :param self: 图像信号
    :param window: 主窗口
    :param alpha: alpha值
    :param distance: 相互距离
    :return: 初始位置
    """
    window.start_label.config(text="Initial Peaks >> Maximum Start To Run")
    self = numpy.array(self)
    storage = []
    copy_image = copy.deepcopy(self)
    center_tag = 0
    sigma = numpy.std(copy_image)
    while True:
        j, i = numpy.unravel_index(numpy.argmax(copy_image), copy_image.shape)
        if copy_image[j, i] >= alpha * sigma:
            storage.append([i, j])
            x = numpy.arange(i - distance, i + distance)
            y = numpy.arange(j - distance, j + distance)
            mesh_x, mesh_y = numpy.meshgrid(x, y)
            copy_image[mesh_y.clip(0, copy_image.shape[0] - 1), mesh_x.clip(0, copy_image.shape[1] - 1)] = 0
            center_tag += 1
        else:
            break
    global initial_peaks
    initial_peaks = numpy.array(storage)
    window.end_label.config(text="Initial Peaks >> Maximum Ends")
    write_initial_peaks()
    return initial_peaks


def peak_minimum_cal(self, window, distance=5.0, threshold=10.0):
    """
    Minimum方法
    :param self: 图像信号
    :param window: 主窗口
    :param distance: 间距
    :param threshold: 阈值
    :return: 初始位置
    """
    window.start_label.config(text="Initial Peaks >> Minimum Start To Run")
    self = numpy.array(self)
    maximum_data = ndi.maximum_filter(self, distance)
    range_maxima = (self == maximum_data)
    minimum_data = ndi.minimum_filter(self, distance)
    difference = ((maximum_data - minimum_data) > threshold)
    range_maxima[difference == 0] = 0
    label, number = ndi.label(range_maxima)
    global initial_peaks
    initial_peaks = numpy.array(
        ndi.center_of_mass(self, label, range(1, number + 1)))
    window.end_label.config(text="Initial Peaks >> Minimum Ends")
    write_initial_peaks()
    return initial_peaks


def difference_gaussian_cal(self, window, minimum_sigma=1, maximum_sigma=20,
                            sigma_ratio=1.6, threshold=0.2, overlap=0.5):
    """
    DoG方法
    :param self: 图像信号
    :param window: 主窗口
    :param minimum_sigma: 高斯核的最小标准差，越小检测到的单元越小
    :param maximum_sigma: 高斯核的最大标准差，越大检测到的单元越大
    :param sigma_ratio: 高斯核的标准差的比值用于DoG的计算
    :param threshold: 尺度空间最大值的绝对下限
    :param overlap: 两个单元的最大重叠比例
    :return: 初始位置
    """
    window.start_label.config(text="Initial Peaks >> DoG Start To Run")
    self = numpy.array(self)
    self = self / numpy.max(self)
    dg_blobs = blob_dog(self,
                        min_sigma=minimum_sigma,
                        max_sigma=maximum_sigma,
                        sigma_ratio=sigma_ratio,
                        threshold=threshold,
                        overlap=overlap)
    try:
        global initial_peaks
        initial_peaks = numpy.round(dg_blobs[:, :2]).astype(int)
        temp = numpy.copy(initial_peaks[:, 0])
        initial_peaks[:, 0] = initial_peaks[:, 1]
        initial_peaks[:, 1] = temp
    except IndexError:
        return messagebox.showerror(title="Method <DoG> Error: ", message="Find No Peaks!")
    window.end_label.config(text="Initial Peaks >> DoG Ends")
    write_initial_peaks()
    return initial_peaks


def laplacian_gaussian_cal(self, window, minimum_sigma=1, maximum_sigma=20,
                           number_of_sigma=10, threshold=0.2, overlap=0.5):
    """
    LoG方法
    :param self: 图像信号
    :param window: 主窗口
    :param minimum_sigma: 高斯核的最小标准差，越小检测到的单元越小
    :param maximum_sigma: 高斯核的最大标准差，越大检测到的单元越大
    :param number_of_sigma: 最大和最小标准差之间要考虑的标准差中间值的数量
    :param threshold: 尺度空间最大值的绝对下限
    :param overlap: 两个单元的最大重叠比例
    :return: 初始位置
    """
    window.start_label.config(text="Initial Peaks >> LoG Start To Run")
    self = numpy.array(self)
    self = self / numpy.max(self)
    if isinstance(number_of_sigma, float):
        return messagebox.showerror(title="Type Error: ",
                                    message="Number of Sigma should be an INTEGER!")
    else:
        lg_blobs = blob_log(self,
                            min_sigma=minimum_sigma,
                            max_sigma=maximum_sigma,
                            num_sigma=number_of_sigma,
                            threshold=threshold,
                            overlap=overlap,
                            log_scale=False)
    try:
        global initial_peaks
        initial_peaks = numpy.round(lg_blobs[:, :2]).astype(int)
        temp = numpy.copy(initial_peaks[:, 0])
        initial_peaks[:, 0] = initial_peaks[:, 1]
        initial_peaks[:, 1] = temp
    except IndexError:
        return messagebox.showerror(title="Method <LoG> Error: ", message="Find No Peaks!")
    window.end_label.config(text="Initial Peaks >> LoG Ends")
    write_initial_peaks()
    return initial_peaks


def local_max_cal(self, window, min_distance=1, threshold=0.02):
    """
    Local Max方法
    :param self: 图像信号
    :param window: 主窗口
    :param min_distance: 两个单元间的最小距离
    :param threshold: 强度最小值
    :return: 初始位置
    """
    window.start_label.config(text="Initial Peaks >> Local Max Start To Run")
    self = numpy.array(self)
    global initial_peaks
    initial_peaks = peak_local_max(self, min_distance, threshold)
    temp = numpy.copy(initial_peaks[:, 0])
    initial_peaks[:, 0] = initial_peaks[:, 1]
    initial_peaks[:, 1] = temp
    window.end_label.config(text="Initial Peaks >> Local Max Ends")
    write_initial_peaks()
    return initial_peaks


def center_of_mass_cal(file_path, window, mode=0, threshold=127):
    """
    CoM方法
    :param file_path: 图像路径
    :param window: 主窗口
    :param mode: 处理模式 "1" - BG(Black); "2" - BG(White)
    :param threshold: 阈值
    :return: 初始位置
    """
    # 根据每个原子点的二值图计算点的初始位置，即质心
    window.start_label.config(text="Initial Peaks >> CoM Start To Run")
    if mode == 0:
        # 背景为黑色时将设置mode为"1"
        mode = Package.get_mode()
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    if mode == "1":
        process_mode = cv2.THRESH_BINARY
    elif mode == "2":
        process_mode = cv2.THRESH_BINARY_INV
    else:
        return messagebox.showerror(title="Process Mode Error",
                                    message="Please check process mode!")
    gaussian_blur = cv2.GaussianBlur(image, (3, 3), 0)
    thresh = cv2.threshold(gaussian_blur, threshold, 255, process_mode)[1]
    # 获取二值图边界
    counts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    counts = imutils.grab_contours(counts)
    peaks = []
    global moment
    file_moment = open("ResultText\\InitialMoment.txt", "w+")
    # 计算质心
    item = 0
    for i in counts:
        moments = cv2.moments(i)
        if moments["m00"] != 0:
            x = moments["m10"] / moments["m00"]
            y = moments["m01"] / moments["m00"]
            if x != 0 and y != 0:
                moment.append(moments["m00"])
                file_moment.write(str(item) + " ")
                file_moment.write(str(moments["m00"]) + "\n")
                peaks.append([x, y])
                item += 1
    file_moment.close()
    global initial_peaks
    initial_peaks = numpy.array(peaks)
    window.end_label.config(text="Initial Peaks >> CoM Ends")
    write_initial_peaks()
    return initial_peaks
