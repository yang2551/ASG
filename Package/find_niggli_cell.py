# coding = UTF-8
import numpy
import pymysql


def relationship_calculate(matrix, error):
    """
    该函数用于计算Niggli约化胞的元素以及元素间的关系
    :param matrix: Niggli矩阵
    :param error: 误差容限
    :return: 包含元素值的列表element_list; 包含元素间关系的condition_list

        condition[0][0]: main condition
        condition[0][1]: relationship about d
        condition[0][2]: relationship about e
        condition[0][3]: relationship about f

    """
    element_list = []
    condition_list = numpy.zeros(shape=[1, 4])
    # element_list计算
    element_list.append(matrix[0][0])
    element_list.append(matrix[0][1])
    element_list.append(matrix[0][2])
    element_list.append(matrix[1][0])
    element_list.append(matrix[1][1])
    element_list.append(matrix[1][1])
    minimum_error = pow(10, -4)
    if abs(element_list[0]) <= minimum_error:
        element_list[0] = 0
    if abs(element_list[1]) <= minimum_error:
        element_list[1] = 0
    if abs(element_list[2]) <= minimum_error:
        element_list[2] = 0
    if abs(element_list[3]) <= minimum_error:
        element_list[3] = 0
    if abs(element_list[4]) <= minimum_error:
        element_list[4] = 0
    if abs(element_list[5]) <= minimum_error:
        element_list[5] = 0
    # condition_list计算
    if abs(element_list[0] - element_list[1]) <= error and abs(element_list[0] - element_list[2]) <= error:
        condition_list[0][0] = 1
        # d与其它元素间的关系
        if abs(element_list[3] - element_list[0] / 2) <= error:
            condition_list[0][1] = 1
        elif element_list[3] == 0:
            condition_list[0][1] = 2
        elif abs(element_list[3] + element_list[0] / 3) <= error:
            condition_list[0][1] = 3
        elif abs(2 * abs(element_list[3] + element_list[4] + element_list[5]) -
                 element_list[0] - element_list[1]) <= error:
            condition_list[0][1] = 4
        else:
            condition_list[0][1] = 5
        # e与其它元素间的关系
        if abs(element_list[4] - element_list[0] / 2) <= error:
            condition_list[0][2] = 1
        elif abs(element_list[4] - element_list[3]) <= error:
            condition_list[0][2] = 2
        elif element_list[4] == 0:
            condition_list[0][2] = 3
        elif abs(element_list[4] + element_list[0] / 3) <= error:
            condition_list[0][2] = 4
        else:
            condition_list[0][2] = 5
        # f与其它元素间的关系
        if abs(element_list[5] - element_list[0] / 2) <= error:
            condition_list[0][3] = 1
        elif abs(element_list[4] - element_list[3]) <= error:
            condition_list[0][3] = 2
        elif element_list[5] == 0:
            condition_list[0][3] = 3
        elif abs(element_list[5] + element_list[0] / 3) <= error:
            condition_list[0][3] = 4
        elif abs(element_list[5] - element_list[4]) <= error:
            condition_list[0][3] = 5
        else:
            condition_list[0][3] = 6
    if abs(element_list[0] - element_list[1]) <= error < abs(element_list[0] - element_list[2]):
        condition_list[0][0] = 2
        # d与其它元素间的关系
        if abs(element_list[3] - element_list[0] / 2) <= error:
            condition_list[0][1] = 1
        elif element_list[3] == 0:
            condition_list[0][1] = 2
        elif abs(element_list[3] + element_list[0] / 2) <= error:
            condition_list[0][1] = 3
        elif abs(2 * abs(element_list[3] + element_list[4] + element_list[5]) -
                 element_list[0] - element_list[1]) <= error:
            condition_list[0][1] = 4
        else:
            condition_list[0][1] = 5
        # e与其它元素间的关系
        if abs(element_list[4] - element_list[0] / 2) <= error:
            condition_list[0][2] = 1
        elif abs(element_list[4] - element_list[3]) <= error:
            condition_list[0][2] = 2
        elif element_list[4] == 0:
            condition_list[0][2] = 3
        elif abs(element_list[4] + element_list[0] / 2) <= error:
            condition_list[0][2] = 4
        else:
            condition_list[0][2] = 5
        # f与其它元素间的关系
        if abs(element_list[5] - element_list[0] / 2) <= error:
            condition_list[0][3] = 1
        elif element_list[5] == 0:
            condition_list[0][3] = 2
        elif abs(element_list[5] + element_list[0] / 2) <= error:
            condition_list[0][3] = 3
        else:
            condition_list[0][3] = 4
    if abs(element_list[1] - element_list[2]) <= error < abs(element_list[0] - element_list[1]):
        condition_list[0][0] = 3
        # d与其它元素间的关系
        if abs(element_list[3] - element_list[0] / 4) <= error:
            condition_list[0][1] = 1
        elif element_list[3] == 0:
            condition_list[0][1] = 2
        elif abs(element_list[3] + element_list[1] / 2) <= error:
            condition_list[0][1] = 3
        elif abs(2 * abs(element_list[3] + element_list[4] + element_list[5]) -
                 element_list[0] - element_list[1]) <= error:
            condition_list[0][1] = 4
        else:
            condition_list[0][1] = 5
        # e与其它元素间的关系
        if abs(element_list[4] - element_list[0] / 2) <= error:
            condition_list[0][2] = 1
        elif element_list[4] == 0:
            condition_list[0][2] = 2
        elif abs(element_list[4] + element_list[0] / 3) <= error:
            condition_list[0][2] = 3
        else:
            condition_list[0][2] = 4
        # f与其它元素间的关系
        if abs(element_list[5] - element_list[0] / 2) <= error:
            condition_list[0][3] = 1
        elif element_list[5] == 0:
            condition_list[0][3] = 2
        elif abs(element_list[5] + element_list[0] / 3) <= error:
            condition_list[0][3] = 3
        else:
            condition_list[0][3] = 4
    if abs(element_list[0] - element_list[1]) > error and abs(
            element_list[0] - element_list[2]) > error and abs(element_list[1] - element_list[2]) > error:
        condition_list[0][0] = 4
        # d与其它元素间的关系
        if abs(element_list[3] - element_list[0] / 4) <= error:
            condition_list[0][1] = 1
        elif abs(element_list[3] - element_list[1] / 2) <= error:
            condition_list[0][1] = 2
        elif abs(element_list[3] + element_list[1] / 2) <= error:
            condition_list[0][1] = 3
        elif element_list[3] == 0:
            condition_list[0][1] = 4
        elif abs(2 * abs(element_list[3] + element_list[4] + element_list[5]) - element_list[0] - element_list[1]
                 ) <= error and abs(abs(2 * element_list[3] + element_list[5]) - element_list[1]) <= error:
            condition_list[0][1] = 5
        else:
            condition_list[0][1] = 6
        # e与其它元素间的关系
        if abs(element_list[4] - element_list[0] / 2) <= error:
            condition_list[0][2] = 1
        elif abs(element_list[4] - 2 * element_list[3]) <= error:
            condition_list[0][2] = 2
        elif element_list[4] == 0:
            condition_list[0][2] = 3
        elif abs(element_list[4] + element_list[0] / 2) <= error:
            condition_list[0][2] = 4
        else:
            condition_list[0][2] = 5
        # f与其它元素间的关系
        if abs(element_list[5] - element_list[0] / 2) <= error:
            condition_list[0][3] = 1
        elif abs(element_list[5] - 2 * element_list[3]) <= error:
            condition_list[0][3] = 2
        elif abs(element_list[5] - 2 * element_list[4]) <= error:
            condition_list[0][3] = 3
        elif element_list[5] == 0:
            condition_list[0][3] = 4
        elif abs(element_list[5] + element_list[0] / 2) <= error:
            condition_list[0][3] = 5
        else:
            condition_list[0][3] = 6
    return condition_list


