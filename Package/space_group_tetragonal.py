import pymysql

space_group_id = None


def __mask_equal_none(mask):
    raise ValueError("%s is/are None" % mask)


def __main_error():
    raise ValueError("Offered info is not enough to determine space group.")


def match_space_group_tetragonal(mask001, mask100, mask110, directions, symmetry, bravais, lattice):
    mask001_a = "-1"
    mask001_b = "-1"
    mask100_a = "-1"
    mask100_b = "-1"
    mask110_a = "-1"
    mask110_b = "-1"
    if len(mask001):
        mask001_a = mask001[0]
        mask001_b = mask001[1]
    if len(mask100):
        mask100_a = mask100[0]
        mask100_b = mask100[1]
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
            if lattice[0] == 'tetragonal':
                sql = "select id from tetragonal where sg001=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need tetragonal or hexagonal, but given %s" % lattice[0].capitalize())
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
            if lattice[0] == 'tetragonal':
                sql = "select id from tetragonal where sg100=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need tetragonal or hexagonal, but given %s" % lattice[0].capitalize())
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
        elif "110" in directions:
            sql = ""
            if lattice[0] == 'tetragonal':
                sql = "select id from tetragonal where sg110=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need tetragonal or hexagonal, but given %s" % lattice[0].capitalize())
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
        if "001" and "100" in directions:
            sql = ""
            if lattice[0] == 'tetragonal':
                sql = "select id from tetragonal where sg001=%s and sg100=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need tetragonal or hexagonal, but given %s" % lattice[0].capitalize())
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
        elif "001" and "110" in directions:
            sql = ""
            if lattice[0] == 'tetragonal':
                sql = "select id from tetragonal where sg001=%s and sg110=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need tetragonal or hexagonal, but given %s" % lattice[0].capitalize())
            print(symmetry[directions.index("001")], symmetry[directions.index("110")], bravais)
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
                    sql += " and mask001b=%s and mask100a=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("110")],
                                         bravais, mask001_b, mask110_a))
                space_group_id = cursor.fetchall()
        elif "110" and "100" in directions:
            sql = ""
            if lattice[0] == 'tetragonal':
                sql = "select id from tetragonal where sg110=%s and sg100=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need tetragonal or hexagonal, but given %s" % lattice[0].capitalize())
            cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("100")], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            if len(space_group_id) == 1:
                break
            if len(space_group_id) > 1:
                if mask110_a != "-1" and mask110_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                    sql += " and mask110a=%s and mask110b=%s and mask100a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("100")],
                                         bravais, mask110_a, mask110_b, mask100_a, mask100_b))
                if mask110_a == "-1" and mask110_b == "-1" and mask100_a == "-1" and mask100_b == "-1":
                    __mask_equal_none([mask110, mask100])
                if mask110_a == "-1" and mask110_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                    sql += " and mask110b=%s and mask100a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("100")],
                                         bravais, mask110_b, mask100_a, mask100_b))
                if mask110_a != "-1" and mask110_b == "-1" and mask100_a != "-1" and mask100_b != "-1":
                    sql += " and mask110a=%s and mask100a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("100")],
                                         bravais, mask110_a, mask100_a, mask100_b))
                if mask110_a != "-1" and mask110_b != "-1" and mask100_a == "-1" and mask100_b != "-1":
                    sql += " and mask110a=%s and mask110b=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("100")],
                                         bravais, mask110_a, mask110_b, mask100_b))
                if mask110_a != "-1" and mask110_b != "-1" and mask100_a != "-1" and mask100_b == "-1":
                    sql += " and mask110a=%s and mask110b=%s and mask100a=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("100")],
                                         bravais, mask110_a, mask110_b, mask100_a))
                if mask110_a != "-1" and mask110_b != "-1" and mask100_a == "-1" and mask100_b == "-1":
                    sql += " and mask110a=%s and mask110b=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("100")],
                                         bravais, mask110_a, mask110_b))
                if mask110_a == "-1" and mask110_b == "-1" and mask100_a != "-1" and mask100_b != "-1":
                    sql += " and mask100a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("100")],
                                         bravais, mask100_a, mask100_b))
                if mask110_a != "-1" and mask110_b == "-1" and mask100_a != "-1" and mask100_b == "-1":
                    sql += " and mask110a=%s and mask100a=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("100")],
                                         bravais, mask110_a, mask100_a))
                if mask110_a != "-1" and mask110_b == "-1" and mask100_a == "-1" and mask100_b != "-1":
                    sql += " and mask110a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("100")],
                                         bravais, mask110_a, mask100_b))
                if mask110_a == "-1" and mask110_b != "-1" and mask100_a == "-1" and mask100_b != "-1":
                    sql += " and mask110b=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("100")],
                                         bravais, mask110_b, mask100_b))
                if mask110_a == "-1" and mask110_b != "-1" and mask100_a != "-1" and mask100_b == "-1":
                    sql += " and mask110b=%s and mask100a=%s"
                    cursor.execute(sql, (symmetry[directions.index("110")], symmetry[directions.index("100")],
                                         bravais, mask110_b, mask100_a))
                space_group_id = cursor.fetchall()
        else:
            raise ValueError("Offered directions are not exactly characteristic directions.")
        break
    while len(symmetry) == 3:
        if "001" and "100" and "110" in directions:
            sql = ""
            if lattice[0] == 'tetragonal':
                sql = "select id from tetragonal where sg001=%s and sg100=%s and sg110=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need tetragonal or hexagonal, but given %s" % lattice[0].capitalize())
            cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                 symmetry[directions.index("110")], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            if len(space_group_id) == 1:
                break
            if len(space_group_id) > 1:
                if flag == 6:
                    sql += " and mask001a=%s and mask001b=%s and mask100a=%s"
                    sql += " and mask100b=%s and mask110a=%s and mask110b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                         symmetry[directions.index("110")], bravais,
                                         mask001_a, mask001_b, mask100_a, mask100_b, mask110_a, mask110_b))
                if flag == 0:
                    __mask_equal_none([mask001, mask100, mask110])

                if flag == 1:
                    if mask001_a != "-1":
                        sql += " and mask001a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask001_a))
                    if mask001_b != "-1":
                        sql += " and mask001b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask001_b))
                    if mask110_a != "-1":
                        sql += " and mask110a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask110_a))
                    if mask110_b != "-1":
                        sql += " and mask110b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask110_b))
                    if mask100_a != "-1":
                        sql += " and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask100_a))
                    if mask100_b != "-1":
                        sql += " and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask100_b))

                if flag == 2:
                    if mask001_a != "-1" and mask001_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask001_a, mask001_b))
                    if mask001_a != "-1" and mask110_a != "-1":
                        sql += " and mask001a=%s and mask110a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask001_a, mask110_a))
                    if mask001_a != "-1" and mask110_b != "-1":
                        sql += " and mask001a=%s and mask110b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask001_a, mask110_b))
                    if mask001_a != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask001_a, mask100_a))
                    if mask001_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask110a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask001_a, mask100_b))
                    if mask001_b != "-1" and mask110_a != "-1":
                        sql += " and mask001b=%s and mask110a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask001_b, mask110_a))
                    if mask001_b != "-1" and mask110_b != "-1":
                        sql += "and mask001b=%s and mask110b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask001_b, mask110_b))
                    if mask001_b != "-1" and mask100_a != "-1":
                        sql += " and mask001b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask001_b, mask100_a))
                    if mask001_b != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask001_b, mask100_b))
                    if mask110_a != "-1" and mask110_b != "-1":
                        sql += " and mask110a=%s and mask110b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask110_a, mask110_b))
                    if mask110_a != "-1" and mask100_a != "-1":
                        sql += " and mask110a=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask110_a, mask100_a))
                    if mask110_a != "-1" and mask100_b != "-1":
                        sql += " and mask110a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask110_a, mask100_b))
                    if mask110_b != "-1" and mask100_a != "-1":
                        sql += " and mask110b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask110_b, mask100_a))
                    if mask110_b != "-1" and mask100_b != "-1":
                        sql += " and mask110b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask110_b, mask100_b))
                    if mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais, mask100_a, mask100_b))

                if flag == 3:
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_a))
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask100_a))
                    if mask001_a != "-1" and mask001_b != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask100_b))
                    if mask001_a != "-1" and mask110_a != "-1" and mask110_b != "-1":
                        sql += " and mask001a=%s and mask110a=%s and mask110b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_a, mask110_b))
                    if mask001_a != "-1" and mask110_a != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask110a=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_a, mask100_a))
                    if mask001_a != "-1" and mask110_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask110a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_a, mask100_b))
                    if mask001_a != "-1" and mask110_b != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask110b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_b, mask100_a))
                    if mask001_a != "-1" and mask110_b != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask110b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_b, mask100_b))
                    if mask001_a != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask100_a, mask100_b))
                    if mask001_b != "-1" and mask110_a != "-1" and mask110_b != "-1":
                        sql += " and mask001b=%s and mask110a=%s and mask110b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_a, mask110_b))
                    if mask001_b != "-1" and mask110_a != "-1" and mask100_a != "-1":
                        sql += " and mask001b=%s and mask110a=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_a, mask100_a))
                    if mask001_b != "-1" and mask110_a != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask110a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_a, mask100_b))
                    if mask001_b != "-1" and mask110_b != "-1" and mask100_a != "-1":
                        sql += " and mask001b=%s and mask110b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_b, mask100_a))
                    if mask001_b != "-1" and mask110_b != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask110a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_b, mask100_b))
                    if mask001_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask100_a, mask100_b))
                    if mask110_a != "-1" and mask110_b != "-1" and mask100_a != "-1":
                        sql += " and mask110a=%s and mask110b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask110_a, mask110_b, mask100_a))
                    if mask110_a != "-1" and mask110_b != "-1" and mask100_b != "-1":
                        sql += " and mask110a=%s and mask110b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask110_a, mask110_b, mask100_b))
                    if mask110_a != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask110a=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask110_a, mask100_a, mask100_b))
                    if mask110_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask110b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask110_b, mask100_a, mask100_b))

                if flag == 4:
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_a != "-1" and mask110_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110a=%s and mask110b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_a, mask110_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_a != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110a=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_a, mask100_a))
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_a, mask100_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_b != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_b, mask100_a))
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_b != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_b, mask100_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask100_a, mask100_b))
                    if mask001_a != "-1" and mask110_a != "-1" and mask110_b != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask110a=%s and mask110b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_a, mask110_b, mask100_a))
                    if mask001_a != "-1" and mask110_a != "-1" and mask110_b != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask110a=%s and mask110b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_a, mask110_b, mask100_b))
                    if mask001_a != "-1" and mask110_a != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask110a=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_a, mask100_a, mask100_b))
                    if mask001_a != "-1" and mask110_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask110b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_b, mask100_a, mask100_b))
                    if mask001_b != "-1" and mask110_a != "-1" and mask110_b != "-1" and mask100_a != "-1":
                        sql += " and mask001b=%s and mask110a=%s and mask110b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_a, mask110_b, mask100_a))
                    if mask001_b != "-1" and mask110_a != "-1" and mask110_b != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask110a=%s and mask110b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_a, mask110_b, mask100_b))
                    if mask001_b != "-1" and mask110_a != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask110a=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_a, mask100_a, mask100_b))
                    if mask001_b != "-1" and mask110_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask110b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_b, mask100_a, mask100_b))
                    if mask110_a != "-1" and mask110_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask110a=%s and mask110b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask110_a, mask110_b, mask100_a, mask100_b))

                if flag == 5:
                    if mask001_b != "-1" and mask110_a != "-1" and mask110_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask110a=%s and mask110b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_b, mask110_a, mask110_b, mask100_a, mask100_b))
                    if mask001_a != "-1" and mask110_a != "-1" and mask110_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask110a=%s and mask110b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask110_a, mask110_b, mask100_a, mask100_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_b, mask100_a, mask100_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_a != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110a=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_a, mask100_a, mask100_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_a != "-1" and mask110_b != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110a=%s and mask110b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_a, mask110_b, mask100_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask110_a != "-1" and mask110_b != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask110a=%s and mask110b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("110")], bravais,
                                             mask001_a, mask001_b, mask110_a, mask110_b, mask100_a))

                space_group_id = cursor.fetchall()
        else:
            raise ValueError("Offered directions are not exactly characteristic directions.")
        break
    cursor.close()
    connect.close()
    print(space_group_id)
    return space_group_id
