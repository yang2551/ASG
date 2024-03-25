# coding = UTF-8
import tkinter

import matplotlib.pyplot as plt
import numpy
import pyperclip
import cv2

mode = 0


def get_mode():
    return mode


# 背景为黑色时将设置mode为"1"
def black_mode():
    test_mode = "BG(Black)"
    global mode
    mode = "1"
    return mode, test_mode


# 背景为黑色时将设置mode为"2"
def white_mode():
    test_mode = "BG(White)"
    global mode
    mode = "2"
    return mode, test_mode


# 直方图
def hist(file_path_open):
    image = cv2.imread(file_path_open, cv2.IMREAD_GRAYSCALE)
    plt.figure().canvas.manager.set_window_title("Hist")
    plt.hist(image.ravel(), 256)
    plt.axis('on')
    plt.show()


def top_hat(file_path_open):
    kernel = numpy.ones((5, 5), numpy.uint8)
    image = cv2.imread(file_path_open, cv2.IMREAD_GRAYSCALE)
    image = image - cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)
    plt.figure().canvas.manager.set_window_title("TopHat")
    plt.imshow(image)
    plt.gray()
    plt.axis('off')
    plt.show()
    return image


def black_hat(file_path_open):
    kernel = numpy.ones((5, 5), numpy.uint8)
    image = cv2.imread(file_path_open, cv2.IMREAD_GRAYSCALE)
    image = image - cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)
    plt.figure().canvas.manager.set_window_title("BlackHat")
    plt.imshow(image)
    plt.gray()
    plt.axis('off')
    plt.show()
    return image


def erode(file_path_open):
    kernel = numpy.ones((3, 3), numpy.uint8)
    image = cv2.imread(file_path_open, cv2.IMREAD_GRAYSCALE)
    image = cv2.erode(image, kernel, iterations=1)
    plt.figure().canvas.manager.set_window_title("Erode")
    plt.imshow(image)
    plt.gray()
    plt.axis('off')
    plt.show()
    return image


def dilate(file_path_open):
    kernel = numpy.ones((5, 5), numpy.uint8)
    image = cv2.imread(file_path_open, cv2.IMREAD_GRAYSCALE)
    image = cv2.dilate(image, kernel, iterations=1)
    plt.figure().canvas.manager.set_window_title("Dilate")
    plt.imshow(image)
    plt.gray()
    plt.axis('off')
    plt.show()
    return image


def morph_open(file_path_open):
    kernel = numpy.ones((5, 5), numpy.uint8)
    image = cv2.imread(file_path_open, cv2.IMREAD_GRAYSCALE)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    plt.figure().canvas.manager.set_window_title("Morphology--Open")
    plt.imshow(image)
    plt.gray()
    plt.axis('off')
    plt.show()
    return image


def morph_close(file_path_open):
    kernel = numpy.ones((5, 5), numpy.uint8)
    image = cv2.imread(file_path_open, cv2.IMREAD_GRAYSCALE)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    plt.figure().canvas.manager.set_window_title("Morphology--Close")
    plt.imshow(image)
    plt.gray()
    plt.axis('off')
    plt.show()
    return image


def morph_gradient(file_path_open):
    kernel = numpy.ones((5, 5), numpy.uint8)
    image = cv2.imread(file_path_open, cv2.IMREAD_GRAYSCALE)
    image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)
    plt.figure().canvas.manager.set_window_title("Morphology--Gradient")
    plt.imshow(image)
    plt.gray()
    plt.axis('off')
    plt.show()
    return image


# 高斯滤波
def gaussian(file_path_open):
    image = cv2.imread(file_path_open, cv2.IMREAD_GRAYSCALE)
    image = cv2.GaussianBlur(image, (3, 3), 0)
    plt.figure().canvas.manager.set_window_title("Filtration--Gaussian")
    plt.imshow(image)
    plt.gray()
    plt.axis('off')
    plt.show()
    return image


# 中值滤波
def median(file_path_open):
    image = cv2.imread(file_path_open, cv2.IMREAD_GRAYSCALE)
    image = cv2.medianBlur(image, ksize=3)
    plt.figure().canvas.manager.set_window_title("Filtration--Median")
    plt.imshow(image)
    plt.gray()
    plt.axis('off')
    plt.show()
    return image


# 方框滤波
def box_filter(file_path_open):
    image = cv2.imread(file_path_open, cv2.IMREAD_GRAYSCALE)
    image = cv2.boxFilter(image, -1, (3, 3), normalize=True)
    plt.figure().canvas.manager.set_window_title("Filtration--BoxFilter")
    plt.imshow(image)
    plt.gray()
    plt.axis('off')
    plt.show()
    return image


