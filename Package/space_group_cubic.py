import pymysql

space_group_id = None


def __mask_equal_none(mask):
    raise ValueError("%s is/are None" % mask)


def __main_error():
    raise ValueError("Offered info is not enough to determine space group.")


def match_space_group_cubic(mask001, mask111, mask110, directions, symmetry, bravais):
    connect = pymysql.connect(host='localhost', user='root', password='123456',
                              database='mybase', charset='utf8')
    cursor = connect.cursor()

    mask001_a = "-1"
    mask001_b = "-1"
    mask111_a = "-1"
    mask111_b = "-1"
    mask110_a = "-1"
    mask110_b = "-1"
    if len(mask001):
        mask001_a = mask001[0]
        mask001_b = mask001[1]
    if len(mask111):
        mask111_a = mask111[0]
        mask111_b = mask111[1]
    if len(mask110):
        mask110_a = mask110[0]
        mask110_b = mask110[1]
    flag = 0
    if mask001_a != "-1":
        flag += 1
    if mask001_b != "-1":
        flag += 1
    if mask110_a != "-1":
        flag += 1
    if mask110_b != "-1":
        flag += 1
    if mask111_a != "-1":
        flag += 1
    if mask111_b != "-1":
        flag += 1
    global space_group_id
    while len(symmetry) == 1:
        if "001" in directions:
            sql = "select id from cubic where sg001=%s and name=%s"
            cursor.execute(sql, (symmetry[0], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            elif len(space_group_id) == 1:
                break
            else:
                if mask001_a != "-1" and mask001_b != "-1":
                    sql += " and mask001a=%s and mask001b=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask001_a, mask001_b))
                if mask001_a != "-1" and mask001_b == "-1":
                    sql += " and mask001a=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask001_a))
                if mask001_a == "-1" and mask001_b != "-1":
                    sql += " and mask001b=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask001_b))
                if mask001_a == "-1" and mask001_b == "-1":
                    __mask_equal_none(mask001)
                space_group_id = cursor.fetchall()
        elif "111" in directions:
            sql = "select id from cubic where sg111=%s and name=%s"
            cursor.execute(sql, (symmetry[0], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            elif len(space_group_id) == 1:
                break
            else:
                if mask111_a != "-1" and mask111_b != "-1":
                    sql += " and mask111a=%s and mask111b=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask111_a, mask111_b))
                if mask111_a != "-1" and mask111_b == "-1":
                    sql += " and mask111a=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask111_a))
                if mask111_a == "-1" and mask111_b != "-1":
                    sql += " and mask111b=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask111_b))
                if mask111_a == "-1" and mask111_b == "-1":
                    __mask_equal_none(mask111)
                space_group_id = cursor.fetchall()
        elif "110" in directions:
            sql = "select id from cubic where sg110=%s and name=%s"
            cursor.execute(sql, (symmetry[0], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            elif len(space_group_id) == 1:
                break
            else:
                if mask110_a != "-1" and mask110_b != "-1":
                    sql += " and mask110a=%s and mask110b=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask110_a, mask110_b))
                if mask110_a != "-1" and mask110_b == "-1":
                    sql += " and mask110a=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask110_a))
                if mask110_a == "-1" and mask110_b != "-1":
                    sql += " and mask110b=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask110_b))
                if mask110_a == "-1" and mask110_b == "-1":
                    __mask_equal_none(mask110)
                space_group_id = cursor.fetchall()
        else:
            raise ValueError("Offered direction is not characteristic direction.")
        break
    while len(symmetry) == 2:
        if "001" and "111" in directions:
            sql = "select id from cubic where sg001=%s and sg111=%s and name=%s"
            cursor.execute(sql, (symmetry[directions.index("001")],
                                 symmetry[directions.index("111")], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            if len(space_group_id) == 1:
                break
            if len(space_group_id) > 1:
                if mask001_a != "-1" and mask001_b != "-1" and mask111_a != "-1" and mask111_b != "-1":
                    sql += " and mask001a=%s and mask001b=%s and mask111a=%s and mask111b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                         bravais, mask001_a, mask001_b, mask111_a, mask111_b))
                if mask001_a == "-1" and mask001_b == "-1" and mask111_a == "-1" and mask111_b == "-1":
                    __mask_equal_none([mask001, mask111])
                if mask001_a == "-1" and mask001_b != "-1" and mask111_a != "-1" and mask111_b != "-1":
                    sql += " and mask001b=%s and mask111a=%s and mask111b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                         bravais, mask001_b, mask111_a, mask111_b))
                if mask001_a != "-1" and mask001_b == "-1" and mask111_a != "-1" and mask111_b != "-1":
                    sql += " and mask001a=%s and mask111a=%s and mask111b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                         bravais, mask001_a, mask111_a, mask111_b))
                if mask001_a != "-1" and mask001_b != "-1" and mask111_a == "-1" and mask111_b != "-1":
                    sql += " and mask001a=%s and mask001b=%s and mask111b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                         bravais, mask001_a, mask001_b, mask111_b))
                if mask001_a != "-1" and mask001_b != "-1" and mask111_a != "-1" and mask111_b == "-1":
                    sql += " and mask001a=%s and mask001b=%s and mask111a=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                         bravais, mask001_a, mask001_b, mask111_a))
                if mask001_a != "-1" and mask001_b != "-1" and mask111_a == "-1" and mask111_b == "-1":
                    sql += " and mask001a=%s and mask001b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                         bravais, mask001_a, mask001_b))
                if mask001_a == "-1" and mask001_b == "-1" and mask111_a != "-1" and mask111_b != "-1":
                    sql += " and mask111a=%s and mask111b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                         bravais, mask111_a, mask111_b))
                if mask001_a != "-1" and mask001_b == "-1" and mask111_a != "-1" and mask111_b == "-1":
                    sql += " and mask001a=%s and mask111a=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                         bravais, mask001_a, mask111_a))
                if mask001_a != "-1" and mask001_b == "-1" and mask111_a == "-1" and mask111_b != "-1":
                    sql += " and mask001a=%s and mask111b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                         bravais, mask001_a, mask111_b))
                if mask001_a == "-1" and mask001_b != "-1" and mask111_a == "-1" and mask111_b != "-1":
                    sql += " and mask001b=%s and mask111b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                         bravais, mask001_b, mask111_b))
                if mask001_a == "-1" and mask001_b != "-1" and mask111_a != "-1" and mask111_b == "-1":
                    sql += " and mask001b=%s and mask111a=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                         bravais, mask001_b, mask111_a))
                space_group_id = cursor.fetchall()
        elif "001" and "110" in directions:
            sql = "select id from cubic where sg001=%s and sg110=%s and name=%s"
            cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("110")], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            if len(space_group_id) == 1:
                break
            if len(space_group_id) > 1:
                if mask001_a != "-1" and mask001_b != "-1" and mask110_a != "-1" and mask110_b != "-1":
                    sql += " and mask001a=%s and mask001b=%s and mask110a=%s and mask110b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("110")],
                                         bravais, mask001_a, mask001_b, mask110_a, mask110_b))
                if mask001_a == "-1" and mask001_b == "-1" and mask110_a == "-1" and mask110_b == "-1":
                    __mask_equal_none([mask001, mask110])
                if mask001_a == "-1" and mask001_b != "-1" and mask110_a != "-1" and mask110_b != "-1":
                    sql += " and mask001b=%s and mask110a=%s and mask110b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("110")],
                                         bravais, mask001_b, mask110_a, mask110_b))
                if mask001_a != "-1" and mask001_b == "-1" and mask110_a != "-1" and mask110_b != "-1":
                    sql += " and mask001a=%s and mask110a=%s and mask110b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("110")],
                                         bravais, mask001_a, mask110_a, mask110_b))
                if mask001_a != "-1" and mask001_b != "-1" and mask110_a == "-1" and mask110_b != "-1":
                    sql += " and mask001a=%s and mask001b=%s and mask110b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("110")],
                                         bravais, mask001_a, mask001_b, mask110_b))
                if mask001_a != "-1" and mask001_b != "-1" and mask110_a != "-1" and mask110_b == "-1":
                    sql += " and mask001a=%s and mask001b=%s and mask110a=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("110")],
                                         bravais, mask001_a, mask001_b, mask110_a))
                if mask001_a != "-1" and mask001_b != "-1" and mask110_a == "-1" and mask110_b == "-1":
                    sql += " and mask001a=%s and mask001b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("110")],
                                         bravais, mask001_a, mask001_b))
                if mask001_a == "-1" and mask001_b == "-1" and mask110_a != "-1" and mask110_b != "-1":
                    sql += " and mask110a=%s and mask110b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("110")],
                                         bravais, mask110_a, mask110_b))
                if mask001_a != "-1" and mask001_b == "-1" and mask110_a != "-1" and mask110_b == "-1":
                    sql += " and mask001a=%s and mask110a=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("110")],
                                         bravais, mask001_a, mask110_a))
                if mask001_a != "-1" and mask001_b == "-1" and mask110_a == "-1" and mask110_b != "-1":
                    sql += " and mask001a=%s and mask110b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("110")],
                                         bravais, mask001_a, mask110_b))
                if mask001_a == "-1" and mask001_b != "-1" and mask110_a == "-1" and mask110_b != "-1":
                    sql += " and mask001b=%s and mask110b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("110")],
                                         bravais, mask001_b, mask110_b))
                if mask001_a == "-1" and mask001_b != "-1" and mask110_a != "-1" and mask110_b == "-1":
                    sql += " and mask001b=%s and mask111a=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("110")],
                                         bravais, mask001_b, mask110_a))
                space_group_id = cursor.fetchall()
        elif "110" and "111" in directions:
            sql = "select id from cubic where sg110=%s and sg111=%s and name=%s"
            cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("111")], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            if len(space_group_id) == 1:
                break
            if len(space_group_id) > 1:
                if mask110_a != "-1" and mask110_b != "-1" and mask111_a != "-1" and mask111_b != "-1":
                    sql += " and mask110a=%s and mask110b=%s and mask111a=%s and mask111b=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("111")],
                                         bravais, mask110_a, mask110_b, mask111_a, mask111_b))
                if mask110_a == "-1" and mask110_b == "-1" and mask111_a == "-1" and mask111_b == "-1":
                    __mask_equal_none([mask110, mask111])
                if mask110_a == "-1" and mask110_b != "-1" and mask111_a != "-1" and mask111_b != "-1":
                    sql += " and mask110b=%s and mask111a=%s and mask111b=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("111")],
                                         bravais, mask110_b, mask111_a, mask111_b))
                if mask110_a != "-1" and mask110_b == "-1" and mask111_a != "-1" and mask111_b != "-1":
                    sql += " and mask110a=%s and mask111a=%s and mask111b=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("111")],
                                         bravais, mask110_a, mask111_a, mask111_b))
                if mask110_a != "-1" and mask110_b != "-1" and mask111_a == "-1" and mask111_b != "-1":
                    sql += " and mask110a=%s and mask110b=%s and mask111b=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("111")],
                                         bravais, mask110_a, mask110_b, mask111_b))
                if mask110_a != "-1" and mask110_b != "-1" and mask111_a != "-1" and mask111_b == "-1":
                    sql += " and mask110a=%s and mask110b=%s and mask111a=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("111")],
                                         bravais, mask110_a, mask110_b, mask111_a))
                if mask110_a != "-1" and mask110_b != "-1" and mask111_a == "-1" and mask111_b == "-1":
                    sql += " and mask110a=%s and mask110b=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("111")],
                                         bravais, mask110_a, mask110_b))
                if mask110_a == "-1" and mask110_b == "-1" and mask111_a != "-1" and mask111_b != "-1":
                    sql += " and mask111a=%s and mask111b=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("111")],
                                         bravais, mask111_a, mask111_b))
                if mask110_a != "-1" and mask110_b == "-1" and mask111_a != "-1" and mask111_b == "-1":
                    sql += " and mask110a=%s and mask111a=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("111")],
                                         bravais, mask110_a, mask111_a))
                if mask110_a != "-1" and mask110_b == "-1" and mask111_a == "-1" and mask111_b != "-1":
                    sql += " and mask110a=%s and mask111b=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("111")],
                                         bravais, mask110_a, mask111_b))
                if mask110_a == "-1" and mask110_b != "-1" and mask111_a == "-1" and mask111_b != "-1":
                    sql += " and mask110b=%s and mask111b=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("111")],
                                         bravais, mask110_b, mask111_b))
                if mask110_a == "-1" and mask110_b != "-1" and mask111_a != "-1" and mask111_b == "-1":
                    sql += " and mask110b=%s and mask111a=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("111")],
                                         bravais, mask110_b, mask111_a))
                space_group_id = cursor.fetchall()
        else:
            raise ValueError("Offered directions are not exactly characteristic directions.")
        break
    while len(symmetry) == 3:
        if "001" and "111" and "110" in directions:
            sql = "select id from cubic where sg001=%s and sg111=%s and sg110=%s and name=%s"
            cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                 symmetry[directions.index("110")], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            if len(space_group_id) == 1:
                break
            if len(space_group_id) > 1:
                if flag == 6:
                    sql += " and mask001a=%s and mask001b=%s and mask111a=%s"
                    sql += " and mask111b=%s and mask110a=%s and mask110b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                         symmetry[directions.index("110")], bravais,
                                         mask001_a, mask001_b, mask111_a, mask111_b, mask110_a, mask110_b))
                if flag == 0:
                    __mask_equal_none([mask001, mask111, mask110])

                if flag == 1:
                    if mask001_a != "-1":
                        sql += " and mask001a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask001_a))
                    if mask001_b != "-1":
                        sql += " and mask001b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask001_b))
                    if mask110_a != "-1":
                        sql += " and mask110a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask110_a))
                    if mask110_b != "-1":
                        sql += " and mask110b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask110_b))
                    if mask111_a != "-1":
                        sql += " and mask111a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask111_a))
                    if mask111_b != "-1":
                        sql += " and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask111_b))

                if flag == 2:
                    if mask001_a != "-1" and mask001_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask001_a, mask001_b))
                    if mask001_a != "-1" and mask110_a != "-1":
                        sql += " and mask001a=%s and mask110a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask001_a, mask110_a))
                    if mask001_a != "-1" and mask110_b != "-1":
                        sql += " and mask001a=%s and mask110b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask001_a, mask110_b))
                    if mask001_a != "-1" and mask111_a != "-1":
                        sql += " and mask001a=%s and mask111a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask001_a, mask111_a))
                    if mask001_a != "-1" and mask111_b != "-1":
                        sql += " and mask001a=%s and mask110a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask001_a, mask111_b))
                    if mask001_b != "-1" and mask110_a != "-1":
                        sql += " and mask001b=%s and mask110a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask001_b, mask110_a))
                    if mask001_b != "-1" and mask110_b != "-1":
                        sql += "and mask001b=%s and mask110b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask001_b, mask110_b))
                    if mask001_b != "-1" and mask111_a != "-1":
                        sql += " and mask001b=%s and mask111a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask001_b, mask111_a))
                    if mask001_b != "-1" and mask111_b != "-1":
                        sql += " and mask001b=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask001_b, mask111_b))
                    if mask110_a != "-1" and mask110_b != "-1":
                        sql += " and mask110a=%s and mask110b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask110_a, mask110_b))
                    if mask110_a != "-1" and mask111_a != "-1":
                        sql += " and mask110a=%s and mask111a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask110_a, mask111_a))
                    if mask110_a != "-1" and mask111_b != "-1":
                        sql += " and mask110a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask110_a, mask111_b))
                    if mask110_b != "-1" and mask111_a != "-1":
                        sql += " and mask110b=%s and mask111a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask110_b, mask111_a))
                    if mask110_b != "-1" and mask111_b != "-1":
                        sql += " and mask110b=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask110_b, mask111_b))
                    if mask111_a != "-1" and mask111_b != "-1":
                        sql += " and mask111a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais, mask111_a, mask111_b))

                if flag == 3:
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_a))
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask111_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask111a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask111_a))
                    if mask001_a != "-1" and mask001_b != "-1" and mask111_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask111_b))
                    if mask001_a != "-1" and mask110_a != "-1" and mask110_b != "-1":
                        sql += " and mask001a=%s and mask110a=%s and mask110b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_a, mask110_b))
                    if mask001_a != "-1" and mask110_a != "-1" and mask111_a != "-1":
                        sql += " and mask001a=%s and mask110a=%s and mask111a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_a, mask111_a))
                    if mask001_a != "-1" and mask110_a != "-1" and mask111_b != "-1":
                        sql += " and mask001a=%s and mask110a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_a, mask111_b))
                    if mask001_a != "-1" and mask110_b != "-1" and mask111_a != "-1":
                        sql += " and mask001a=%s and mask110b=%s and mask111a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_b, mask111_a))
                    if mask001_a != "-1" and mask110_b != "-1" and mask111_b != "-1":
                        sql += " and mask001a=%s and mask110b=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_b, mask111_b))
                    if mask001_a != "-1" and mask111_a != "-1" and mask111_b != "-1":
                        sql += " and mask001a=%s and mask111a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask111_a, mask111_b))
                    if mask001_b != "-1" and mask110_a != "-1" and mask110_b != "-1":
                        sql += " and mask001b=%s and mask110a=%s and mask110b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_a, mask110_b))
                    if mask001_b != "-1" and mask110_a != "-1" and mask111_a != "-1":
                        sql += " and mask001b=%s and mask110a=%s and mask111a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_a, mask111_a))
                    if mask001_b != "-1" and mask110_a != "-1" and mask111_b != "-1":
                        sql += " and mask001b=%s and mask110a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_a, mask111_b))
                    if mask001_b != "-1" and mask110_b != "-1" and mask111_a != "-1":
                        sql += " and mask001b=%s and mask110b=%s and mask111a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_b, mask111_a))
                    if mask001_b != "-1" and mask110_b != "-1" and mask111_b != "-1":
                        sql += " and mask001b=%s and mask110a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_b, mask111_b))
                    if mask001_b != "-1" and mask111_a != "-1" and mask111_b != "-1":
                        sql += " and mask001b=%s and mask111a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask111_a, mask111_b))
                    if mask110_a != "-1" and mask110_b != "-1" and mask111_a != "-1":
                        sql += " and mask110a=%s and mask110b=%s and mask111a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask110_a, mask110_b, mask111_a))
                    if mask110_a != "-1" and mask110_b != "-1" and mask111_b != "-1":
                        sql += " and mask110a=%s and mask110b=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask110_a, mask110_b, mask111_b))
                    if mask110_a != "-1" and mask111_a != "-1" and mask111_b != "-1":
                        sql += " and mask110a=%s and mask111a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask110_a, mask111_a, mask111_b))
                    if mask110_b != "-1" and mask111_a != "-1" and mask111_b != "-1":
                        sql += " and mask110b=%s and mask111a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask110_b, mask111_a, mask111_b))

                if flag == 4:
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_a != "-1" and mask110_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110a=%s and mask110b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_a, mask110_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_a != "-1" and mask111_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110a=%s and mask111a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_a, mask111_a))
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_a != "-1" and mask111_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_a, mask111_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_b != "-1" and mask111_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110b=%s and mask111a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_b, mask111_a))
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_b != "-1" and mask111_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110b=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_b, mask111_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask111_a != "-1" and mask111_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask111a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask111_a, mask111_b))
                    if mask001_a != "-1" and mask110_a != "-1" and mask110_b != "-1" and mask111_a != "-1":
                        sql += " and mask001a=%s and mask110a=%s and mask110b=%s and mask111a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_a, mask110_b, mask111_a))
                    if mask001_a != "-1" and mask110_a != "-1" and mask110_b != "-1" and mask111_b != "-1":
                        sql += " and mask001a=%s and mask110a=%s and mask110b=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_a, mask110_b, mask111_b))
                    if mask001_a != "-1" and mask110_a != "-1" and mask111_a != "-1" and mask111_b != "-1":
                        sql += " and mask001a=%s and mask110a=%s and mask111a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_a, mask111_a, mask111_b))
                    if mask001_a != "-1" and mask110_b != "-1" and mask111_a != "-1" and mask111_b != "-1":
                        sql += " and mask001a=%s and mask110b=%s and mask111a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_b, mask111_a, mask111_b))
                    if mask001_b != "-1" and mask110_a != "-1" and mask110_b != "-1" and mask111_a != "-1":
                        sql += " and mask001b=%s and mask110a=%s and mask110b=%s and mask111a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_a, mask110_b, mask111_a))
                    if mask001_b != "-1" and mask110_a != "-1" and mask110_b != "-1" and mask111_b != "-1":
                        sql += " and mask001b=%s and mask110a=%s and mask110b=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_a, mask110_b, mask111_b))
                    if mask001_b != "-1" and mask110_a != "-1" and mask111_a != "-1" and mask111_b != "-1":
                        sql += " and mask001b=%s and mask110a=%s and mask111a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_a, mask111_a, mask111_b))
                    if mask001_b != "-1" and mask110_b != "-1" and mask111_a != "-1" and mask111_b != "-1":
                        sql += " and mask001b=%s and mask110b=%s and mask111a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_b, mask111_a, mask111_b))
                    if mask110_a != "-1" and mask110_b != "-1" and mask111_a != "-1" and mask111_b != "-1":
                        sql += " and mask110a=%s and mask110b=%s and mask111a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask110_a, mask110_b, mask111_a, mask111_b))

                if flag == 5:
                    if mask001_b != "-1" and mask110_a != "-1" and mask110_b != "-1" and mask111_a != "-1" and mask111_b != "-1":
                        sql += " and mask001b=%s and mask110a=%s and mask110b=%s and mask111a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_a, mask110_b, mask111_a, mask111_b))
                    if mask001_a != "-1" and mask110_a != "-1" and mask110_b != "-1" and mask111_a != "-1" and mask111_b != "-1":
                        sql += " and mask001a=%s and mask110a=%s and mask110b=%s and mask111a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_a, mask110_b, mask111_a, mask111_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_b != "-1" and mask111_a != "-1" and mask111_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110b=%s and mask111a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_b, mask111_a, mask111_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_a != "-1" and mask111_a != "-1" and mask111_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110a=%s and mask111a=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_a, mask111_a, mask111_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_a != "-1" and mask110_b != "-1" and mask111_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110a=%s and mask110b=%s and mask111b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_a, mask110_b, mask111_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_a != "-1" and mask110_b != "-1" and mask111_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110a=%s and mask110b=%s and mask111a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("111")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_a, mask110_b, mask111_a))

                space_group_id = cursor.fetchall()
        else:
            raise ValueError("Offered directions are not exactly characteristic directions.")
        break
    cursor.close()
    connect.close()
    return space_group_id
