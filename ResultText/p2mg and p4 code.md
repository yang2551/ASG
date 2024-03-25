# calculation of p4, do not delete!!!
import numpy

c51 = [151.02039984, 241.39086087]
c60 = [86.83271984, 226.91574642]
a75 = [268.89642417, 123.4406083]
a78 = [204.73513735, 108.88109881]
b25 = [268.84818482, 359.33787129]
b28 = [204.78364008, 344.91820041]
c_point = numpy.array([(c51[0] + c60[0]) / 2, (c51[1] + c60[1]) / 2])
f_point = numpy.array([(a75[0] + a78[0]) / 2, (a75[1] + a78[1]) / 2])
s_point = numpy.array([(b25[0] + b28[0]) / 2, (b25[1] + b28[1]) / 2])
length_fc_x = abs(f_point[0] - c_point[0])
length_fc_y = abs(f_point[1] - c_point[1])
length_sc_x = abs(s_point[0] - c_point[0])
length_sc_y = abs(s_point[1] - c_point[1])
print(length_fc_x, length_fc_y, length_sc_x, length_sc_y)
para_a = numpy.sqrt(numpy.square(length_fc_x) + numpy.square(length_fc_y))
para_b = numpy.sqrt(numpy.square(length_sc_x) + numpy.square(length_sc_y))
degrees = numpy.degrees(numpy.arccos(
	numpy.dot(f_point - c_point, s_point - c_point) / (para_a * para_b)))

# calculation of p2mg, do not delete!!!
import numpy

c47 = [259.97402597, 303.05844156]
c60 = [259.98795181, 262.439759042]
a72 = [259.96480331, 221.68115942]
a82 = [260., 181.]
b46 = [389.41573034, 303.0505618 ]
b58 = [389.5, 262.5]
d70 = [389.476979741, 221.71639042]
d81 = [389.57741348, 180.95810565]
c_point = numpy.array([(c47[0] + c60[0]) / 2, (c47[1] + c60[1]) / 2])
f_point = numpy.array([(a72[0] + a82[0]) / 2, (a72[1] + a82[1]) / 2])
s_point = numpy.array([(b46[0] + b58[0]) / 2, (b46[1] + b58[1]) / 2])
t_point = numpy.array([(d70[0] + d81[0]) / 2, (d70[1] + d81[1]) / 2])
length_fc_x = abs(f_point[0] - c_point[0])
length_fc_y = abs(f_point[1] - c_point[1])
length_sc_x = abs(s_point[0] - c_point[0])
length_sc_y = abs(s_point[1] - c_point[1])
print(length_fc_x, length_fc_y, length_sc_x, length_sc_y)
para_a = numpy.sqrt(numpy.square(length_fc_x) + numpy.square(length_fc_y))
para_b = numpy.sqrt(numpy.square(length_sc_x) + numpy.square(length_sc_y))
degrees = numpy.degrees(numpy.arccos(
	numpy.dot(f_point - c_point, s_point - c_point) / (para_a * para_b)))

# calculation of experimental p2mm, do not delete!!!
import numpy

c47 = [259.97402597, 303.05844156]
c60 = [259.98795181, 262.439759042]
a72 = [259.96480331, 221.68115942]
a82 = [260., 181.]
b46 = [389.41573034, 303.0505618 ]
b58 = [389.5, 262.5]
d70 = [389.476979741, 221.71639042]
d81 = [389.57741348, 180.95810565]
c_point = numpy.array([(c47[0] + c60[0]) / 2, (c47[1] + c60[1]) / 2])
f_point = numpy.array([(a72[0] + a82[0]) / 2, (a72[1] + a82[1]) / 2])
s_point = numpy.array([(b46[0] + b58[0]) / 2, (b46[1] + b58[1]) / 2])
t_point = numpy.array([(d70[0] + d81[0]) / 2, (d70[1] + d81[1]) / 2])
length_fc_x = abs(f_point[0] - c_point[0])
length_fc_y = abs(f_point[1] - c_point[1])
length_sc_x = abs(s_point[0] - c_point[0])
length_sc_y = abs(s_point[1] - c_point[1])
print(length_fc_x, length_fc_y, length_sc_x, length_sc_y)
para_a = numpy.sqrt(numpy.square(length_fc_x) + numpy.square(length_fc_y))
para_b = numpy.sqrt(numpy.square(length_sc_x) + numpy.square(length_sc_y))
degrees = numpy.degrees(numpy.arccos(
	numpy.dot(f_point - c_point, s_point - c_point) / (para_a * para_b)))