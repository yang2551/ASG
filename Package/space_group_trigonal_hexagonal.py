import pymysql

space_group_id = None


def __mask_equal_none(mask):
    raise ValueError("%s is/are None" % mask)


def __main_error():
    raise ValueError("Offered info is not enough to determine space group.")


def match_space_group_trigonal_hexagonal(mask001, mask100, mask210, directions, symmetry, bravais, lattice):
    mask001_a = "-1"
    mask001_b = "-1"
    mask100_a = "-1"
    mask100_b = "-1"
    mask210_a = "-1"
    mask210_b = "-1"
    # directions = []
    if len(mask001):
        mask001_a = mask001[0]
        mask001_b = mask001[1]
        # directions.append("001")
    if len(mask100):
        mask100_a = mask100[0]
        mask100_b = mask100[1]
        # directions.append("100")
    if len(mask210):
        mask210_a = mask210[0]
        mask210_b = mask210[1]
        # directions.append("210")
    flag = 0
    if mask001_a != "-1":
        flag += 1
    if mask001_b != "-1":
        flag += 1
    if mask210_a != "-1":
        flag += 1
    if mask210_b != "-1":
        flag += 1
    if mask100_a != "-1":
        flag += 1
    if mask100_b != "-1":
        flag += 1
    connect = pymysql.connect(host='localhost', user='root', password='123456',
                              database='mybase', charset='utf8')
    cursor = connect.cursor()
    global space_group_id
    while len(symmetry) == 1:
        if "001" in directions:
            sql = ""
            if lattice[0] == 'trigonal':
                sql = "select id from trigonal where sg001=%s and name=%s"
            if lattice[0] == 'hexagonal':
                sql = "select id from hexagonal where sg001=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need trigonal or hexagonal, but given %s" % lattice[0].capitalize())
            cursor.execute(sql, (symmetry[0], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) == 1:
                break
            if len(space_group_id) < 1:
                __main_error()
            else:
                if mask001_a == "-1" and mask001_b == "-1":
                    __mask_equal_none(mask001)
                if mask001_a == "-1" and mask001_b != "-1":
                    sql += " and mask001b=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask001_b))
                if mask001_a != "-1" and mask001_b == "-1":
                    sql += " and mask001a=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask001_a))
                if mask001_a != "-1" and mask001_b != "-1":
                    sql += " and mask001a=%s and mask001b=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask001_a, mask001_b))
                space_group_id = cursor.fetchall()
        elif "100" in directions:
            sql = ""
            if lattice[0] == 'trigonal':
                sql = "select id from trigonal where sg100=%s and name=%s"
            if lattice[0] == 'hexagonal':
                sql = "select id from hexagonal where sg100=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need trigonal or hexagonal, but given %s" % lattice[0].capitalize())
            cursor.execute(sql, (symmetry[0], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            elif len(space_group_id) == 1:
                break
            else:
                if mask100_a != "-1" and mask100_b != "-1":
                    sql += " and mask100a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask100_a, mask100_b))
                if mask100_b == "-1" and mask100_a != "-1":
                    sql += " and mask100a=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask100_a))
                if mask100_a == "-1" and mask100_b != "-1":
                    sql += " and mask100b=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask100_b))
                if mask100_a == "-1" and mask100_b == "-1":
                    __mask_equal_none(mask100)
                space_group_id = cursor.fetchall()
        elif "210" in directions:
            sql = ""
            if lattice[0] == 'trigonal':
                sql = "select id from trigonal where sg210=%s and name=%s"
            if lattice[0] == 'hexagonal':
                sql = "select id from hexagonal where sg210=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need trigonal or hexagonal, but given %s" % lattice[0].capitalize())
            cursor.execute(sql, (symmetry[0], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            elif len(space_group_id) == 1:
                break
            else:
                if mask210_a != "-1" and mask210_b != "-1":
                    sql += " and mask210a=%s and mask210b=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask210_a, mask210_b))
                if mask210_a != "-1" and mask210_b == "-1":
                    sql += " and mask210a=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask210_a))
                if mask210_a == "-1" and mask210_b != "-1":
                    sql += " and mask210b=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask210_b))
                if mask210_a == "-1" and mask210_b == "-1":
                    __mask_equal_none(mask210)
                space_group_id = cursor.fetchall()
        else:
            raise ValueError("Offered direction is not characteristic direction.")
        break
    while len(symmetry) == 2:
        if "001" and "100" in directions:
            sql = ""
            if lattice[0] == 'trigonal':
                sql = "select id from trigonal where sg001=%s and sg100=%s and name=%s"
            if lattice[0] == 'hexagonal':
                sql = "select id from hexagonal where sg001=%s and sg100=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need trigonal or hexagonal, but given %s" % lattice[0].capitalize())
            cursor.execute(sql, (symmetry[directions.index("001")],
                                 symmetry[directions.index("100")], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            if len(space_group_id) == 1:
                break
            if len(space_group_id) > 1:
                if mask001_a != "-1" and mask001_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                    sql += " and mask001a=%s and mask001b=%s and mask100a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                         bravais, mask001_a, mask001_b, mask100_a, mask100_b))
                if mask001_a == "-1" and mask001_b == "-1" and mask100_a == "-1" and mask100_b == "-1":
                    __mask_equal_none([mask001, mask100])
                if mask001_a == "-1" and mask001_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                    sql += " and mask001b=%s and mask100a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                         bravais, mask001_b, mask100_a, mask100_b))
                if mask001_a != "-1" and mask001_b == "-1" and mask100_a != "-1" and mask100_b != "-1":
                    sql += " and mask001a=%s and mask100a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                         bravais, mask001_a, mask100_a, mask100_b))
                if mask001_a != "-1" and mask001_b != "-1" and mask100_a == "-1" and mask100_b != "-1":
                    sql += " and mask001a=%s and mask001b=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                         bravais, mask001_a, mask001_b, mask100_b))
                if mask001_a != "-1" and mask001_b != "-1" and mask100_a != "-1" and mask100_b == "-1":
                    sql += " and mask001a=%s and mask001b=%s and mask100a=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                         bravais, mask001_a, mask001_b, mask100_a))
                if mask001_a != "-1" and mask001_b != "-1" and mask100_a == "-1" and mask100_b == "-1":
                    sql += " and mask001a=%s and mask001b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                         bravais, mask001_a, mask001_b))
                if mask001_a == "-1" and mask001_b == "-1" and mask100_a != "-1" and mask100_b != "-1":
                    sql += " and mask100a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                         bravais, mask100_a, mask100_b))
                if mask001_a != "-1" and mask001_b == "-1" and mask100_a != "-1" and mask100_b == "-1":
                    sql += " and mask001a=%s and mask100a=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                         bravais, mask001_a, mask100_a))
                if mask001_a != "-1" and mask001_b == "-1" and mask100_a == "-1" and mask100_b != "-1":
                    sql += " and mask001a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                         bravais, mask001_a, mask100_b))
                if mask001_a == "-1" and mask001_b != "-1" and mask100_a == "-1" and mask100_b != "-1":
                    sql += " and mask001b=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                         bravais, mask001_b, mask100_b))
                if mask001_a == "-1" and mask001_b != "-1" and mask100_a != "-1" and mask100_b == "-1":
                    sql += " and mask001b=%s and mask100a=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                         bravais, mask001_b, mask100_a))
                space_group_id = cursor.fetchall()
        elif "001" and "210" in directions:
            sql = ""
            if lattice[0] == 'trigonal':
                sql = "select id from trigonal where sg001=%s and sg210=%s and name=%s"
            if lattice[0] == 'hexagonal':
                sql = "select id from hexagonal where sg001=%s and sg210=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need trigonal or hexagonal, but given %s" % lattice[0].capitalize())
            print(symmetry[directions.index("001")], symmetry[directions.index("210")], bravais)
            cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("210")], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            if len(space_group_id) == 1:
                break
            if len(space_group_id) > 1:
                if mask001_a != "-1" and mask001_b != "-1" and mask210_a != "-1" and mask210_b != "-1":
                    sql += " and mask001a=%s and mask001b=%s and mask210a=%s and mask210b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("210")],
                                         bravais, mask001_a, mask001_b, mask210_a, mask210_b))
                if mask001_a == "-1" and mask001_b == "-1" and mask210_a == "-1" and mask210_b == "-1":
                    __mask_equal_none([mask001, mask210])
                if mask001_a == "-1" and mask001_b != "-1" and mask210_a != "-1" and mask210_b != "-1":
                    sql += " and mask001b=%s and mask210a=%s and mask210b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("210")],
                                         bravais, mask001_b, mask210_a, mask210_b))
                if mask001_a != "-1" and mask001_b == "-1" and mask210_a != "-1" and mask210_b != "-1":
                    sql += " and mask001a=%s and mask210a=%s and mask210b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("210")],
                                         bravais, mask001_a, mask210_a, mask210_b))
                if mask001_a != "-1" and mask001_b != "-1" and mask210_a == "-1" and mask210_b != "-1":
                    sql += " and mask001a=%s and mask001b=%s and mask210b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("210")],
                                         bravais, mask001_a, mask001_b, mask210_b))
                if mask001_a != "-1" and mask001_b != "-1" and mask210_a != "-1" and mask210_b == "-1":
                    sql += " and mask001a=%s and mask001b=%s and mask210a=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("210")],
                                         bravais, mask001_a, mask001_b, mask210_a))
                if mask001_a != "-1" and mask001_b != "-1" and mask210_a == "-1" and mask210_b == "-1":
                    sql += " and mask001a=%s and mask001b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("210")],
                                         bravais, mask001_a, mask001_b))
                if mask001_a == "-1" and mask001_b == "-1" and mask210_a != "-1" and mask210_b != "-1":
                    sql += " and mask210a=%s and mask210b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("210")],
                                         bravais, mask210_a, mask210_b))
                if mask001_a != "-1" and mask001_b == "-1" and mask210_a != "-1" and mask210_b == "-1":
                    sql += " and mask001a=%s and mask210a=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("210")],
                                         bravais, mask001_a, mask210_a))
                if mask001_a != "-1" and mask001_b == "-1" and mask210_a == "-1" and mask210_b != "-1":
                    sql += " and mask001a=%s and mask210b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("210")],
                                         bravais, mask001_a, mask210_b))
                if mask001_a == "-1" and mask001_b != "-1" and mask210_a == "-1" and mask210_b != "-1":
                    sql += " and mask001b=%s and mask210b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("210")],
                                         bravais, mask001_b, mask210_b))
                if mask001_a == "-1" and mask001_b != "-1" and mask210_a != "-1" and mask210_b == "-1":
                    sql += " and mask001b=%s and mask100a=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("210")],
                                         bravais, mask001_b, mask210_a))
                space_group_id = cursor.fetchall()
        elif "210" and "100" in directions:
            sql = ""
            if lattice[0] == 'trigonal':
                sql = "select id from trigonal where sg210=%s and sg100=%s and name=%s"
            if lattice[0] == 'hexagonal':
                sql = "select id from trigonal where sg001=%s and sg100=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need trigonal or hexagonal, but given %s" % lattice[0].capitalize())
            cursor.execute(sql, (symmetry[directions.index("210")], symmetry[directions.index("100")], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            if len(space_group_id) == 1:
                break
            if len(space_group_id) > 1:
                if mask210_a != "-1" and mask210_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                    sql += " and mask210a=%s and mask210b=%s and mask100a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("210")], symmetry[directions.index("100")],
                                         bravais, mask210_a, mask210_b, mask100_a, mask100_b))
                if mask210_a == "-1" and mask210_b == "-1" and mask100_a == "-1" and mask100_b == "-1":
                    __mask_equal_none([mask210, mask100])
                if mask210_a == "-1" and mask210_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                    sql += " and mask210b=%s and mask100a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("210")], symmetry[directions.index("100")],
                                         bravais, mask210_b, mask100_a, mask100_b))
                if mask210_a != "-1" and mask210_b == "-1" and mask100_a != "-1" and mask100_b != "-1":
                    sql += " and mask210a=%s and mask100a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("210")], symmetry[directions.index("100")],
                                         bravais, mask210_a, mask100_a, mask100_b))
                if mask210_a != "-1" and mask210_b != "-1" and mask100_a == "-1" and mask100_b != "-1":
                    sql += " and mask210a=%s and mask210b=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("210")], symmetry[directions.index("100")],
                                         bravais, mask210_a, mask210_b, mask100_b))
                if mask210_a != "-1" and mask210_b != "-1" and mask100_a != "-1" and mask100_b == "-1":
                    sql += " and mask210a=%s and mask210b=%s and mask100a=%s"
                    cursor.execute(sql, (symmetry[directions.index("210")], symmetry[directions.index("100")],
                                         bravais, mask210_a, mask210_b, mask100_a))
                if mask210_a != "-1" and mask210_b != "-1" and mask100_a == "-1" and mask100_b == "-1":
                    sql += " and mask210a=%s and mask210b=%s"
                    cursor.execute(sql, (symmetry[directions.index("210")], symmetry[directions.index("100")],
                                         bravais, mask210_a, mask210_b))
                if mask210_a == "-1" and mask210_b == "-1" and mask100_a != "-1" and mask100_b != "-1":
                    sql += " and mask100a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("210")], symmetry[directions.index("100")],
                                         bravais, mask100_a, mask100_b))
                if mask210_a != "-1" and mask210_b == "-1" and mask100_a != "-1" and mask100_b == "-1":
                    sql += " and mask210a=%s and mask100a=%s"
                    cursor.execute(sql, (symmetry[directions.index("210")], symmetry[directions.index("100")],
                                         bravais, mask210_a, mask100_a))
                if mask210_a != "-1" and mask210_b == "-1" and mask100_a == "-1" and mask100_b != "-1":
                    sql += " and mask210a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("210")], symmetry[directions.index("100")],
                                         bravais, mask210_a, mask100_b))
                if mask210_a == "-1" and mask210_b != "-1" and mask100_a == "-1" and mask100_b != "-1":
                    sql += " and mask210b=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("210")], symmetry[directions.index("100")],
                                         bravais, mask210_b, mask100_b))
                if mask210_a == "-1" and mask210_b != "-1" and mask100_a != "-1" and mask100_b == "-1":
                    sql += " and mask210b=%s and mask100a=%s"
                    cursor.execute(sql, (symmetry[directions.index("210")], symmetry[directions.index("100")],
                                         bravais, mask210_b, mask100_a))
                space_group_id = cursor.fetchall()
        else:
            raise ValueError("Offered directions are not exactly characteristic directions.")
        break
    while len(symmetry) == 3:
        if "001" and "100" and "210" in directions:
            sql = ""
            if lattice[0] == 'trigonal':
                sql = "select id from trigonal where sg001=%s and sg100=%s and sg210=%s and name=%s"
            if lattice[0] == 'hexagonal':
                sql = "select id from hexagonal where sg001=%s and sg100=%s and sg210=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need trigonal or hexagonal, but given %s" % lattice[0].capitalize())
            cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                 symmetry[directions.index("210")], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            if len(space_group_id) == 1:
                break
            if len(space_group_id) > 1:
                if flag == 6:
                    sql += " and mask001a=%s and mask001b=%s and mask100a=%s"
                    sql += " and mask100b=%s and mask210a=%s and mask210b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                         symmetry[directions.index("210")], bravais,
                                         mask001_a, mask001_b, mask100_a, mask100_b, mask210_a, mask210_b))
                if flag == 0:
                    __mask_equal_none([mask001, mask100, mask210])

                if flag == 1:
                    if mask001_a != "-1":
                        sql += " and mask001a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask001_a))
                    if mask001_b != "-1":
                        sql += " and mask001b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask001_b))
                    if mask210_a != "-1":
                        sql += " and mask210a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask210_a))
                    if mask210_b != "-1":
                        sql += " and mask210b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask210_b))
                    if mask100_a != "-1":
                        sql += " and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask100_a))
                    if mask100_b != "-1":
                        sql += " and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask100_b))

                if flag == 2:
                    if mask001_a != "-1" and mask001_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask001_a, mask001_b))
                    if mask001_a != "-1" and mask210_a != "-1":
                        sql += " and mask001a=%s and mask210a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask001_a, mask210_a))
                    if mask001_a != "-1" and mask210_b != "-1":
                        sql += " and mask001a=%s and mask210b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask001_a, mask210_b))
                    if mask001_a != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask001_a, mask100_a))
                    if mask001_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask210a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask001_a, mask100_b))
                    if mask001_b != "-1" and mask210_a != "-1":
                        sql += " and mask001b=%s and mask210a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask001_b, mask210_a))
                    if mask001_b != "-1" and mask210_b != "-1":
                        sql += "and mask001b=%s and mask210b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask001_b, mask210_b))
                    if mask001_b != "-1" and mask100_a != "-1":
                        sql += " and mask001b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask001_b, mask100_a))
                    if mask001_b != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask001_b, mask100_b))
                    if mask210_a != "-1" and mask210_b != "-1":
                        sql += " and mask210a=%s and mask210b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask210_a, mask210_b))
                    if mask210_a != "-1" and mask100_a != "-1":
                        sql += " and mask210a=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask210_a, mask100_a))
                    if mask210_a != "-1" and mask100_b != "-1":
                        sql += " and mask210a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask210_a, mask100_b))
                    if mask210_b != "-1" and mask100_a != "-1":
                        sql += " and mask210b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask210_b, mask100_a))
                    if mask210_b != "-1" and mask100_b != "-1":
                        sql += " and mask210b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask210_b, mask100_b))
                    if mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais, mask100_a, mask100_b))

                if flag == 3:
                    if mask001_a != "-1" and mask001_b != "-1" and mask210_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask210a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask001_b, mask210_a))
                    if mask001_a != "-1" and mask001_b != "-1" and mask210_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask210b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask001_b, mask210_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask001_b, mask100_a))
                    if mask001_a != "-1" and mask001_b != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask001_b, mask100_b))
                    if mask001_a != "-1" and mask210_a != "-1" and mask210_b != "-1":
                        sql += " and mask001a=%s and mask210a=%s and mask210b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask210_a, mask210_b))
                    if mask001_a != "-1" and mask210_a != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask210a=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask210_a, mask100_a))
                    if mask001_a != "-1" and mask210_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask210a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask210_a, mask100_b))
                    if mask001_a != "-1" and mask210_b != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask210b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask210_b, mask100_a))
                    if mask001_a != "-1" and mask210_b != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask210b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask210_b, mask100_b))
                    if mask001_a != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask100_a, mask100_b))
                    if mask001_b != "-1" and mask210_a != "-1" and mask210_b != "-1":
                        sql += " and mask001b=%s and mask210a=%s and mask210b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_b, mask210_a, mask210_b))
                    if mask001_b != "-1" and mask210_a != "-1" and mask100_a != "-1":
                        sql += " and mask001b=%s and mask210a=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_b, mask210_a, mask100_a))
                    if mask001_b != "-1" and mask210_a != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask210a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_b, mask210_a, mask100_b))
                    if mask001_b != "-1" and mask210_b != "-1" and mask100_a != "-1":
                        sql += " and mask001b=%s and mask210b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_b, mask210_b, mask100_a))
                    if mask001_b != "-1" and mask210_b != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask210a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_b, mask210_b, mask100_b))
                    if mask001_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_b, mask100_a, mask100_b))
                    if mask210_a != "-1" and mask210_b != "-1" and mask100_a != "-1":
                        sql += " and mask210a=%s and mask210b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask210_a, mask210_b, mask100_a))
                    if mask210_a != "-1" and mask210_b != "-1" and mask100_b != "-1":
                        sql += " and mask210a=%s and mask210b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask210_a, mask210_b, mask100_b))
                    if mask210_a != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask210a=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask210_a, mask100_a, mask100_b))
                    if mask210_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask210b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask210_b, mask100_a, mask100_b))

                if flag == 4:
                    if mask001_a != "-1" and mask001_b != "-1" and mask210_a != "-1" and mask210_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask210a=%s and mask210b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask001_b, mask210_a, mask210_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask210_a != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask210a=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask001_b, mask210_a, mask100_a))
                    if mask001_a != "-1" and mask001_b != "-1" and mask210_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask210a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask001_b, mask210_a, mask100_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask210_b != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask210b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask001_b, mask210_b, mask100_a))
                    if mask001_a != "-1" and mask001_b != "-1" and mask210_b != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask210b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask001_b, mask210_b, mask100_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask001_b, mask100_a, mask100_b))
                    if mask001_a != "-1" and mask210_a != "-1" and mask210_b != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask210a=%s and mask210b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask210_a, mask210_b, mask100_a))
                    if mask001_a != "-1" and mask210_a != "-1" and mask210_b != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask210a=%s and mask210b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask210_a, mask210_b, mask100_b))
                    if mask001_a != "-1" and mask210_a != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask210a=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask210_a, mask100_a, mask100_b))
                    if mask001_a != "-1" and mask210_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask210b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask210_b, mask100_a, mask100_b))
                    if mask001_b != "-1" and mask210_a != "-1" and mask210_b != "-1" and mask100_a != "-1":
                        sql += " and mask001b=%s and mask210a=%s and mask210b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_b, mask210_a, mask210_b, mask100_a))
                    if mask001_b != "-1" and mask210_a != "-1" and mask210_b != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask210a=%s and mask210b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_b, mask210_a, mask210_b, mask100_b))
                    if mask001_b != "-1" and mask210_a != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask210a=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_b, mask210_a, mask100_a, mask100_b))
                    if mask001_b != "-1" and mask210_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask210b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_b, mask210_b, mask100_a, mask100_b))
                    if mask210_a != "-1" and mask210_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask210a=%s and mask210b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask210_a, mask210_b, mask100_a, mask100_b))

                if flag == 5:
                    if mask001_b != "-1" and mask210_a != "-1" and mask210_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask210a=%s and mask210b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_b, mask210_a, mask210_b, mask100_a, mask100_b))
                    if mask001_a != "-1" and mask210_a != "-1" and mask210_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask210a=%s and mask210b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask210_a, mask210_b, mask100_a, mask100_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask210_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask210b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask001_b, mask210_b, mask100_a, mask100_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask210_a != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask210a=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask001_b, mask210_a, mask100_a, mask100_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask210_a != "-1" and mask210_b != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask210a=%s and mask210b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask001_b, mask210_a, mask210_b, mask100_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask210_a != "-1" and mask210_b != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask210a=%s and mask210b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("210")], bravais,
                                             mask001_a, mask001_b, mask210_a, mask210_b, mask100_a))

                space_group_id = cursor.fetchall()
        else:
            raise ValueError("Offered directions are not exactly characteristic directions.")
        break
    cursor.close()
    connect.close()
    print(space_group_id)
    return space_group_id