# 均值滤波
def mean_filter(file_path_open):
    image = cv2.imread(file_path_open, cv2.IMREAD_GRAYSCALE)
    image = cv2.blur(image, (3, 3))
    plt.figure().canvas.manager.set_window_title("Filtration--MeanFilter")
    plt.imshow(image)
    plt.gray()
    plt.axis('off')
    plt.show()
    return image


# 高通滤波
def hpf(file_path_open):
    image = cv2.imread(file_path_open)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    discrete_ft = cv2.dft(numpy.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
    discrete_ft_shift = numpy.fft.fftshift(discrete_ft)
    rows, cols = image.shape[:2]
    crow, ccol = int(rows / 2), int(cols / 2)
    mask = numpy.ones((rows, cols, 2), numpy.uint8)
    mask[crow - 30:crow + 30, ccol - 30:ccol + 30] = 0
    for_shift = discrete_ft_shift * mask
    inv_shift = numpy.fft.ifftshift(for_shift)
    inv_img = cv2.idft(inv_shift)
    output = cv2.magnitude(inv_img[:, :, 0], inv_img[:, :, 1])
    plt.figure().canvas.manager.set_window_title("Filtration--HPF")
    plt.imshow(output, 'gray')
    plt.axis('off')
    plt.show()
    return output


# 低通滤波
def lpf(file_path_open):
    image = cv2.imread(file_path_open)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    discrete_ft = cv2.dft(numpy.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
    discrete_ft_shift = numpy.fft.fftshift(discrete_ft)
    rows, cols = image.shape[:2]
    crow, ccol = int(rows / 2), int(cols / 2)
    mask = numpy.zeros((rows, cols, 2), numpy.uint8)
    mask[crow - 30:crow + 30, ccol - 30:ccol + 30] = 1
    for_shift = discrete_ft_shift * mask
    inv_shift = numpy.fft.ifftshift(for_shift)
    inv_img = cv2.idft(inv_shift)
    output = cv2.magnitude(inv_img[:, :, 0], inv_img[:, :, 1])
    plt.figure().canvas.manager.set_window_title("LPF")
    plt.imshow(output, 'gray')
    plt.axis('off')
    plt.show()
    return output


# 离散傅里叶变换
def dft(file_path_open):
    image = cv2.imread(file_path_open)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    discrete_ft = cv2.dft(numpy.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
    discrete_ft_shift = numpy.fft.fftshift(discrete_ft)
    res_dft = 20 * numpy.log(cv2.magnitude(discrete_ft_shift[:, :, 0], discrete_ft_shift[:, :, 1]))
    plt.figure().canvas.manager.set_window_title("Fourier--DFT")
    plt.imshow(res_dft, 'gray')
    plt.axis('off')
    plt.show()
    return res_dft


# 反离散傅里叶变换
def i_dft(file_path_open):
    image = cv2.imread(file_path_open)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    discrete_ft = cv2.dft(numpy.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
    discrete_ft_shift = numpy.fft.fftshift(discrete_ft)
    inv_dis_ft_shift = numpy.fft.ifftshift(discrete_ft_shift)
    inv_img = cv2.idft(inv_dis_ft_shift)
    res_i_dft = 20 * numpy.log(cv2.magnitude(inv_img[:, :, 0], inv_img[:, :, 1]))
    plt.figure().canvas.manager.set_window_title("Fourier--IDFT")
    plt.imshow(res_i_dft, 'gray')
    plt.show()
    return res_i_dft


# 傅里叶变换
def fft(file_path_open):
    image = cv2.imread(file_path_open)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fast_ft = numpy.fft.fft2(image)
    fft_shift = numpy.fft.fftshift(fast_ft)
    fft_img = 20 * numpy.log(1 + numpy.abs(fft_shift))
    plt.figure().canvas.manager.set_window_title("Fourier--FFT")
    plt.imshow(fft_img, 'gray')
    plt.axis('off')
    plt.show()
    return fft_img


# 反离散傅里叶
def i_fft(file_path_open):
    image = cv2.imread(file_path_open)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fast_ft = numpy.fft.fft2(image)
    fft_shift = numpy.fft.fftshift(fast_ft)
    inv_fft = numpy.fft.ifftshift(fft_shift)
    inv_fft_img = numpy.fft.ifft2(inv_fft)
    inv_fft_img = numpy.abs(inv_fft_img)
    plt.figure().canvas.manager.set_window_title("Fourier--IFFT")
    plt.imshow(inv_fft_img, 'gray')
    plt.axis('off')
    plt.show()
    return inv_fft_img


def roberts(file_path_open):
    image = cv2.imread(file_path_open)
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel_x = numpy.array(([[-1, 0], [0, 1]]), dtype=int)
    kernel_y = numpy.array(([0, -1], [1, 0]), dtype=int)
    x = cv2.filter2D(gray_img, cv2.CV_16S, kernel_x)
    y = cv2.filter2D(gray_img, cv2.CV_16S, kernel_y)
    abs_x = cv2.convertScaleAbs(x)
    abs_y = cv2.convertScaleAbs(y)
    robert = cv2.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)
    plt.figure().canvas.manager.set_window_title("Operators--Roberts")
    plt.imshow(robert, 'gray')
    plt.axis('off')
    plt.show()
    return robert


def prewitt(file_path_open):
    image = cv2.imread(file_path_open)
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel_x = numpy.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=int)
    kernel_y = numpy.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=int)
    x = cv2.filter2D(gray_img, cv2.CV_16S, kernel_x)
    y = cv2.filter2D(gray_img, cv2.CV_16S, kernel_y)
    abs_x = cv2.convertScaleAbs(x)
    abs_y = cv2.convertScaleAbs(y)
    pre_witt = cv2.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)
    plt.figure().canvas.manager.set_window_title("Operators--Prewitt")
    plt.imshow(pre_witt, 'gray')
    plt.axis('off')
    plt.show()
    return pre_witt


