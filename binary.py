import struct

with open("fluxtime.dat","rb") as f:
    bin_data = f.read()

num_entries = len(bin_data)/4

data_unpak = struct.unpack('{0}f'.format(num),bin_data)

RA_set = data_unpack[0::7]
DEC_set = data_unpack[1::7]
AST_set = data_unpack[2::7]
I_set = data_unpack[3::7]
Q_set = data_unpack[4::7]
U_set = data_unpack[5::7]
V_set = data_unpack[6::7]

num_point = len(RA_set)/num_channels