def niggli_cell(niggli_mat, tol_r_err, n_type):
    """
    :param niggli_mat: Niggli矩阵
    :param tol_r_err: 误差
    :param n_type: Niggli约化胞类型
    :return: 包含Niggli约化胞的序号、转换矩阵和布拉菲点阵类型的元组Tuple
    """
    conditions = relationship_calculate(niggli_mat, tol_r_err)
    main_condition = conditions[0][0]
    condition_d = conditions[0][1]
    condition_e = conditions[0][2]
    condition_f = conditions[0][3]
    # 链接MySQL
    connect = pymysql.connect(host='localhost', user='root', password='123456', database='mybase')
    cursor = connect.cursor()
    # 根据n_mat的条件获得transformation，Niggli约化矩阵内的元素之间的关系并放到下一行execute中
    trans = "select id, trans, bravaistype from mybase.reduced_base"
    trans += " where conditions=%s and d=%s and e=%s and d=%s and type=%s"
    if main_condition == 1:
        if condition_d == 1 and condition_e == 1 and condition_d == 1:
            cursor.execute(trans, ('a=b=c', 'a/2', 'a/2', 'a/2', n_type))  # 1
        elif condition_d == 5 and condition_e == 2 and n_type == 'type 1':
            cursor.execute(trans, ('a=b=c', 'd', 'd', 'd', n_type))  # 2
        elif condition_d == 2 and condition_e == 3 and condition_f == 3:
            cursor.execute(trans, ('a=b=c', 0, 0, 0, n_type))  # 3
        elif condition_d == 5 and condition_e == 2 and condition_f == 2 and n_type == 'type 2':
            cursor.execute(trans, ('a=b=c', 'd', 'd', 'd', n_type))  # 4
        elif condition_d == 3 and condition_e == 4 and condition_f == 4:
            cursor.execute(trans, ('a=b=c', '-a/3', '-a/3', '-a/3', n_type))  # 5
        elif condition_e == 2 and condition_f == 6:
            cursor.execute(trans, ('a=b=c', 'd', 'd', 'f', n_type))  # 6
        elif condition_f == 5:
            cursor.execute(trans, ('a=b=c', 'd', 'e', 'e', n_type))  # 7
        elif condition_e == 5 and condition_f == 6:
            cursor.execute(trans, ('a=b=c', 'd', 'e', 'f', n_type))  # 8
    if main_condition == 2:
        if condition_d == condition_e == condition_f == 1:
            cursor.execute(trans, ('a=b', 'a/2', 'a/2', 'a/2', n_type))  # 9
        elif condition_f == 4 and n_type == 'type 1':
            cursor.execute(trans, ('a=b', 'd', 'd', 'f', n_type))  # 10
        elif condition_d == condition_f == 2 and condition_e == 3:
            cursor.execute(trans, ('a=b', 0, 0, 0, n_type))  # 11
        elif condition_f == 3:
            cursor.execute(trans, ('a=b', 0, 0, '-a/2', n_type))  # 12
        elif condition_d == 2 and condition_e == 3 and condition_f == 4:
            cursor.execute(trans, ('a=b', 0, 0, 'f', n_type))  # 13
        elif condition_d == 5 and condition_e == 2 and condition_f == 4 and n_type == 'type 2':
            cursor.execute(trans, ('a=b', 'd', 'd', 'f', n_type))  # 14
        elif condition_d == 3 and condition_e == 4:
            cursor.execute(trans, ('a=b', '-a/2', '-a/2', 0, n_type))  # 15
        elif condition_d == 4 and condition_e == 2 and condition_f == 4:
            cursor.execute(trans, ('a=b', 'd', 'd', 'a-abs(d)', n_type))  # 16
        elif condition_d == 4 and condition_e == 5 and condition_f == 4:
            cursor.execute(trans, ('a=b', 'd', 'e', 'f', n_type))  # 17
    if main_condition == 3:
        if condition_d == 1:
            cursor.execute(trans, ('b=c', 'a/4', 'a/2', 'a/2', n_type))  # 18
        elif condition_d == 5 and condition_e == condition_f == 1:
            cursor.execute(trans, ('b=c', 'd', 'a/2', 'a/2', n_type))  # 19
        elif condition_d == 5 and condition_e == condition_f == 4 and n_type == 'type 1':
            cursor.execute(trans, ('b=c', 'd', 'e', 'e', n_type))  # 20
        elif condition_d == condition_e == condition_f == 2:
            cursor.execute(trans, ('b=c', 0, 0, 0, n_type))  # 21
        elif condition_d == 3:
            cursor.execute(trans, ('b=c', '-b/2', 0, 0, n_type))  # 22
        elif condition_d == 5 and condition_e == condition_f == 0:
            cursor.execute(trans, ('b=c', 'd', 0, 0, n_type))  # 23
        elif condition_e == condition_f == 3:
            cursor.execute(trans, ('b=c', 'd', '-a/3', '-a/3', n_type))  # 24
        elif condition_d == 5 and condition_e == condition_f == 4 and n_type == 'type 2':
            cursor.execute(trans, ('b=c', 'd', 'e', 'e', n_type))  # 25
    if main_condition == 4:
        if condition_d == 1:
            cursor.execute(trans, ('none', 'a/4', 'a/2', 'a/2', n_type))  # 26
        if condition_d == 6 and condition_e == condition_f == 1:
            cursor.execute(trans, ('none', 'd', 'a/2', 'a/2', n_type))  # 27
        if condition_f == 2:
            cursor.execute(trans, ('none', 'd', 'a/2', '2d', n_type))  # 28
        if condition_e == 2:
            cursor.execute(trans, ('none', 'd', '2d', 'a/2', n_type))  # 29
        if condition_d == 2:
            cursor.execute(trans, ('none', 'b/2', 'e', '2e', n_type))  # 30
        if condition_d == 6 and condition_e == 5 and condition_f == 6 and n_type == 'type 1':
            cursor.execute(trans, ('none', 'd', 'e', 'f', n_type))  # 31
        if condition_d == condition_f == 4 and condition_e == 3:
            cursor.execute(trans, ('none', 0, 0, 0, n_type))  # 32
        if condition_d == 4 and condition_e == 5 and condition_f == 4:
            cursor.execute(trans, ('none', 0, 'e', 0, n_type))  # 33
        if condition_d == 4 and condition_e == 3 and condition_f == 6:
            cursor.execute(trans, ('none', 0, 0, 'f', n_type))  # 34
        if condition_d == 6 and condition_e == 3 and condition_f == 4:
            cursor.execute(trans, ('none', 'd', 0, 0, n_type))  # 35
        if condition_d == 4 and condition_e == 4 and condition_f == 4:
            cursor.execute(trans, ('none', 0, '-a/2', 0, n_type))  # 36
        if condition_d == 6 and condition_e == 4 and condition_f == 4:
            cursor.execute(trans, ('none', 'd', '-a/2', 0, n_type))  # 37
        if condition_d == 4 and condition_e == 3 and condition_f == 5:
            cursor.execute(trans, ('none', 0, 0, '-a/2', n_type))  # 38
        if condition_d == 6 and condition_e == 3 and condition_f == 5:
            cursor.execute(trans, ('none', 'd', 0, '-a/2', n_type))  # 39
        if condition_d == 3 and condition_e == 3 and condition_f == 4:
            cursor.execute(trans, ('none', '-b/2', 0, 0, n_type))  # 40
        if condition_d == 3 and condition_e == 5 and condition_f == 4:
            cursor.execute(trans, ('none', '-b/2', 'e', 0, n_type))  # 41
        if condition_d == 3 and condition_e == condition_f == 4:
            cursor.execute(trans, ('none', '-b/2', '-a/2', 0, n_type))  # 42
        if condition_d == 5:
            cursor.execute(trans, ('none', '(b-abs(f))/2', 'e', 'f', n_type))  # 43
        if condition_d == 6 and condition_e == 5 and condition_f == 6 and n_type == 'type 2':
            cursor.execute(trans, ('none', 'd', 'e', 'f', n_type))  # 44
    data = cursor.fetchmany()
    cursor.close()
    connect.close()
    return data
