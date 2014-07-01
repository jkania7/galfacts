"""
channel.py
Channel object for GALFACTS transient search
02 June 2014 - Trey Wenger - creation
25 June 2014 - Modified by jkania to better handle missing fluxtimexxxx.dat files fit calgary's file stucture
28 June Modified by jkania to improve missing file handling

"""
import os
import sys
import numpy as np
import struct
from collections import defaultdict

class Channel(object):
    """Channel object for GALFACTS transient search"""
    def __init__(self, chan_num, beam_num, **options):
        """Initialize the channel object"""
        if options["format"] == "ascii":
           #Added band0/run1/ to fit calgary's file structure
           #self.chan_file = "{0}/{1}/band0/run1/{2}/beam{3}/fluxtime{4:04d}.dat".\
           self.chan_file = "{0}/{1}/{2}/beam{3}/fluxtime{4:04d}.dat".\
             format(options["data_filepath"],
                    options["field"],
                    options["date"],
                    beam_num,
                    chan_num)
           self.error = (not os.path.isfile(self.chan_file))
           try: #handles missing channels
               ra,dec,ast,I,Q,U,V = np.loadtxt(self.chan_file,unpack=True)
               self.num_points = len(ra)
           except IOError:
               if options["verbose"] == True:
                   print "Log: fluxtime{0}.dat not found".\
                         format(chan_num)
        else:
            cfg_file = "{0}/{1}/band0/{2}/beam{3}/fluxtime.dat_cfg".\
                       format(options["data_filepath"],
                              options["field"],
                              options["date"],
                              beam_num)
            
            self.chan_file = "{0}/{1}/band0/{2}/beam{3}/fluxtime.dat".\
                             format(options["data_filepath"],
                                    options["field"],
                                    options["date"],
                                    beam_num)
             
            chan, loc, length = np.loadtxt(cfg_file,dtype = 'int',unpack=True)
            cfg = defaultdict(list)
            for i in xrange(len(chan)):
                cfg[chan[i]].append(loc[i])
                cfg[chan[i]].append(length[i])
        
            if chan_num in cfg:
                f = open(self.chan_file,"rb")
                f.seek((cfg[chan_num])[0])
                binary = f.read((cfg[chan_num])[1])
                num = len(binary)/4 #floats are 4 bytes
                print len(binary)
                data = struct.unpack('{0}f'.format(num),binary)
                ra = data[0::7]
                dec = data[1::7]
                ast = data[2::7]
                I = data[3::7]
                Q = data[4::7]
                U = data[5::7]
                V = data[6::7]
            else:
                self.error = False
                print "Log: fluxtime{0}.dat not in binary file".\
                      format(chan_num)
          
    def average(self):
        """Return the average Stokes for this channel"""
        #if options["format"] == "ascii":
        ra,dec,ast,I,Q,U,V = np.loadtxt(self.chan_file,unpack=True)
        self.num_points = len(ra)
        """else:
            f = open(self.chan_file,"rb")
            f.seek(cfg(self.chan_num)[0])
            binary = f.read(cfg(self.chan_num)[1])
            data = struct.unpack('{0}f'.format(num),bin_data)
            ra = data[0::7]
            dec = data[1::7]
            ast = data[2::7]
            I = data[3::7]
            Q = data[4::7]
            U = data[5::7]
            V = data[6::7]"""
        return (np.mean(I), np.mean(Q), np.mean(U), np.mean(V))

    def add_points(self, Iarr, Qarr, Uarr, Varr):
        """Add these channel's points to the running I, Q, U, V total
           for each timestamp"""
        #if options["format"] == "ascii":
        ra,dec,ast,I,Q,U,V = np.loadtxt(self.chan_file,unpack=True)
        """else:
            f = open(self.chan_file,"rb")
            f.seek(cfg(self.chan_num)[0])
            binary = f.read(cfg(self.chan_num)[1])
            data = struct.unpack('{0}f'.format(num),bin_data)
            ra = data[0::7]
            dec = data[1::7]
            ast = data[2::7]
            I = data[3::7]
            Q = data[4::7]
            U = data[5::7]
            V = data[6::7]"""
        return (Iarr + I, Qarr + Q, Uarr + U, Varr + V)

    def get_coordinates(self):
        """Get the AST, RA, and DEC for this channel"""
        #if options["format"] == "ascii":
        ra,dec,ast,I,Q,U,V = np.loadtxt(self.chan_file,unpack=True)
        """else:
            f = open(self.chan_file,"rb")
            f.seek(cfg(self.chan_num)[0])
            binary = f.read(cfg(self.chan_num)[1])
            data = struct.unpack('{0}f'.format(num),bin_data)
            ra = data[0::7]
            dec = data[1::7]
            ast = data[2::7]
            I = data[3::7]
            Q = data[4::7]
            U = data[5::7]
            V = data[6::7]"""
        return ra, dec, ast

if __name__ == "__main__":
    sys.exit("Error: module not meant to be run at top level.")
