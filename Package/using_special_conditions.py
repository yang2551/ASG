# coding = UTF-8

from tkinter import messagebox
from Package import analyse_general_position
from Package import analyse_wyckoff_position
from Package import match_plane_group


def determine_using_other_conditions(space_group_id, directions):
    # :param space_group_id: 未使用特殊条件所得空间群种类
    # :param directions: 所有特征方向
    # :return: 空间群id
    origin_at = match_plane_group.get_origin_at()
    general_position = analyse_general_position.get_general_position()
    wyckoff_position = analyse_wyckoff_position.get_wyckoff_position()
    temp_ids = []
    if len(space_group_id) != 1:
        messagebox.showinfo(title="Info", message="Space Group is Not Unique")
        for i in range(len(space_group_id)):
            temp_ids.append(space_group_id[i][0])
        if 16 and 47 in temp_ids:
            if general_position == 4:
                space_group_id = 16
            if general_position == 8:
                space_group_id = 47
        if 21 and 65 in temp_ids:
            if general_position == 8:
                space_group_id = 21
            if general_position == 16:
                space_group_id = 65
        if 22 and 69 in temp_ids:
            if general_position == 16:
                space_group_id = 22
            if general_position == 32:
                space_group_id = 69
        if 23 and 24 and 71 in temp_ids:
            if ["1/4,0,z"] in origin_at or ["x,1/4,0"] in origin_at or ["0,y,1/4"] in origin_at:
                space_group_id = 24
            else:
                if general_position == 8:
                    space_group_id = 23
                if general_position == 16:
                    space_group_id = 71
        if 75 and 77 and 81 in temp_ids:
            if ["-y,x,z"] or ["y,x,z"] in wyckoff_position:
                space_group_id = 75
            if ["-y,x,z+1/2"] or ["y,x,z+1/2"] in wyckoff_position:
                space_group_id = 77
            if ["y,x,-z"] or ["-y,x,-z"] in wyckoff_position:
                space_group_id = 81
        if 76 and 78 in temp_ids:
            messagebox.showinfo("Info", "Space group 76 and 78 cannot be distinguished.")
        if 79 and 80 and 82 in temp_ids:
            if ["1/4,1/4,z"] in origin_at:
                space_group_id = 80
            else:
                messagebox.showinfo("Info", "Space group 79 and 82 cannot be distinguished.")
        if 83 and 84 in temp_ids:
            if "100" or "001" in directions:
                if ["-y,x,z+1/2"] or ["y,-x,z+1/2"] or ["y,-x,-z+1/2"] or ["-y,x,-z+1/2"] in wyckoff_position:
                    space_group_id = 84
                else:
                    space_group_id = 83
            else:
                messagebox.showinfo("Info", "Wyckoff position of [100] or [001] is needed.")
        if 85 and 86 in temp_ids:
            if ["x,1/4,0"] or ["x,x,0"] in origin_at:
                space_group_id = 85
            else:
                space_group_id = 86
        if 89 and 93 and 123 in temp_ids:
            if ["x,x,1/4"] in origin_at:
                space_group_id = 93
            else:
                if general_position == 8:
                    space_group_id = 89
                if general_position == 16:
                    space_group_id = 123
        if 90 and 94 in temp_ids:
            if ["x,1/4,0"] in origin_at:
                space_group_id = 90
            else:
                space_group_id = 94
        if 91 and 95 in temp_ids:
            if ["x,x,3/8"] in origin_at:
                space_group_id = 91
            else:
                space_group_id = 95
        if 92 and 96 in temp_ids:
            if ["x,1/4,3/8"] in origin_at:
                space_group_id = 92
            else:
                space_group_id = 96
        if 97 and 98 and 139 in temp_ids:
            if ["1/4,1/4,z"] or ["x,0,3/8"] in origin_at:
                space_group_id = 98
            else:
                if general_position == 16:
                    space_group_id = 97
                if general_position == 32:
                    space_group_id = 139
        if 143 and 144 and 145 in temp_ids:
            if general_position == 3:
                space_group_id = 143
            else:
                messagebox.showinfo("Info", "Space group 144 and 145 cannot be distinguished.")
        if 149 and 151 and 153 in temp_ids:
            if ["x,0,0"] in origin_at:
                space_group_id = 149
            if ["x,0,1/6"] in origin_at:
                space_group_id = 151
            if ["x,0,1/3"] in origin_at:
                space_group_id = 153
        if 150 and 152 and 154 in temp_ids:
            if ["x,0,1/3"] or ["x,1/2x,1/6"] in origin_at:
                space_group_id = 152
            elif ["x,0,1/6"] or ["x,1/2x,1/3"] in origin_at:
                space_group_id = 154
            else:
                space_group_id = 150
        if 168 and 171 and 172 in temp_ids:
            if "010" in directions:
                if ["-y,x-y,z+2/3"] and ["-x+y,-x,z+1/3"] \
                        and ["y,x+y,z+2/3"] and ["x-y,x,z+1/3"] not in wyckoff_position:
                    space_group_id = 168
                else:
                    messagebox.showinfo("Info", "Space group 171 and 172 cannot be distinguished.")
            else:
                messagebox.showinfo("Info", "Wyckoff position of [010] is needed.")
        if 169 and 170 and 173 in temp_ids:
            if "010" or "100" in directions:
                if ["-x+y,-x,z+2/3"] and ["y,-x+y,z+5/6"] \
                        and ["-y,x-y,z+1/3"] and ["x-y,x,z+1/6"] not in wyckoff_position:
                    space_group_id = 173
                else:
                    messagebox.showinfo("Info", "Space group 169 and 170 cannot be distinguished.")
            else:
                messagebox.showinfo("Info", "Wyckoff position of [010] or [100] is needed.")
        if 177 and 180 and 181 and 191 in temp_ids:
            if ["x,1/2x,0"] in origin_at:
                space_group_id = 177
            elif ["x,1/2x,1/6"] in origin_at:
                space_group_id = 180
            elif ["x,1/2x,1/3"] in origin_at:
                space_group_id = 181
            else:
                space_group_id = 191
        if 178 and 179 and 182 in temp_ids:
            if ["x,1/2x,1/12"] in origin_at:
                space_group_id = 178
            if ["x,1/2x,5/12"] in origin_at:
                space_group_id = 179
            if ["x,1/2x,1/4"] in origin_at:
                space_group_id = 182
        if 197 and 199 in temp_ids:
            if ["0,0,z"] or ["x,x,0"] in origin_at:
                space_group_id = 197
            else:
                space_group_id = 199
        if 207 and 208 in temp_ids:
            if ["0,0,z"] or ["x,x,0"] in origin_at:
                space_group_id = 207
            else:
                space_group_id = 208
        if 209 and 210 in temp_ids:
            if ["0,0,z"] or ["x,x,0"] in origin_at:
                space_group_id = 209
            else:
                space_group_id = 210
        if 211 and 214 in temp_ids:
            if ["0,0,z"] or ["x,x,0"] in origin_at:
                space_group_id = 211
            else:
                space_group_id = 214
        if 212 and 213 in temp_ids:
            if ["1/4,0,z"] in origin_at:
                space_group_id = 213
            else:
                space_group_id = 212
    return space_group_id
