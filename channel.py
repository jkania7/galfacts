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
           #self.chan_file = "{0}/{1}/{2}/beam{3}/fluxtime{4:04d}.dat".\
           self.chan_file = "{0}/{1}/band0/run1/{2}/beam{3}/fluxtime{4:04d}.dat".\
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
        cfg = self.cfg_read(cfg_file)
        ra,dec,ast,I,Q,U,V = self.bin_read(cfg, chan_num)

          
    def average(self):
        """Return the average Stokes for this channel"""
        if self.options["format"] == "ascii":
            ra,dec,ast,I,Q,U,V = np.loadtxt(self.chan_file,unpack=True)
        self.num_points = len(ra)
        """else: """
        return (np.mean(I), np.mean(Q), np.mean(U), np.mean(V))

    def add_points(self, Iarr, Qarr, Uarr, Varr):
        """Add these channel's points to the running I, Q, U, V total
           for each timestamp"""
        #if options["format"] == "ascii":
        ra,dec,ast,I,Q,U,V = np.loadtxt(self.chan_file,unpack=True)
        """else:    """
        return (Iarr + I, Qarr + Q, Uarr + U, Varr + V)

    def get_coordinates(self):
        """Get the AST, RA, and DEC for this channel"""
        #if options["format"] == "ascii":
        ra,dec,ast,I,Q,U,V = np.loadtxt(self.chan_file,unpack=True)
        """else:"""
        return ra, dec, ast

    def bin_read(self, cfg, chan_num):
        if chan_num in cfg:
            f = open(self.chan_file,"rb")
            f.seek((cfg[chan_num])["loc"]*7*4) #seek point * amount of data * size of floats
            binary = f.read((cfg[chan_num])["num_rec"]*7*4) #number records* 7 data points * size of float
            num = len(binary)/4 #floats are 4 bytes
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
            print "Log: fluxtime{0:04d}.dat not in binary file".\
                  format(chan_num)
            ra = 0
            dec = 0
            ast = 0
            I = 0
            Q = 0
            U = 0
            V = 0 
            
        return (ra, dec, ast, I, Q, U, V)       


    def cfg_read(self, cfg_file):
        chan, loc, length = np.loadtxt(cfg_file,dtype = 'int',unpack=True)
        cfg = {my_chan:{"loc":my_loc, "num_rec":my_rec} for my_chan, my_loc, my_rec in zip(chan,loc,length)}
        return cfg

        
    
if __name__ == "__main__":
    sys.exit("Error: module not meant to be run at top level.")
