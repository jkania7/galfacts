!/usr/env/python

import numpy as np
import sys
import os
import struct

f=open('/n/fox/processed/N1_CALS/band0/S0206+330/54704/beam0/fluxtime.dat','rb')
data = []

struct_fmt = "<f" # 4 byte float
struct_len = struct.calcsize(struct_fmt)

f.seek(0,2)
size = f.tell() # Finding the size of the file
f.seek(0,0)

elem = size/4
iter = elem/7

print 'The size of the file is',size
print 'The number of iterations required are', iter
print 'The number of elements are',elem

a=4
for j in range(iter):
    f.seek(0,1)
      ra =(f.read(struct_len))
      if ra !="":
            RA = struct.unpack(struct_fmt,ra)
                data.append(RA)
                  dec=(f.read(struct_len))
                  if dec !="":
                        DEC =struct.unpack(struct_fmt,dec)
                            data.append(DEC)
                              ast=(f.read(struct_len))
                              if ast !="":
                                    AST =struct.unpack(struct_fmt,ast)
                                        data.append(AST)
                                          i=(f.read(struct_len))
                                          if i !="":
                                                I=struct.unpack(struct_fmt,i)
                                                    data.append(I)
                                                      q=(f.read(struct_len))
                                                      if q !="":
                                                            Q =struct.unpack(struct_fmt,q)
                                                                data.append(Q)
                                                                  u=(f.read(struct_len))
                                                                  if u !="":
                                                                        U=struct.unpack(struct_fmt,u)
                                                                            data.append(U)
       v=(f.read(struct_len))
   if v !="":
         V =struct.unpack(struct_fmt,v)
         data.append(V)

print 'Done!'

f.close()


                                                                                        