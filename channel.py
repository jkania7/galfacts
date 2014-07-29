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
        self.options = options #to get options in lower functions
        self.chan_num = chan_num
        if self.options["format"] == "ascii":
           #Added band0/run1/ to fit calgary's file structure
           #self.chan_file = "{0}/{1}/{2}/run1/{3}/beam{4}/fluxtime{5:04d}.dat".\
           self.chan_file = "{0}/{1}/{2}/{3}/beam{4}/fluxtime{5:04d}.dat".\
             format(options["data_filepath"],
                    options["band"],
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
                   print "Log: fluxtime{0:04d}.dat not found".\
                         format(chan_num)
        else:
            self.cfg_file = "{0}/{1}/{2}/{3}/beam{4}/fluxtime.dat_cfg".\
                       format(options["data_filepath"],
                              options["band"],
                              options["field"],
                              options["date"],
                              beam_num)
            
            self.chan_file = "{0}/{1}/{2}/{3}/beam{4}/fluxtime.dat".\
                             format(options["data_filepath"],
                                    options["band"],
                                    options["field"],
                                    options["date"],
                                    beam_num)
            try:
                ra,dec,ast,I,Q,U,V = self.bin_read(self.cfg_read(self.cfg_file), chan_num)
                self.num_points = len(ra)
                self.error = False
            except TypeError:
                self.error = True
                if options["verbose"] == True:
                    print "log: fluxtime{0:04d}.dat not in binary".\
                          format(chan_num)

          
    def average(self):
        """Return the average Stokes for this channel"""
        if self.options["format"] == "ascii":
            ra,dec,ast,I,Q,U,V = np.loadtxt(self.chan_file,unpack=True)
        else:
            ra,dec,ast,I,Q,U,V = self.bin_read(self.cfg_read(self.cfg_file), self.chan_num)
        self.num_points = len(ra)
        return (np.nanmean(I), np.nanmean(Q), np.nanmean(U), np.nanmean(V))

    def add_points(self, Iarr, Qarr, Uarr, Varr):
        """Add these channel's points to the running I, Q, U, V total
           for each timestamp"""
        if self.options["format"] == "ascii":
            ra,dec,ast,I,Q,U,V = np.loadtxt(self.chan_file,unpack=True)
        else:
            ra,dec,ast,I,Q,U,V = self.bin_read(self.cfg_read(self.cfg_file), self.chan_num)
        return (Iarr + I, Qarr + Q, Uarr + U, Varr + V)

    def get_coordinates(self):
        """Get the AST, RA, and DEC for this channel"""
        if self.options["format"] == "ascii":
            ra,dec,ast,I,Q,U,V = np.loadtxt(self.chan_file,unpack=True)
        else:
            ra,dec,ast,I,Q,U,V = self.bin_read(self.cfg_read(self.cfg_file), self.chan_num)     
        return ra, dec, ast

    def bin_read(self, cfg, chan_num):
        if chan_num in cfg:
            #self.error = False #all channels must have self.error
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
            ra = list(ra) #unpack returns imputable tuples, we want lists
            dec = list(dec)
            ast = list(ast)
            I = list(I)
            Q = list(Q)
            U = list(U)
            V = list(V)
            """
            if chan_num%100 == 0:
                with  open("../results_ascii/chan{0}.txt".format(chan_num),"w") as txt:
                    txt.write(";ra\tdec\tast\tI\tQ\tU\tV")
                    for i in xrange(len(I)):
                        txt.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n".format(ra[i], dec[i], ast[i], I[i], Q[i], U[i], V[i]))
            """
            return (ra, dec, ast, I, Q, U, V)

    def cfg_read(self, cfg_file):
        chan, loc, length = np.loadtxt(cfg_file,dtype = 'int',unpack=True)
        cfg = {my_chan:{"loc":my_loc, "num_rec":my_rec} for my_chan, my_loc, my_rec in zip(chan,loc,length)}
        return cfg
        
    
if __name__ == "__main__":
    sys.exit("Error: module not meant to be run at top level.")
