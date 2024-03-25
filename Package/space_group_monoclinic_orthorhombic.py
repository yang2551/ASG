import pymysql

space_group_id = None


def __mask_equal_none(mask):
    raise ValueError("%s is/are None" % mask)


def __main_error():
    raise ValueError("Offered info is not enough to determine space group.")


def match_space_group_monoclinic_orthorhombic(mask001, mask100, mask010, directions, symmetry, bravais, lattice):
    global space_group_id
    mask001_a = "-1"
    mask001_b = "-1"
    mask100_a = "-1"
    mask100_b = "-1"
    mask010_a = "-1"
    mask010_b = "-1"
    if len(mask001):
        mask001_a = mask001[0]
        mask001_b = mask001[1]
    if len(mask100):
        mask100_a = mask100[0]
        mask100_b = mask100[1]
    if len(mask010):
        mask010_a = mask010[0]
        mask010_b = mask010[1]
    flag = 0
    if mask001_a != "-1":
        flag += 1
    if mask001_b != "-1":
        flag += 1
    if mask010_a != "-1":
        flag += 1
    if mask010_b != "-1":
        flag += 1
    if mask100_a != "-1":
        flag += 1
    if mask100_b != "-1":
        flag += 1
    connect = pymysql.connect(host='localhost', user='root', password='123456',
                              database='mybase', charset='utf8')
    cursor = connect.cursor()
    while len(symmetry) == 1:
        if "001" in directions:
            sql = ""
            if lattice[0] == 'monoclinic':
                sql = "select id from monoclinic where sg001=%s and name=%s"
            if lattice[0] == 'orthorhombic':
                sql = "select id from orthorhombic where sg001=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need Monoclinic or Orthorhombic, but given %s" % lattice[0].capitalize())
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
            if lattice[0] == 'monoclinic':
                sql = "select id from monoclinic where sg100=%s and name=%s"
            if lattice[0] == 'orthorhombic':
                sql = "select id from orthorhombic where sg100=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need Monoclinic or Orthorhombic, but given %s" % lattice[0].capitalize())
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
        elif "010" in directions:
            sql = ""
            if lattice[0] == 'monoclinic':
                sql = "select id from monoclinic where sg010=%s and name=%s"
            if lattice[0] == 'orthorhombic':
                sql = "select id from orthorhombic where sg010=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need Monoclinic or Orthorhombic, but given %s" % lattice[0].capitalize())
            cursor.execute(sql, (symmetry[0], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            elif len(space_group_id) == 1:
                break
            else:
                if mask010_a != "-1" and mask010_b != "-1":
                    sql += " and mask010a=%s and mask010b=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask010_a, mask010_b))
                if mask010_a != "-1" and mask010_b == "-1":
                    sql += " and mask010a=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask010_a))
                if mask010_a == "-1" and mask010_b != "-1":
                    sql += " and mask010b=%s"
                    cursor.execute(sql, (symmetry[0], bravais, mask010_b))
                if mask010_a == "-1" and mask010_b == "-1":
                    __mask_equal_none(mask010)
                space_group_id = cursor.fetchall()
        else:
            raise ValueError("Offered direction is not characteristic direction.")
        break
    while len(symmetry) == 2:
        if "001" and "100" in directions:
            sql = ""
            if lattice[0] == 'monoclinic':
                sql = "select id from monoclinic where sg001=%s and sg100=%s and name=%s"
            if lattice[0] == 'orthorhombic':
                sql = "select id from orthorhombic where sg001=%s and sg100=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need Monoclinic or Orthorhombic, but given %s" % lattice[0].capitalize())
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
        elif "001" and "010" in directions:
            sql = ""
            if lattice[0] == 'monoclinic':
                sql = "select id from monoclinic where sg001=%s and sg010=%s and name=%s"
            if lattice[0] == 'orthorhombic':
                sql = "select id from orthorhombic where sg001=%s and sg010=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need Monoclinic or Orthorhombic, but given %s" % lattice[0].capitalize())
            print(symmetry[directions.index("001")], symmetry[directions.index("010")], bravais)
            cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("010")], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            if len(space_group_id) == 1:
                break
            if len(space_group_id) > 1:
                if mask001_a != "-1" and mask001_b != "-1" and mask010_a != "-1" and mask010_b != "-1":
                    sql += " and mask001a=%s and mask001b=%s and mask010a=%s and mask010b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("010")],
                                         bravais, mask001_a, mask001_b, mask010_a, mask010_b))
                if mask001_a == "-1" and mask001_b == "-1" and mask010_a == "-1" and mask010_b == "-1":
                    __mask_equal_none([mask001, mask010])
                if mask001_a == "-1" and mask001_b != "-1" and mask010_a != "-1" and mask010_b != "-1":
                    sql += " and mask001b=%s and mask010a=%s and mask010b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("010")],
                                         bravais, mask001_b, mask010_a, mask010_b))
                if mask001_a != "-1" and mask001_b == "-1" and mask010_a != "-1" and mask010_b != "-1":
                    sql += " and mask001a=%s and mask010a=%s and mask010b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("010")],
                                         bravais, mask001_a, mask010_a, mask010_b))
                if mask001_a != "-1" and mask001_b != "-1" and mask010_a == "-1" and mask010_b != "-1":
                    sql += " and mask001a=%s and mask001b=%s and mask010b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("010")],
                                         bravais, mask001_a, mask001_b, mask010_b))
                if mask001_a != "-1" and mask001_b != "-1" and mask010_a != "-1" and mask010_b == "-1":
                    sql += " and mask001a=%s and mask001b=%s and mask010a=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("010")],
                                         bravais, mask001_a, mask001_b, mask010_a))
                if mask001_a != "-1" and mask001_b != "-1" and mask010_a == "-1" and mask010_b == "-1":
                    sql += " and mask001a=%s and mask001b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("010")],
                                         bravais, mask001_a, mask001_b))
                if mask001_a == "-1" and mask001_b == "-1" and mask010_a != "-1" and mask010_b != "-1":
                    sql += " and mask010a=%s and mask010b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("010")],
                                         bravais, mask010_a, mask010_b))
                if mask001_a != "-1" and mask001_b == "-1" and mask010_a != "-1" and mask010_b == "-1":
                    sql += " and mask001a=%s and mask010a=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("010")],
                                         bravais, mask001_a, mask010_a))
                if mask001_a != "-1" and mask001_b == "-1" and mask010_a == "-1" and mask010_b != "-1":
                    sql += " and mask001a=%s and mask010b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("010")],
                                         bravais, mask001_a, mask010_b))
                if mask001_a == "-1" and mask001_b != "-1" and mask010_a == "-1" and mask010_b != "-1":
                    sql += " and mask001b=%s and mask010b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("010")],
                                         bravais, mask001_b, mask010_b))
                if mask001_a == "-1" and mask001_b != "-1" and mask010_a != "-1" and mask010_b == "-1":
                    sql += " and mask001b=%s and mask100a=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("010")],
                                         bravais, mask001_b, mask010_a))
                space_group_id = cursor.fetchall()
        elif "010" and "100" in directions:
            sql = ""
            if lattice[0] == 'monoclinic':
                sql = "select id from monoclinic where sg010=%s and sg100=%s and name=%s"
            if lattice[0] == 'orthorhombic':
                sql = "select id from monoclinic where sg001=%s and sg100=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need Monoclinic or Orthorhombic, but given %s" % lattice[0].capitalize())
            cursor.execute(sql, (symmetry[directions.index("010")], symmetry[directions.index("100")], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            if len(space_group_id) == 1:
                break
            if len(space_group_id) > 1:
                if mask010_a != "-1" and mask010_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                    sql += " and mask010a=%s and mask010b=%s and mask100a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("010")], symmetry[directions.index("100")],
                                         bravais, mask010_a, mask010_b, mask100_a, mask100_b))
                if mask010_a == "-1" and mask010_b == "-1" and mask100_a == "-1" and mask100_b == "-1":
                    __mask_equal_none([mask010, mask100])
                if mask010_a == "-1" and mask010_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                    sql += " and mask010b=%s and mask100a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("010")], symmetry[directions.index("100")],
                                         bravais, mask010_b, mask100_a, mask100_b))
                if mask010_a != "-1" and mask010_b == "-1" and mask100_a != "-1" and mask100_b != "-1":
                    sql += " and mask010a=%s and mask100a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("010")], symmetry[directions.index("100")],
                                         bravais, mask010_a, mask100_a, mask100_b))
                if mask010_a != "-1" and mask010_b != "-1" and mask100_a == "-1" and mask100_b != "-1":
                    sql += " and mask010a=%s and mask010b=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("010")], symmetry[directions.index("100")],
                                         bravais, mask010_a, mask010_b, mask100_b))
                if mask010_a != "-1" and mask010_b != "-1" and mask100_a != "-1" and mask100_b == "-1":
                    sql += " and mask010a=%s and mask010b=%s and mask100a=%s"
                    cursor.execute(sql, (symmetry[directions.index("010")], symmetry[directions.index("100")],
                                         bravais, mask010_a, mask010_b, mask100_a))
                if mask010_a != "-1" and mask010_b != "-1" and mask100_a == "-1" and mask100_b == "-1":
                    sql += " and mask010a=%s and mask010b=%s"
                    cursor.execute(sql, (symmetry[directions.index("010")], symmetry[directions.index("100")],
                                         bravais, mask010_a, mask010_b))
                if mask010_a == "-1" and mask010_b == "-1" and mask100_a != "-1" and mask100_b != "-1":
                    sql += " and mask100a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("010")], symmetry[directions.index("100")],
                                         bravais, mask100_a, mask100_b))
                if mask010_a != "-1" and mask010_b == "-1" and mask100_a != "-1" and mask100_b == "-1":
                    sql += " and mask010a=%s and mask100a=%s"
                    cursor.execute(sql, (symmetry[directions.index("010")], symmetry[directions.index("100")],
                                         bravais, mask010_a, mask100_a))
                if mask010_a != "-1" and mask010_b == "-1" and mask100_a == "-1" and mask100_b != "-1":
                    sql += " and mask010a=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("010")], symmetry[directions.index("100")],
                                         bravais, mask010_a, mask100_b))
                if mask010_a == "-1" and mask010_b != "-1" and mask100_a == "-1" and mask100_b != "-1":
                    sql += " and mask010b=%s and mask100b=%s"
                    cursor.execute(sql, (symmetry[directions.index("010")], symmetry[directions.index("100")],
                                         bravais, mask010_b, mask100_b))
                if mask010_a == "-1" and mask010_b != "-1" and mask100_a != "-1" and mask100_b == "-1":
                    sql += " and mask010b=%s and mask100a=%s"
                    cursor.execute(sql, (symmetry[directions.index("010")], symmetry[directions.index("100")],
                                         bravais, mask010_b, mask100_a))
                space_group_id = cursor.fetchall()
        else:
            raise ValueError("Offered directions are not exactly characteristic directions.")
        break
    while len(symmetry) == 3:
        if "001" and "100" and "010" in directions:
            sql = ""
            if lattice[0] == 'monoclinic':
                sql = "select id from monoclinic where sg001=%s and sg100=%s and sg010=%s and name=%s"
            if lattice[0] == 'orthorhombic':
                sql = "select id from orthorhombic where sg001=%s and sg100=%s and sg010=%s and name=%s"
            else:
                ValueError("Wrong Lattice. Need Monoclinic or Orthorhombic, but given %s" % lattice[0].capitalize())
            cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                 symmetry[directions.index("010")], bravais))
            space_group_id = cursor.fetchall()
            if len(space_group_id) < 1:
                __main_error()
            if len(space_group_id) == 1:
                break
            if len(space_group_id) > 1:
                if flag == 6:
                    sql += " and mask001a=%s and mask001b=%s and mask100a=%s"
                    sql += " and mask100b=%s and mask010a=%s and mask010b=%s"
                    cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                         symmetry[directions.index("010")], bravais,
                                         mask001_a, mask001_b, mask100_a, mask100_b, mask010_a, mask010_b))
                if flag == 0:
                    __mask_equal_none([mask001, mask100, mask010])

                if flag == 1:
                    if mask001_a != "-1":
                        sql += " and mask001a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask001_a))
                    if mask001_b != "-1":
                        sql += " and mask001b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask001_b))
                    if mask010_a != "-1":
                        sql += " and mask010a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask010_a))
                    if mask010_b != "-1":
                        sql += " and mask010b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask010_b))
                    if mask100_a != "-1":
                        sql += " and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask100_a))
                    if mask100_b != "-1":
                        sql += " and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask100_b))

                if flag == 2:
                    if mask001_a != "-1" and mask001_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask001_a, mask001_b))
                    if mask001_a != "-1" and mask010_a != "-1":
                        sql += " and mask001a=%s and mask010a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask001_a, mask010_a))
                    if mask001_a != "-1" and mask010_b != "-1":
                        sql += " and mask001a=%s and mask010b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask001_a, mask010_b))
                    if mask001_a != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask001_a, mask100_a))
                    if mask001_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask010a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask001_a, mask100_b))
                    if mask001_b != "-1" and mask010_a != "-1":
                        sql += " and mask001b=%s and mask010a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask001_b, mask010_a))
                    if mask001_b != "-1" and mask010_b != "-1":
                        sql += "and mask001b=%s and mask010b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask001_b, mask010_b))
                    if mask001_b != "-1" and mask100_a != "-1":
                        sql += " and mask001b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask001_b, mask100_a))
                    if mask001_b != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask001_b, mask100_b))
                    if mask010_a != "-1" and mask010_b != "-1":
                        sql += " and mask010a=%s and mask010b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask010_a, mask010_b))
                    if mask010_a != "-1" and mask100_a != "-1":
                        sql += " and mask010a=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask010_a, mask100_a))
                    if mask010_a != "-1" and mask100_b != "-1":
                        sql += " and mask010a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask010_a, mask100_b))
                    if mask010_b != "-1" and mask100_a != "-1":
                        sql += " and mask010b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask010_b, mask100_a))
                    if mask010_b != "-1" and mask100_b != "-1":
                        sql += " and mask010b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask010_b, mask100_b))
                    if mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais, mask100_a, mask100_b))

                if flag == 3:
                    if mask001_a != "-1" and mask001_b != "-1" and mask010_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask010a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask001_b, mask010_a))
                    if mask001_a != "-1" and mask001_b != "-1" and mask010_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask010b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask001_b, mask010_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask001_b, mask100_a))
                    if mask001_a != "-1" and mask001_b != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask001_b, mask100_b))
                    if mask001_a != "-1" and mask010_a != "-1" and mask010_b != "-1":
                        sql += " and mask001a=%s and mask010a=%s and mask010b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask010_a, mask010_b))
                    if mask001_a != "-1" and mask010_a != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask010a=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask010_a, mask100_a))
                    if mask001_a != "-1" and mask010_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask010a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask010_a, mask100_b))
                    if mask001_a != "-1" and mask010_b != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask010b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask010_b, mask100_a))
                    if mask001_a != "-1" and mask010_b != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask010b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask010_b, mask100_b))
                    if mask001_a != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask100_a, mask100_b))
                    if mask001_b != "-1" and mask010_a != "-1" and mask010_b != "-1":
                        sql += " and mask001b=%s and mask010a=%s and mask010b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_b, mask010_a, mask010_b))
                    if mask001_b != "-1" and mask010_a != "-1" and mask100_a != "-1":
                        sql += " and mask001b=%s and mask010a=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_b, mask010_a, mask100_a))
                    if mask001_b != "-1" and mask010_a != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask010a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_b, mask010_a, mask100_b))
                    if mask001_b != "-1" and mask010_b != "-1" and mask100_a != "-1":
                        sql += " and mask001b=%s and mask010b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_b, mask010_b, mask100_a))
                    if mask001_b != "-1" and mask010_b != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask010a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_b, mask010_b, mask100_b))
                    if mask001_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_b, mask100_a, mask100_b))
                    if mask010_a != "-1" and mask010_b != "-1" and mask100_a != "-1":
                        sql += " and mask010a=%s and mask010b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask010_a, mask010_b, mask100_a))
                    if mask010_a != "-1" and mask010_b != "-1" and mask100_b != "-1":
                        sql += " and mask010a=%s and mask010b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask010_a, mask010_b, mask100_b))
                    if mask010_a != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask010a=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask010_a, mask100_a, mask100_b))
                    if mask010_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask010b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask010_b, mask100_a, mask100_b))

                if flag == 4:
                    if mask001_a != "-1" and mask001_b != "-1" and mask010_a != "-1" and mask010_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask010a=%s and mask010b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask001_b, mask010_a, mask010_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask010_a != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask010a=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask001_b, mask010_a, mask100_a))
                    if mask001_a != "-1" and mask001_b != "-1" and mask010_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask010a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask001_b, mask010_a, mask100_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask010_b != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask010b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask001_b, mask010_b, mask100_a))
                    if mask001_a != "-1" and mask001_b != "-1" and mask010_b != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask010b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask001_b, mask010_b, mask100_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask001_b, mask100_a, mask100_b))
                    if mask001_a != "-1" and mask010_a != "-1" and mask010_b != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask010a=%s and mask010b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask010_a, mask010_b, mask100_a))
                    if mask001_a != "-1" and mask010_a != "-1" and mask010_b != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask010a=%s and mask010b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask010_a, mask010_b, mask100_b))
                    if mask001_a != "-1" and mask010_a != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask010a=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask010_a, mask100_a, mask100_b))
                    if mask001_a != "-1" and mask010_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask010b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask010_b, mask100_a, mask100_b))
                    if mask001_b != "-1" and mask010_a != "-1" and mask010_b != "-1" and mask100_a != "-1":
                        sql += " and mask001b=%s and mask010a=%s and mask010b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_b, mask010_a, mask010_b, mask100_a))
                    if mask001_b != "-1" and mask010_a != "-1" and mask010_b != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask010a=%s and mask010b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_b, mask010_a, mask010_b, mask100_b))
                    if mask001_b != "-1" and mask010_a != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask010a=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_b, mask010_a, mask100_a, mask100_b))
                    if mask001_b != "-1" and mask010_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask010b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_b, mask010_b, mask100_a, mask100_b))
                    if mask010_a != "-1" and mask010_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask010a=%s and mask010b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask010_a, mask010_b, mask100_a, mask100_b))

                if flag == 5:
                    if mask001_b != "-1" and mask010_a != "-1" and mask010_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001b=%s and mask010a=%s and mask010b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_b, mask010_a, mask010_b, mask100_a, mask100_b))
                    if mask001_a != "-1" and mask010_a != "-1" and mask010_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask010a=%s and mask010b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask010_a, mask010_b, mask100_a, mask100_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask010_b != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask010b=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask001_b, mask010_b, mask100_a, mask100_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask010_a != "-1" and mask100_a != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask010a=%s and mask100a=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask001_b, mask010_a, mask100_a, mask100_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask010_a != "-1" and mask010_b != "-1" and mask100_b != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask010a=%s and mask010b=%s and mask100b=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask001_b, mask010_a, mask010_b, mask100_b))
                    if mask001_a != "-1" and mask001_b != "-1" and mask010_a != "-1" and mask010_b != "-1" and mask100_a != "-1":
                        sql += " and mask001a=%s and mask001b=%s and mask010a=%s and mask010b=%s and mask100a=%s"
                        cursor.execute(sql, (symmetry[directions.index("001")], symmetry[directions.index("100")],
                                             symmetry[directions.index("010")], bravais,
                                             mask001_a, mask001_b, mask010_a, mask010_b, mask100_a))

                space_group_id = cursor.fetchall()
        else:
            raise ValueError("Offered directions are not exactly characteristic directions.")
        break
    cursor.close()
    connect.close()
    print(space_group_id)
    return space_group_id
