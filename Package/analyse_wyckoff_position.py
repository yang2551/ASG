# coding = UTF-8

from Package import real_space_parameters, match_plane_group

"""
tetragonal: [75,77,81] [83,84]
trigonal: [143,144,145]
hexagonal: [168,171,172] [169,170,173]
"""

wyckoff_position = []  # 单个保存，如 ["-y,x,z"]
lattice = real_space_parameters.get_real_space_parameter()[0]
bravais = real_space_parameters.get_real_space_parameter()[4]
if bravais is None:
    bravais = match_plane_group.get_match_plane_group_result()[4]


def get_wyckoff_position():
    return wyckoff_position


# unfinished
def calculate_wyckoff_position():
    global wyckoff_position
    if lattice == "tetragonal":
        pass
    if lattice == "trigonal":
        pass
    if lattice == "hexagonal":
        pass
    return wyckoff_position
