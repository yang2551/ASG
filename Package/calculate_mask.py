# coding = UTF-8
from tkinter import messagebox


def __error_a(lattice_in, direction_in):
    """
    a'和a不匹配时返回的信息框
    :param lattice_in: 晶系
    :param direction_in: 特征方向
    :return: No Return
    """
    messagebox.showinfo("Info", "(%s [%s]) Relationship between a' and a is not match. "
                                "Value will be set as None"
                        % (lattice_in.capitalize(), direction_in))


def __error_b(lattice_in, direction_in):
    """
    b'和b不匹配时返回的信息框
    :param lattice_in: 晶系
    :param direction_in: 特征方向
    :return: No Return
    """
    messagebox.showinfo("Info", "(%s [%s]) Relationship between b' and b is not match. "
                                "Value will be set as None"
                        % (lattice_in.capitalize(), direction_in))


def calculate_mask(real_space_params, reciprocal_params, directions, error=0.1):
    """
    根据实空间参数和倒易空间参数计算两者之间的关系, 返回两者关系对应的标识符
    :param real_space_params: 正空间晶格参数
    :param reciprocal_params: 倒易空间参数
    :param directions: 特征方向
    :param error: 误差
    :return: 返回两个参数间关系对应的标识符
    """
    lattice = real_space_params[0].lower()
    real_space_a = real_space_params[1]
    real_space_b = real_space_params[2]
    real_space_c = real_space_params[3]
    reciprocal_001, reciprocal_100, reciprocal_010 = [], [], []
    reciprocal_110, reciprocal_210, reciprocal_111 = [], [], []
    if "001" in directions:
        reciprocal_001 = reciprocal_params[directions.index("001")]
    if "100" in directions:
        reciprocal_100 = reciprocal_params[directions.index("100")]
    if "010" in directions:
        reciprocal_010 = reciprocal_params[directions.index("010")]
    if "110" in directions:
        reciprocal_110 = reciprocal_params[directions.index("110")]
    if "210" in directions:
        reciprocal_210 = reciprocal_params[directions.index("210")]
    if "111" in directions:
        reciprocal_111 = reciprocal_params[directions.index("111")]
    mask001, mask100, mask010 = [], [], []
    mask110, mask210, mask111 = [], [], []
    if lattice == 'cubic':
        if "001" in directions:
            if len(reciprocal_001):
                if abs(reciprocal_001[0] - real_space_a) < error:
                    mask001.append("4")
                elif abs(reciprocal_001[0] - 0.5 * real_space_a) < error:
                    mask001.append("6")
                elif abs(reciprocal_001[0] - 0.5 * (real_space_a - real_space_b)) < error:
                    mask001.append("9")
                elif abs(reciprocal_001[0] - 0.25 * (real_space_a - real_space_b)) < error:
                    mask001.append("j")
                else:
                    mask001.append("-1")
                    __error_a(lattice, "001")
                if abs(reciprocal_001[1] - real_space_b) < error:
                    mask001.append("3")
                elif abs(reciprocal_001[1] - 0.5 * real_space_b) < error:
                    mask001.append("6")
                elif abs(reciprocal_001[1] - 0.5 * (real_space_a + real_space_b)) < error:
                    mask001.append("9")
                elif abs(reciprocal_001[1] - 0.25 * (real_space_a + real_space_b)) < error:
                    mask001.append("i")
                else:
                    mask001.append("-1")
                    __error_b(lattice, "001")
        if "111" in directions:
            if len(reciprocal_111):
                if abs(reciprocal_111[0] - 1 / 3 * (2 * real_space_a - real_space_b - real_space_c)) < error:
                    mask111.append("d")
                elif abs(reciprocal_111[0] - 1 / 6 * (2 * real_space_a - real_space_b - real_space_c)) < error:
                    mask111.append("h")
                else:
                    mask111.append("-1")
                    __error_a(lattice, "111")
                if abs(reciprocal_111[1] - 1 / 3 * (2 * real_space_b - real_space_a - real_space_c)) < error:
                    mask111.append("d")
                elif abs(reciprocal_111[1] - 1 / 6 * (2 * real_space_b - real_space_a - real_space_c)) < error:
                    mask111.append("h")
                else:
                    mask111.append("-1")
                    __error_b(lattice, "111")
        if "110" in directions:
            if len(reciprocal_110):
                if abs(reciprocal_110[0] - real_space_a) < error:
                    mask110.append("a")
                elif abs(reciprocal_110[0] - 0.25 * (real_space_b - real_space_a)) < error:
                    mask110.append("i")
                else:
                    mask110.append("-1")
                    __error_a(lattice, "110")
                if abs(reciprocal_110[1] - real_space_c) < error:
                    mask110.append("5")
                elif abs(reciprocal_110[1] - 0.5 * real_space_c) < error:
                    mask110.append("8")
                else:
                    mask110.append("-1")
                    __error_b(lattice, "110")
    if lattice == 'trigonal':
        if "001" in directions:
            if len(reciprocal_001):
                if abs(reciprocal_001[0] - real_space_a) < error:
                    mask001.append("4")
                elif abs(reciprocal_001[0] - 1 / 3 * (2 * real_space_a + real_space_b)) < error:
                    mask001.append("c")
                elif abs(reciprocal_001[0] - 1 / 3 * (2 * real_space_a - real_space_b - real_space_c)) < error:
                    mask001.append("d")
                else:
                    mask001.append("-1")
                    __error_a(lattice, "001")
                if abs(reciprocal_001[1] - real_space_b) < error:
                    mask001.append("3")
                elif abs(reciprocal_001[1] - 1 / 3 * (real_space_b - real_space_a)) < error:
                    mask001.append("b")
                elif abs(reciprocal_001[1] - 1 / 3 * (2 * real_space_b - real_space_a - real_space_c)) < error:
                    mask001.append("d")
                else:
                    mask001.append("-1")
                    __error_b(lattice, "001")
        if "100" in directions:
            if len(reciprocal_100):
                if abs(reciprocal_100[0] - 0.5 * (real_space_a + 2 * real_space_b)) < error:
                    mask100.append("b")
                elif abs(reciprocal_100[0] - 1 / 6 * (2 * real_space_a + 4 * real_space_b + real_space_c)) < error:
                    mask100.append("f")
                elif abs(reciprocal_100[0] - 0.5 * (real_space_a + real_space_b - 2 * real_space_c)) < error:
                    mask100.append("k")
                else:
                    mask100.append("-1")
                    __error_a(lattice, "100")
                if abs(reciprocal_100[1] - real_space_c) < error:
                    mask100.append("5")
                elif abs(reciprocal_100[1] - 0.5 * real_space_c) < error:
                    mask100.append("8")
                elif abs(reciprocal_100[1] - 1 / 3 * (real_space_c - real_space_a - 2 * real_space_b)) < error:
                    mask100.append("f")
                elif abs(reciprocal_100[1] - 1 / 6 * (real_space_c - real_space_a - 2 * real_space_b)) < error:
                    mask100.append("g")
                else:
                    mask100.append("-1")
                    __error_b(lattice, "100")
        if "210" in directions:
            if len(reciprocal_210):
                if abs(reciprocal_210[0] - 0.5 * real_space_b) < error:
                    mask210.append("8")
                elif abs(reciprocal_210[0] - 0.5 * (real_space_b - real_space_c)) < error:
                    mask210.append("e")
                else:
                    mask210.append("-1")
                    __error_a(lattice, "210")
                if abs(reciprocal_210[1] - real_space_c) < error:
                    mask210.append("5")
                elif abs(reciprocal_210[1] - 0.5 * real_space_c) < error:
                    mask210.append("8")
                elif abs(reciprocal_210[1] - 1 / 3 * real_space_c) < error:
                    mask210.append("c")
                elif abs(reciprocal_210[1] - 1 / 3 * (real_space_a + real_space_b + real_space_c)) < error:
                    mask210.append("e")
                else:
                    mask210.append("-1")
                    __error_b(lattice, "210")
    if lattice == 'hexagonal':
        if "001" in directions:
            if len(reciprocal_001):
                if abs(reciprocal_001[0] - real_space_a) < error:
                    mask001.append("4")
                else:
                    mask001.append("-1")
                    __error_a(lattice, "001")
                if abs(reciprocal_001[1] - real_space_b) < error:
                    mask001.append("3")
                else:
                    mask001.append("-1")
                    __error_b(lattice, "001")
        if "100" in directions:
            if len(reciprocal_100):
                if abs(reciprocal_100[0] - 0.5 * (real_space_a - 2 * real_space_b)) < error:
                    mask100.append("b")
                else:
                    mask100.append("-1")
                    __error_a(lattice, "100")
                if abs(reciprocal_100[1] - real_space_c) < error:
                    mask100.append("5")
                elif abs(reciprocal_100[1] - 0.5 * real_space_c) < error:
                    mask100.append("8")
                else:
                    mask100.append("-1")
                    __error_b(lattice, "100")
        if "210" in directions:
            if len(reciprocal_210):
                if abs(reciprocal_210[0] - 0.5 * real_space_b) < error:
                    mask210.append("8")
                else:
                    mask210.append("-1")
                    __error_a(lattice, "210")
                if abs(reciprocal_210[1] - real_space_c) < error:
                    mask210.append("5")
                elif abs(reciprocal_210[1] - 0.5 * real_space_c) < error:
                    mask210.append("8")
                else:
                    mask210.append("-1")
                    __error_b(lattice, "210")
    if lattice == 'monoclinic':
        if "001" in directions:
            if len(reciprocal_001):
                if abs(reciprocal_001[0] - real_space_a) < error:
                    mask001.append("4")
                elif abs(reciprocal_001[0] - 0.5 * real_space_a) < error:
                    mask001.append("6")
                else:
                    mask001.append("-1")
                    __error_a(lattice, "001")
                if abs(reciprocal_001[1] - real_space_b) < error:
                    mask001.append("3")
                elif abs(reciprocal_001[1] - 0.5 * real_space_b) < error:
                    mask001.append("6")
                else:
                    mask001.append("-1")
                    __error_b(lattice, "001")
        if "100" in directions:
            if len(reciprocal_100):
                if abs(reciprocal_100[0] - real_space_b) < error:
                    mask100.append("5")
                elif abs(reciprocal_100[0] - 0.5 * real_space_b) < error:
                    mask100.append("8")
                else:
                    mask100.append("-1")
                    __error_a(lattice, "100")
                if abs(reciprocal_100[1] - real_space_c) < error:
                    mask100.append("5")
                else:
                    mask100.append("-1")
                    __error_b(lattice, "100")
        if "010" in directions:
            if len(reciprocal_010):
                if abs(reciprocal_010[0] - real_space_c) < error:
                    mask010.append("3")
                elif abs(reciprocal_010[0] - 0.5 * real_space_c) < error:
                    mask010.append("7")
                else:
                    mask010.append("-1")
                    __error_a(lattice, "010")
                if abs(reciprocal_010[1] - real_space_a) < error:
                    mask010.append("4")
                elif abs(reciprocal_010[1] - 0.5 * real_space_a) < error:
                    mask010.append("7")
                else:
                    mask010.append("-1")
                    __error_b(lattice, "010")
    if lattice == 'orthorhombic':
        if "001" in directions:
            if len(reciprocal_001):
                if abs(reciprocal_001[0] - real_space_a) < error:
                    mask001.append("4")
                elif abs(reciprocal_001[0] - 1/2 * real_space_a) < error:
                    mask001.append("6")
                else:
                    mask001.append("-1")
                    __error_a(lattice, "001")
                if abs(reciprocal_001[1] - real_space_b) < error:
                    mask001.append("3")
                elif abs(reciprocal_001[1] - 0.5 * real_space_b) < error:
                    mask001.append("6")
                else:
                    mask001.append("-1")
                    __error_b(lattice, "001")
        if "100" in directions:
            if len(reciprocal_100):
                if abs(reciprocal_100[0] - real_space_b) < error:
                    mask100.append("5")
                elif abs(reciprocal_100[0] - 0.5 * real_space_b) < error:
                    mask100.append("8")
                else:
                    mask100.append("-1")
                    __error_a(lattice, "100")
                if abs(reciprocal_100[1] - real_space_c) < error:
                    mask100.append("5")
                elif abs(reciprocal_100[1] - 0.5 * real_space_c) < error:
                    mask100.append("8")
                else:
                    mask100.append("-1")
                    __error_b(lattice, "100")
        if "010" in directions:
            if len(reciprocal_010):
                if abs(reciprocal_010[0] - real_space_c) < error:
                    mask010.append("3")
                elif abs(reciprocal_010[0] - 0.5 * real_space_c) < error:
                    mask010.append("7")
                else:
                    mask010.append("-1")
                    __error_a(lattice, "010")
                if abs(reciprocal_010[1] - real_space_a) < error:
                    mask010.append("4")
                elif abs(reciprocal_010[1] - 0.5 * real_space_a) < error:
                    mask010.append("7")
                else:
                    mask010.append("-1")
                    __error_b(lattice, "010")
    if lattice == 'tetragonal':
        if "001" in directions:
            if len(reciprocal_001):
                if abs(reciprocal_001[0] - real_space_a) < error:
                    mask001.append("4")
                elif abs(reciprocal_001[0] - 0.5 * real_space_a) < error:
                    mask001.append("6")
                elif abs(reciprocal_001[0] - 0.5 * (real_space_a - real_space_b)) < error:
                    mask001.append("9")
                else:
                    mask001.append("-1")
                    __error_a(lattice, "001")
                if abs(reciprocal_001[1] - real_space_b) < error:
                    mask001.append("3")
                elif abs(reciprocal_001[1] - 0.5 * real_space_b) < error:
                    mask001.append("6")
                elif abs(reciprocal_001[1] - 0.5 * (real_space_a + real_space_b)) < error:
                    mask001.append("9")
                else:
                    mask001.append("-1")
                    __error_b(lattice, "001")
        if "100" in directions:
            if len(reciprocal_100):
                if abs(reciprocal_100[0] - real_space_b) < error:
                    mask100.append("2")
                elif abs(reciprocal_100[0] - 0.5 * real_space_b) < error:
                    mask100.append("8")
                else:
                    mask100.append("-1")
                    __error_a(lattice, "100")
                if abs(reciprocal_100[1] - real_space_c) < error:
                    mask100.append("5")
                elif abs(reciprocal_100[1] - 0.5 * real_space_c) < error:
                    mask100.append("8")
                else:
                    mask100.append("-1")
                    __error_b(lattice, "100")
        if "110" in directions:
            if len(reciprocal_110):
                if abs(reciprocal_110[0] - 0.5 * (real_space_b - real_space_a)) < error:
                    mask110.append("a")
                else:
                    mask110.append("-1")
                    __error_a(lattice, "110")
                if abs(reciprocal_110[1] - real_space_c) < error:
                    mask110.append("5")
                elif abs(reciprocal_110[1] - 0.5 * real_space_c) < error:
                    mask110.append("8")
                else:
                    mask110.append("-1")
                    __error_b(lattice, "110")
    return [mask001, mask100, mask010, mask110, mask210, mask111]