def sobel(file_path_open):
    image = cv2.imread(file_path_open)
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    x = cv2.Sobel(gray_img, cv2.CV_16S, 1, 0)
    y = cv2.Sobel(gray_img, cv2.CV_16S, 0, 1)
    abs_x = cv2.convertScaleAbs(x)
    abs_y = cv2.convertScaleAbs(y)
    so_bel = cv2.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)
    plt.figure().canvas.manager.set_window_title("Operators--Sobel")
    plt.imshow(so_bel, 'gray')
    plt.axis('off')
    plt.show()
    return so_bel


def laplacian(file_path_open):
    image = cv2.imread(file_path_open)
    gray_pic = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_l = cv2.Laplacian(gray_pic, cv2.CV_16S, ksize=3)
    laplacian_l = cv2.convertScaleAbs(img_l)
    plt.figure().canvas.manager.set_window_title("Operators--Laplacian")
    plt.imshow(laplacian_l, 'gray')
    plt.axis('off')
    plt.show()
    return laplacian_l


def scharr(file_path_open):  # sobel增强
    image = cv2.imread(file_path_open)
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    x = cv2.Sobel(gray_img, cv2.CV_32F, 1, 0)
    y = cv2.Sobel(gray_img, cv2.CV_32F, 0, 1)
    abs_x = cv2.convertScaleAbs(x)
    abs_y = cv2.convertScaleAbs(y)
    scharr_s = cv2.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)
    plt.figure().canvas.manager.set_window_title("Operators--Scharr")
    plt.imshow(scharr_s, 'gray')
    plt.axis('off')
    plt.show()
    return scharr_s


def canny(file_path_open):  # canny
    image = cv2.imread(file_path_open)
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gaussian_c = cv2.GaussianBlur(gray_img, (5, 5), 0)
    canny_c = cv2.Canny(gaussian_c, 127, 255)
    plt.figure().canvas.manager.set_window_title("Operators--Canny")
    plt.imshow(canny_c, 'gray')
    plt.axis('off')
    plt.show()
    return canny_c


def lo_g(file_path_open):
    image = cv2.imread(file_path_open)
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gaussian_c = cv2.GaussianBlur(gray_img, (5, 5), 0)
    img_log = cv2.Laplacian(gaussian_c, cv2.CV_16S, ksize=3)
    log = cv2.convertScaleAbs(img_log)
    plt.figure().canvas.manager.set_window_title("Operators--LoG")
    plt.imshow(log, 'gray')
    plt.axis('off')
    plt.show()
    return log


def max_scale(file_path_open):
    image = cv2.imread(file_path_open)
    height, width = image.shape[:2]
    empty = numpy.zeros((height, width, 3), numpy.uint8)
    for i in range(height):
        for j in range(width):
            gray = max(image[i, j][0], image[i, j][1], image[i, j][2])
            empty[i, j] = numpy.uint8(gray)
    plt.figure().canvas.manager.set_window_title("Grayscale--Max")
    plt.imshow(empty, 'gray')
    plt.axis('off')
    plt.show()
    return empty


