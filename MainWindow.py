import os
import sys
import tkinter
from tkinter import filedialog, ttk, messagebox

import cv2
import hyperspy.api as hyper_spy
import numpy
from PIL import Image, ImageTk
import ctypes

import Package
from Package import basic_vector_calculate, initial_peaks
from Package import match_plane_group, match_space_group
import Package.real_space_parameters as real_space_parameter
from Package import side_functions
from Package.initial_peaks import center_of_mass, local_max
from Package.initial_peaks import difference_gaussian, laplacian_gaussian
from Package.initial_peaks import peak_minimum, peak_maximum
from Package.real_space_parameters import load_pixels_length_to_calculate


def get_real_space_params_from_main_window():
    return real_space_params


# 文件导入窗口，路径不要有中文
class NewOpenImport(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('Image')
        self.parent = parent
        width_w = 600
        height_w = 550
        # 窗口大小
        self.geometry("%dx%d+%d+%d" % (width_w, height_w, 10, 150))
        default_dir_nop = u'Path'
        global image_path, signals
        #  文件选择
        image_path = filedialog.askopenfilename(
            title=u'Select',
            # 图像类型
            filetypes=[('TIF', 'tif'),
                       ('JPG', 'jpg'),
                       ('PNG', 'png'),
                       ('All Files', '.*')],
            initialdir=os.path.expanduser(default_dir_nop),
            defaultextension='.tif')
        # 将图像大小设置为子窗口的大小
        if len(image_path) != 0:
            image = Image.open(image_path).resize((600, 600))
            if image.size[1] >= 600:
                image = image.resize((600, 600), Image.ADAPTIVE)
            global image_load
            image_load = ImageTk.PhotoImage(image)
            label_image_load = tkinter.Label(
                self, height=600, width=600, image=image_load)
            label_image_load.pack()
            # 将主界面的菜单引入
            self.config(menu=menu_bar)
            # Signal2D数据，为部分初始位置获取方法及二维高斯拟合所需数据
            signals = hyper_spy.signals.Signal2D(cv2.imread(image_path, cv2.IMREAD_GRAYSCALE))
        else:
            messagebox.showinfo(title="Info", message="Please Load Image!")


class Search(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('Search')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width_w = 700
        height_w = 350
        left = (screen_width - width_w) / 2
        top = (screen_height - height_w) / 2
        self.geometry("%dx%d+%d+%d" % (width_w, height_w, left, top))
        self.resizable(height=False, width=False)
        self.config(menu=menu_bar)
        self.parent = parent

        def __go_system(*args):
            global lattice, directions_in
            lattice = "Triclinic"
            lattice = combobox_list.get()
            if lattice == "Triclinic" or lattice == "Monoclinic" or lattice == "Orthorhombic":
                tkinter.Label(self, width=18, text="[001]", font=text_font).place(x=345, y=170)
                tkinter.Label(self, width=18, text="[100]", font=text_font).place(x=345, y=200)
                tkinter.Label(self, width=18, text="[010]", font=text_font).place(x=345, y=230)
                tkinter.Label(self, width=18, text="[001]", font=text_font).place(x=350, y=40)
                tkinter.Label(self, width=18, text="[100]", font=text_font).place(x=350, y=70)
                tkinter.Label(self, width=18, text="[010]", font=text_font).place(x=350, y=100)
                directions_in.append("001")
                directions_in.append("100")
                directions_in.append("010")
            if lattice == "Tetragonal":
                tkinter.Label(self, width=18, text="[001]", font=text_font).place(x=345, y=170)
                tkinter.Label(self, width=18, text="[100]", font=text_font).place(x=345, y=200)
                tkinter.Label(self, width=18, text="[110]", font=text_font).place(x=345, y=230)
                tkinter.Label(self, width=18, text="[001]", font=text_font).place(x=350, y=40)
                tkinter.Label(self, width=18, text="[100]", font=text_font).place(x=350, y=70)
                tkinter.Label(self, width=18, text="[110]", font=text_font).place(x=350, y=100)
                directions_in.append("001")
                directions_in.append("100")
                directions_in.append("110")
            if lattice == "Cubic":
                tkinter.Label(self, width=18, text="[001]", font=text_font).place(x=345, y=170)
                tkinter.Label(self, width=18, text="[111]", font=text_font).place(x=345, y=200)
                tkinter.Label(self, width=18, text="[110]", font=text_font).place(x=345, y=230)
                tkinter.Label(self, width=18, text="[001]", font=text_font).place(x=350, y=40)
                tkinter.Label(self, width=18, text="[111]", font=text_font).place(x=350, y=70)
                tkinter.Label(self, width=18, text="[110]", font=text_font).place(x=350, y=100)
                directions_in.append("001")
                directions_in.append("111")
                directions_in.append("110")
            if lattice == "Trigonal" or lattice == "Hexagonal":
                tkinter.Label(self, width=18, text="[001]", font=text_font).place(x=345, y=170)
                tkinter.Label(self, width=18, text="[100]", font=text_font).place(x=345, y=200)
                tkinter.Label(self, width=18, text="[210]", font=text_font).place(x=345, y=230)
                tkinter.Label(self, width=18, text="[001]", font=text_font).place(x=350, y=40)
                tkinter.Label(self, width=18, text="[100]", font=text_font).place(x=350, y=70)
                tkinter.Label(self, width=18, text="[210]", font=text_font).place(x=350, y=100)
                directions_in.append("001")
                directions_in.append("100")
                directions_in.append("210")
            return lattice

        self.combobox_list = tkinter.StringVar()
        combobox_list = ttk.Combobox(self, width=14, textvariable=self.combobox_list, font=text_font)
        combobox_list['values'] = ('Triclinic', 'Monoclinic',
                                   'Orthorhombic', 'Tetragonal',
                                   'Cubic', 'Trigonal', 'Hexagonal')
        combobox_list.current(0)
        combobox_list.bind("<<ComboboxSelected>>", __go_system)
        combobox_list.place(x=175, y=10)
        tkinter.Label(self, width=18, text='Crystal System', font=text_font).place(x=5, y=10)
        tkinter.Label(self, width=18, text='Bravais', font=text_font).place(x=5, y=70)
        self.bravais_text = tkinter.StringVar()
        bravais_text = tkinter.Entry(self, width=18)
        bravais_text.place(x=175, y=70)

        tkinter.Label(self, width=18, text='Lattice Params', font=text_font).place(x=5, y=140)
        tkinter.Label(self, width=18, text='a (Å)', font=text_font).place(x=5, y=170)
        tkinter.Label(self, width=18, text='b (Å)', font=text_font).place(x=5, y=200)
        tkinter.Label(self, width=18, text='c (Å)', font=text_font).place(x=5, y=230)
        self.ua_text = tkinter.StringVar()
        ua_text = tkinter.Entry(self, width=18)
        ua_text.place(x=175, y=170)
        self.ub_text = tkinter.StringVar()
        ub_text = tkinter.Entry(self, width=18)
        ub_text.place(x=175, y=200)
        self.uc_text = tkinter.StringVar()
        uc_text = tkinter.Entry(self, width=18)
        uc_text.place(x=175, y=230)
        primitive_cell_para_label = tkinter.Label(self, width=18,
                                                  text='Reciprocal Params', font=text_font)
        primitive_cell_para_label.place(x=350, y=10)
        self.pa_text = tkinter.StringVar()
        pa_text = tkinter.Entry(self, width=18)
        pa_text.place(x=520, y=40)
        self.pb_text = tkinter.StringVar()
        pb_text = tkinter.Entry(self, width=18)
        pb_text.place(x=520, y=70)
        self.pc_text = tkinter.StringVar()
        pc_text = tkinter.Entry(self, width=18)
        pc_text.place(x=520, y=100)
        tkinter.Label(self, width=18, text='Plane Group', font=text_font).place(x=350, y=140)
        self.pg_entry_first = tkinter.StringVar()
        pg_entry_first = tkinter.Entry(self, width=18)
        pg_entry_first.place(x=520, y=170)
        self.pg_entry_second = tkinter.StringVar()
        pg_entry_second = tkinter.Entry(self, width=18)
        pg_entry_second.place(x=520, y=200)
        self.pg_entry_third = tkinter.StringVar()
        pg_entry_third = tkinter.Entry(self, width=18)
        pg_entry_third.place(x=520, y=230)

        def space_group_search():
            global symmetry_in
            main_win.start_label.config(text="Searching Space Group")
            lattice_in = lattice
            bravais_in = bravais_text.get()
            unit_cell_a = ua_text.get()
            if len(unit_cell_a) != 0:
                unit_cell_a = float(ua_text.get())
            unit_cell_b = ub_text.get()
            if len(unit_cell_b) != 0:
                unit_cell_b = float(ub_text.get())
            unit_cell_c = uc_text.get()
            if len(unit_cell_c) != 0:
                unit_cell_c = float(uc_text.get())
            primitive_cell_a = pa_text.get()
            primitive_cell_b = pb_text.get()
            primitive_cell_c = pc_text.get()
            if len(primitive_cell_a) != 0:
                primitive_cell_a = numpy.array(pa_text.get().split(" "), dtype=float)
            if len(primitive_cell_b) != 0:
                primitive_cell_b = numpy.array(pb_text.get().split(" "), dtype=float)
            if len(primitive_cell_c) != 0:
                primitive_cell_c = numpy.array(pc_text.get().split(" "), dtype=float)
            reciprocal_params = [primitive_cell_a, primitive_cell_b, primitive_cell_c]
            if len(pg_entry_first.get()) != 0:
                symmetry_in.append(str(pg_entry_first.get()))
            if len(pg_entry_second.get()) != 0:
                symmetry_in.append(str(pg_entry_second.get()))
            if len(pg_entry_third.get()) != 0:
                symmetry_in.append(str(pg_entry_third.get()))
            real_space_params_in = [lattice_in, unit_cell_a, unit_cell_b, unit_cell_c, bravais_in]
            match_space_group.para_match(window=main_win, load_lattice=lattice_in,
                                         real_space_params_in=real_space_params_in,
                                         symmetry_in=symmetry_in, directions_in=directions_in,
                                         reciprocal_params_in=reciprocal_params)
            main_win.end_label.config(text="Finish Searching Space Group")

        tkinter.Label(self, text="Reciprocal Params Should be Separated by Blank Space!",
                      font=("Times New Roman", 10, "bold", "underline")).place(x=5, y=265)
        tkinter.Button(self, text="Confirm", width=10, font=text_font,
                       command=space_group_search).place(x=310, y=300)


# 初始位置获取
class InitialPeaksFinder(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('Initial Peaks Finders')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width_w = 690
        height_w = 300
        left = (screen_width - width_w) / 2
        top = (screen_height - height_w) / 2
        self.geometry("%dx%d+%d+%d" % (width_w, height_w, left, top))
        self.config(menu=menu_bar)
        self.parent = parent
        self.resizable(height=False, width=False)

        tkinter.Label(self, text="Maximum", width=10).place(x=0, y=20)
        tkinter.Label(self, text="Alpha", width=10).place(x=100, y=0)
        tkinter.Label(self, text="Distance", width=10).place(x=200, y=0)
        tkinter.Label(self, text="Minimum", width=10).place(x=0, y=70)
        tkinter.Label(self, text="Distance", width=10).place(x=100, y=50)
        tkinter.Label(self, text="Threshold", width=10).place(x=200, y=50)
        tkinter.Label(self, text="DoG", width=10).place(x=0, y=120)
        tkinter.Label(self, text="MinSigma", width=10).place(x=100, y=100)
        tkinter.Label(self, text="MaxSigma", width=10).place(x=200, y=100)
        tkinter.Label(self, text="SigmaRatio", width=10).place(x=300, y=100)
        tkinter.Label(self, text="Threshold", width=10).place(x=400, y=100)
        tkinter.Label(self, text="Overlap", width=10).place(x=500, y=100)
        tkinter.Label(self, text="LoG", width=10).place(x=0, y=170)
        tkinter.Label(self, text="MinSigma", width=10).place(x=100, y=150)
        tkinter.Label(self, text="MaxSigma", width=10).place(x=200, y=150)
        tkinter.Label(self, text="SigmaNums", width=10).place(x=300, y=150)
        tkinter.Label(self, text="Threshold", width=10).place(x=400, y=150)
        tkinter.Label(self, text="Overlap", width=10).place(x=500, y=150)
        tkinter.Label(self, text="LocalMax", width=10).place(x=0, y=220)
        tkinter.Label(self, text="MinDistance", width=10).place(x=100, y=200)
        tkinter.Label(self, text="Threshold", width=10).place(x=200, y=200)
        tkinter.Label(self, text="CoM", width=10).place(x=0, y=270)
        tkinter.Label(self, text="Mode", width=10).place(x=100, y=250)
        tkinter.Label(self, text="Threshold", width=10).place(x=200, y=250)
        tkinter.Label(self, text="Mode: 1-BG(Black); 2-BG(White)").place(x=320, y=270)
        self.alpha = tkinter.StringVar()
        alpha = tkinter.Entry(self, width=10, textvariable=self.alpha)
        alpha.place(x=100, y=20)
        self.max_distance = tkinter.StringVar()
        max_distance = tkinter.Entry(self, width=10, textvariable=self.max_distance)
        max_distance.place(x=200, y=20)
        self.min_distance = tkinter.StringVar()
        min_distance = tkinter.Entry(self, width=10, textvariable=self.min_distance)
        min_distance.place(x=100, y=70)
        self.min_threshold = tkinter.StringVar()
        min_threshold = tkinter.Entry(self, width=10, textvariable=self.min_threshold)
        min_threshold.place(x=200, y=70)
        self.dog_min_sigma = tkinter.StringVar()
        dog_min_sigma = tkinter.Entry(self, width=10, textvariable=self.dog_min_sigma)
        dog_min_sigma.place(x=100, y=120)
        self.dog_max_sigma = tkinter.StringVar()
        dog_max_sigma = tkinter.Entry(self, width=10, textvariable=self.dog_max_sigma)
        dog_max_sigma.place(x=200, y=120)
        self.sigma_ratio = tkinter.StringVar()
        sigma_ratio = tkinter.Entry(self, width=10, textvariable=self.sigma_ratio)
        sigma_ratio.place(x=300, y=120)
        self.dog_threshold = tkinter.StringVar()
        dog_threshold = tkinter.Entry(self, width=10, textvariable=self.dog_threshold)
        dog_threshold.place(x=400, y=120)
        self.dog_overlap = tkinter.StringVar()
        dog_overlap = tkinter.Entry(self, width=10, textvariable=self.dog_overlap)
        dog_overlap.place(x=500, y=120)
        self.log_min_sigma = tkinter.StringVar()
        log_min_sigma = tkinter.Entry(self, width=10, textvariable=self.log_min_sigma)
        log_min_sigma.place(x=100, y=170)
        self.log_max_sigma = tkinter.StringVar()
        log_max_sigma = tkinter.Entry(self, width=10, textvariable=self.log_max_sigma)
        log_max_sigma.place(x=200, y=170)
        self.sigma_numbers = tkinter.StringVar()
        sigma_numbers = tkinter.Entry(self, width=10, textvariable=self.sigma_numbers)
        sigma_numbers.place(x=300, y=170)
        self.log_threshold = tkinter.StringVar()
        log_threshold = tkinter.Entry(self, width=10, textvariable=self.log_threshold)
        log_threshold.place(x=400, y=170)
        self.log_overlap = tkinter.StringVar()
        log_overlap = tkinter.Entry(self, width=10, textvariable=self.log_overlap)
        log_overlap.place(x=500, y=170)
        self.local_distance = tkinter.StringVar()
        local_distance = tkinter.Entry(self, width=10, textvariable=self.local_distance)
        local_distance.place(x=100, y=220)
        self.local_threshold = tkinter.StringVar()
        local_threshold = tkinter.Entry(self, width=10, textvariable=self.local_threshold)
        local_threshold.place(x=200, y=220)
        self.mode = tkinter.StringVar()
        com_mode = tkinter.Entry(self, width=10, textvariable=self.mode)
        com_mode.place(x=100, y=270)
        self.com_threshold = tkinter.StringVar()
        com_threshold = tkinter.Entry(self, width=10, textvariable=self.com_threshold)
        com_threshold.place(x=200, y=270)
        tkinter.Button(self, text="Run", width=5,
                       command=self.__maximum_run).place(x=625, y=15)
        tkinter.Button(self, text="Run", width=5,
                       command=self.__minimum_run).place(x=625, y=65)
        tkinter.Button(self, text="Run", width=5,
                       command=self.__dog_run).place(x=625, y=115)
        tkinter.Button(self, text="Run", width=5,
                       command=self.__log_run).place(x=625, y=165)
        tkinter.Button(self, text="Run", width=5,
                       command=self.__local_run).place(x=625, y=215)
        tkinter.Button(self, text="Run", width=5,
                       command=self.__com_run).place(x=625, y=265)

    def __maximum_run(self):
        alpha = float(self.alpha.get())
        distance = int(self.max_distance.get())
        peaks = peak_maximum(signals, main_win, alpha, distance)
        return peaks

    # 获取子窗口输入的数据进行初始位置的获取
    def __minimum_run(self):
        distance = float(self.min_distance.get())
        threshold = float(self.min_threshold.get())
        peaks = peak_minimum(signals, main_win, distance, threshold)
        return peaks

    def __dog_run(self):
        min_sigma = int(self.dog_min_sigma.get())
        max_sigma = int(self.dog_max_sigma.get())
        sigma_ratio = float(self.sigma_ratio.get())
        threshold = float(self.dog_threshold.get())
        overlap = float(self.dog_overlap.get())
        peaks = difference_gaussian(signals, main_win, min_sigma, max_sigma,
                                    sigma_ratio, threshold, overlap)
        return peaks

    def __log_run(self):
        min_sigma = int(self.log_min_sigma.get())
        max_sigma = int(self.log_max_sigma.get())
        sigma_numbers = int(self.sigma_numbers.get())
        threshold = float(self.log_threshold.get())
        overlap = float(self.log_overlap.get())
        peaks = laplacian_gaussian(signals, main_win, min_sigma, max_sigma,
                                   sigma_numbers, threshold, overlap)
        return peaks

    def __local_run(self):
        distance = int(self.local_distance.get())
        peaks = local_max(signals, main_win, distance)
        return peaks

    def __com_run(self):
        process_mode = self.mode.get()
        threshold = int(self.com_threshold.get())
        peaks = center_of_mass(image_path, main_win, process_mode, threshold)
        return peaks


# 晶格参数导入
class LoadParams(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('Load Real Space Params')
        self.geometry("%dx%d" % (650, 100))
        self.config(menu=menu_bar)
        self.parent = parent
        self.resizable(height=False, width=False)
        tkinter.Label(self, text="Length(Å)", font=text_font).place(x=20, y=10)
        self.length_abc = tkinter.StringVar()
        length_abc = tkinter.Entry(self, width=25)
        length_abc.place(x=20, y=35, height=30)

        tkinter.Label(self, text="Degrees(°)", font=text_font).place(x=280, y=10)
        self.value_degrees = tkinter.StringVar()
        value_degrees = tkinter.Entry(self, width=25)
        value_degrees.place(x=280, y=35, height=30)

        tkinter.Label(self, text="Separate each params by Blank Space!",
                      font=("Times New Roman", 10, "bold", "underline")).place(x=20, y=70)

        global real_space_params
        real_space_params = []

        def __get_params():
            real_space_params_length = length_abc.get().split(" ")
            for i in range(len(real_space_params_length)):
                real_space_params.append(float(real_space_params_length[i]))
            real_space_params_degrees = value_degrees.get().split(" ")
            for i in range(len(real_space_params_degrees)):
                real_space_params.append(float(real_space_params_degrees[i]))
            if len(real_space_params) != 6:
                messagebox.showinfo(title="Info", message="Length of real space params != 6")
            else:
                real_a = real_space_params[0]
                real_b = real_space_params[1]
                real_c = real_space_params[2]
                real_alpha = real_space_params[3]
                real_beta = real_space_params[4]
                real_gamma = real_space_params[5]
                real_length_ab = abs(real_a - real_b)
                real_length_bc = abs(real_b - real_c)
                alpha_error = abs(real_alpha - 90)
                beta_error = abs(real_beta - 90)
                gamma_error = abs(real_gamma - 90)
                lambda_error = abs(real_gamma - 120)
                global lattice
                if real_length_ab > 0.1:
                    if alpha_error <= 1 and gamma_error <= 1:
                        if beta_error <= 1:
                            lattice = 'orthorhombic'
                        else:
                            lattice = 'monoclinic'
                    else:
                        lattice = 'triclinic'
                else:
                    if real_length_bc > 0.1:
                        if lambda_error < 1:
                            lattice = 'hexagonal'
                        else:
                            lattice = 'tetragonal'
                    else:
                        if gamma_error > 1:
                            lattice = 'trigonal'
                        else:
                            lattice = 'cubic'
                print(lattice)
        tkinter.Button(self, text="Confirm", command=__get_params,
                       font=text_font).place(x=530, y=35, height=30)


# 程序主入口
if __name__ == '__main__':
    kernel = numpy.ones((5, 5), numpy.uint8)
    directions_in = []
    symmetry_in = []
    image_load = None
    default_dir = u'Path'
    lattice = None
    text_font = ("Times New Roman", 10)
    image_path = None
    signals = None
    real_space_params = []
    points = None
    tol_r_err = pow(10, -2)
    tor_error = 1


    class MainWindow(tkinter.Toplevel):
        # 该类包含主窗口和其它子窗口的设置
        def __init__(self):
            super().__init__()
            self.title('AutoSGD')
            self.geometry("%dx%d" % (600, 40))
            # 空标签，后续使用某个函数时更改text中的文本以实现在主窗口中显示执行信息
            self.start_label = tkinter.Label(self, text="", font=text_font)
            self.start_label.pack()
            self.end_label = tkinter.Label(self, text="", font=text_font)
            self.end_label.pack()
            self.resizable(height=False, width=False)
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
            scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
            self.tk.call('tk', 'scaling', scale_factor / 75)
            self.__setup_ui()

        # 主界面的设计，各菜单点击时的函数调用
        def __setup_ui(self):
            global menu_bar
            menu_bar = tkinter.Menu(self)
            file_menu = tkinter.Menu(menu_bar, tearoff=0)  # 文件导入
            mode_menu = tkinter.Menu(menu_bar, tearoff=0)  # 处理模式选择
            peak_menu = tkinter.Menu(menu_bar, tearoff=0)  # 原子位置获取和拟合
            calculate_menu = tkinter.Menu(menu_bar, tearoff=0)  # 所需信息计算
            result_menu = tkinter.Menu(menu_bar, tearoff=0)  # 计算结果
            operations_menu = tkinter.Menu(menu_bar, tearoff=0)  # 直方图等处理
            menu_bar.add_cascade(label='File', menu=file_menu)
            file_menu.add_command(label='New', command=self.new_open_import)
            file_menu.add_command(label="Load Params", command=self.load_params)
            file_menu.add_command(label='Exit', command=sys.exit)

            menu_bar.add_cascade(label="Mode", menu=mode_menu)
            mode_menu.add_command(label="BG(Black)", command=Package.black_mode)
            mode_menu.add_command(label="BG(White)", command=Package.white_mode)
            menu_bar.add_cascade(label='Peaks Finders', menu=peak_menu)
            peak_menu.add_command(label="Initial Peaks", command=self.peaks_finder)
            peak_menu.add_command(label="Initial Result",
                                  command=lambda: initial_peaks.peaks_plot(image_path))
            peak_menu.add_command(label="Refinement",
                                  command=lambda: side_functions.site_func(
                                      signals, main_win, menu_bar, text_font))
            peak_menu.add_command(
                label='Refinement Result', command=lambda: side_functions.plot(image_path))
            menu_bar.add_cascade(label="Calculate", menu=calculate_menu)
            calculate_menu.add_command(label="Search", command=self.search)
            # 计算基本矢量
            calculate_menu.add_command(label="Basic Vectors",
                                       command=lambda: basic_vector_calculate.load_points_to_calculate_matrix(
                                           main_win, image_path, text_font, menu_bar))
            # 计算实空间参数
            calculate_menu.add_command(label="Real Space Parameters",
                                       command=lambda:
                                       load_pixels_length_to_calculate(main_win, tol_r_err, text_font, menu_bar))
            # 二维平面群信息
            calculate_menu.add_command(label="Plane Group",
                                       command=lambda: match_plane_group.load_info_to_calculate_plane_group(
                                           main_win, lattice, image_path, text_font, menu_bar))
            # 查找三维空间群
            calculate_menu.add_command(label="Space Group",
                                       command=lambda: match_space_group.para_match(main_win, lattice))
            menu_bar.add_cascade(label="Result", menu=result_menu)
            result_menu.add_command(label="Initial Peaks",
                                    command=initial_peaks.show_initial_peaks)
            result_menu.add_command(label="Refine Peaks",
                                    command=Package.side_functions.refine_peaks)
            result_menu.add_command(label="Basic Vectors",
                                    command=basic_vector_calculate.show_matrix)
            result_menu.add_command(label="Parameters",
                                    command=real_space_parameter.show_parameters)
            result_menu.add_command(label="Plane Group",
                                    command=match_plane_group.show_plane_group)
            result_menu.add_command(label="Space Group",
                                    command=match_space_group.show_space_group)
            menu_bar.add_cascade(label='Operations',
                                 menu=operations_menu)
            morphology = tkinter.Menu(operations_menu, tearoff=0)
            operations_menu.add_command(label='Histogram',
                                        command=lambda: Package.hist(image_path))
            operations_menu.add_cascade(label='Morphology',
                                        menu=morphology)
            morphology.add_command(label='TopHat',
                                   command=lambda: Package.top_hat(image_path))
            morphology.add_command(label='BlackHat',
                                   command=lambda: Package.black_hat(image_path))
            morphology.add_separator()
            morphology.add_command(label='Erode',
                                   command=lambda: Package.erode(image_path))
            morphology.add_command(label='Dilate',
                                   command=lambda: Package.dilate(image_path))
            morphology.add_separator()
            morphology.add_command(label='Open',
                                   command=lambda: Package.morph_open(image_path))
            morphology.add_command(label='Close',
                                   command=lambda: Package.morph_close(image_path))
            morphology.add_command(label='Gradient',
                                   command=lambda: Package.morph_gradient(image_path))
            filtration = tkinter.Menu(operations_menu, tearoff=0)
            operations_menu.add_cascade(label='Filtration',
                                        menu=filtration)
            filtration.add_command(label='Gaussian',
                                   command=lambda: Package.gaussian(image_path))
            filtration.add_command(label='Median',
                                   command=lambda: Package.median(image_path))
            filtration.add_command(label='BoxFilter',
                                   command=lambda: Package.box_filter(image_path))
            filtration.add_command(label='MeanFilter',
                                   command=lambda: Package.mean_filter(image_path))
            filtration.add_command(label='HPF',
                                   command=lambda: Package.hpf(image_path))
            filtration.add_command(label='LPF',
                                   command=lambda: Package.lpf(image_path))
            fourier = tkinter.Menu(operations_menu, tearoff=0)
            operations_menu.add_cascade(label='Fourier',
                                        menu=fourier)
            fourier.add_command(label='DFT',
                                command=lambda: Package.dft(image_path))
            fourier.add_command(label='IDFT',
                                command=lambda: Package.i_dft(image_path))
            fourier.add_separator()
            fourier.add_command(label='FFT',
                                command=lambda: Package.fft(image_path))
            fourier.add_command(label='IFFT',
                                command=lambda: Package.i_fft(image_path))
            operator = tkinter.Menu(operations_menu, tearoff=0)
            operations_menu.add_cascade(label='Operators',
                                        menu=operator)
            operator.add_command(label='Roberts',
                                 command=lambda: Package.roberts(image_path))
            operator.add_command(label='Prewitt',
                                 command=lambda: Package.prewitt(image_path))
            operator.add_separator()
            operator.add_command(label='Sobel',
                                 command=lambda: Package.sobel(image_path))
            operator.add_command(label='Laplacian',
                                 command=lambda: Package.laplacian(image_path))
            operator.add_separator()
            operator.add_command(label='Scharr',
                                 command=lambda: Package.scharr(image_path))
            operator.add_command(label='Canny',
                                 command=lambda: Package.canny(image_path))
            operator.add_command(label='LoG',
                                 command=lambda: Package.lo_g(image_path))
            grayscale = tkinter.Menu(operations_menu, tearoff=0)
            operations_menu.add_cascade(label='Grayscale',
                                        menu=grayscale)
            grayscale.add_command(label='Max',
                                  command=lambda: Package.max_scale(image_path))
            grayscale.add_command(label='Mean',
                                  command=lambda: Package.mean_scale(image_path))
            grayscale.add_command(label='Weighted Mean',
                                  command=lambda: Package.weighted_scale(image_path))
            grayscale.add_separator()
            grayscale.add_command(label='Non-linear',
                                  command=lambda: Package.non_linear(image_path))
            menu_bar.add_command(label='Help', command=Package.about)
            menu_bar.add_command(label="Exit", command=sys.exit)
            self.config(menu=menu_bar)

        # 等待并获取子窗口中输入的参数
        def new_open_import(self):
            self.wait_window(NewOpenImport(self))

        def search(self):
            self.wait_window(Search(self))

        def peaks_finder(self):
            self.wait_window(InitialPeaksFinder(self))

        def load_params(self):
            self.wait_window(LoadParams(self))


    menu_bar = tkinter.Menu()
    main_win = MainWindow()
    main_win.mainloop()