def mean_scale(file_path_open):
    image = cv2.imread(file_path_open)
    height, width = image.shape[:2]
    empty = numpy.zeros((height, width, 3), numpy.uint8)
    for i in range(height):
        for j in range(width):
            gray = (int(image[i, j][0]) + int(image[i, j][1]) + int(image[i, j][2])) / 3
            empty[i, j] = numpy.uint8(gray)
    plt.figure().canvas.manager.set_window_title("Grayscale--Mean")
    plt.imshow(empty, 'gray')
    plt.axis('off')
    plt.show()
    return empty


def weighted_scale(file_path_open):
    image = cv2.imread(file_path_open)
    height, width = image.shape[:2]
    empty = numpy.zeros((height, width, 3), numpy.uint8)
    for i in range(height):
        for j in range(width):
            gray = 0.30 * image[i, j][0] + 0.59 * image[i, j][1] + 0.11 * image[i, j][2]
            gray = numpy.squeeze(gray)
            empty[i, j] = numpy.uint8(gray)
    plt.figure().canvas.manager.set_window_title("Grayscale--Weighted")
    plt.imshow(empty, 'gray')
    plt.axis('off')
    plt.show()
    return empty


def non_linear(file_path_open):
    image = cv2.imread(file_path_open, cv2.IMREAD_GRAYSCALE)
    height, width = image.shape[:2]
    empty = numpy.zeros((height, width, 3), numpy.uint8)
    for i in range(height):
        for j in range(width):
            gray = int(image[i, j]) * int(image[i, j]) / 255
            empty[i, j] = numpy.uint8(gray)
    plt.figure().canvas.manager.set_window_title("Grayscale--NoneLinear")
    plt.imshow(empty, 'gray')
    plt.axis('off')
    plt.show()
    return empty


def bgr_rgb(file_path_open):
    image = cv2.imread(file_path_open)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.figure().canvas.manager.set_window_title("BGR-RGB")
    plt.imshow(image)
    plt.axis('off')
    plt.show()


def rgb_bgr(file_path_open):
    image = cv2.imread(file_path_open)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    plt.figure().canvas.manager.set_window_title("RGB-BGR")
    plt.imshow(image)
    plt.axis('off')
    plt.show()


def bgr_gray(file_path_open):
    image = cv2.imread(file_path_open)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plt.figure().canvas.manager.set_window_title("BGR-GRAY")
    plt.imshow(image)
    plt.axis('off')
    plt.show()


def rgb_gray(file_path_open):
    image = cv2.imread(file_path_open)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    plt.figure().canvas.manager.set_window_title("RGB-GRAY")
    plt.imshow(image)
    plt.axis('off')
    plt.show()


def bgr_xyz(file_path_open):
    image = cv2.imread(file_path_open)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2XYZ)
    plt.figure().canvas.manager.set_window_title("BGR-XYZ")
    plt.imshow(image)
    plt.axis('off')
    plt.show()


def xyz_bgr(file_path_open):
    image = cv2.imread(file_path_open)
    image = cv2.cvtColor(image, cv2.COLOR_XYZ2BGR)
    plt.figure().canvas.manager.set_window_title("XYZ-BGR")
    plt.imshow(image)
    plt.axis('off')
    plt.show()


def bgr_hls(file_path_open):
    image = cv2.imread(file_path_open)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    plt.figure().canvas.manager.set_window_title("BGR-HLS")
    plt.imshow(image)
    plt.axis('off')
    plt.show()


def bgr_hsv(file_path_open):
    image = cv2.imread(file_path_open)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    plt.figure().canvas.manager.set_window_title("BGR-HSV")
    plt.imshow(image)
    plt.axis('off')
    plt.show()


# 关于
def about():
    top = tkinter.Toplevel()
    top.title('About')
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    width_w = 350
    height_w = 160
    left = (screen_width - width_w) / 2
    right = (screen_height - height_w) / 2
    top.geometry("%dx%d+%d+%d" % (width_w, height_w, left, right))
    top.attributes('-topmost', True)
    top.resizable(False, False)
    tkinter.Label(top, text='AutoSGD'
                            '\nVersion: 1.0 (64-bit)'
                            '\nE-mail: l19791215@outlook.com'
                            '\nInstitution: XTU'
                            '\nAuthor: Nathan',
                  justify='center', bg="white",
                  font=('Times New Roman', 15),
                  compound='center').pack()
    pyperclip.copy("l19791215@outlook.com")
    top.mainloop()
