"""
beam.py
Beam object for GALFACTS transient search
02 June 2014 - Trey Wenger - creation
12 June 2014 - Trey Wenger - Fixed smoothing convolution norm. problem
25 June 2014 - Joseph Kania - handling binary inputs
10 July 2014 - Trey Wenger - adds check for nan's and interpolation
                             through missing data
                             plot bad sources too
                             print out list of rfi channels
"""
import sys
import os
import numpy as np
import channel
import make_plots as plt
import source
import random as rand
import math

class Beam(object):
    """Beam object for GALFACTS transient search"""
    def __init__(self, beam_num, **options):
        """Initialize the beam object"""
        self.beam_num = beam_num
        self.options = options
        self.channels = [channel.Channel(i, beam_num, **options) for
                         i in xrange(options["num_channels"])]
        self.elim_channels = []
        # put error in channel zero. This is the Calgary average
        self.channels[0].error = True
        self.elim_channels.append( (0, 'calgary_average') )
        # put error in  ignored channels
        if options["exclude_channels"] != None:
             for c in options["exclude_channels"]:
                self.channels[c].error = True
                self.elim_channels.append( (c, 'excluded') )
    def find_sources(self):
        """Algorithm to detect sources for this beam"""
        # generate results directory
        results_dir = "{0}/{1}/{2}/beam{3}".\
          format(self.options["results_filepath"],
                 self.options["field"],
                 self.options["date"],
                 self.beam_num)
        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)
        
        # Stokes averaged over time
        if self.options["verbose"]:
            print("Log: Averaging Stokes over time.")
        I_data = np.zeros(self.options["num_channels"])
        Q_data = np.zeros(self.options["num_channels"])
        U_data = np.zeros(self.options["num_channels"])
        V_data = np.zeros(self.options["num_channels"])
        for i in xrange(self.options["num_channels"]):
            if self.channels[i].error: continue
            I_data[i], Q_data[i], U_data[i], V_data[i] = \
              self.channels[i].average()
        if self.options["file_verbose"]:
            np.savez(results_dir+"/time_avg",
                     channel=range(self.options["num_channels"]),
                     I_data = I_data,
                     Q_data = Q_data,
                     U_data = U_data,
                     V_data = V_data)
            chans = range(0,self.options["num_channels"])
            plt.stokes_plot(chans, "Channel", I_data, Q_data, U_data,
                            V_data, results_dir+"/time_avg.png")
            
        # convolve time-avereraged data to detect RFI
        if self.options["verbose"]:
            print("Log: Performing RFI detection convolution.")
        con = np.zeros(2*self.options["rfi_con_width"] + 1)
        con[0] = -0.5
        con[self.options["rfi_con_width"]] = 1.0
        con[-1] = -0.5
        I_data = np.convolve(I_data,con,mode="same")
        Q_data = np.convolve(Q_data,con,mode="same")
        U_data = np.convolve(U_data,con,mode="same")
        V_data = np.convolve(V_data,con,mode="same")
        if self.options["file_verbose"]:
            np.savez(results_dir+"/rfi_conv_time_avg",
                     channel=range(self.options["num_channels"]),
                     I_data = I_data,
                     Q_data = Q_data,
                     U_data = U_data,
                     V_data = V_data)
            chans = range(0,self.options["num_channels"])
            plt.stokes_plot(chans, "Channel", I_data, Q_data, U_data,
                            V_data,
                            results_dir+"/rfi_conv_time_avg.png")

        # eliminated edge channels
        if self.options["verbose"]:
            print("Log: eliminating edge channels.")
        for i in xrange(self.options["edge_buff_chan"]):
            self.channels[i].error=True
            self.channels[-1-i].error=True
            self.elim_channels.append( (i,"channel_edge") )
            self.elim_channels.append( (self.options["num_channels"]-i,
                                        "channel_edge") )
        # determine the minimum mean and std dev in our intervals
        interval_width = self.options["num_channels"]/\
          self.options["num_intervals"]
        for stokes,data in [("I",I_data), ("Q",Q_data),
                            ("U",U_data), ("V",V_data)]:
            means = np.array([np.nanmean(data[i:i+interval_width])
                              for i in
                              range(0,self.options["num_channels"],
                                    interval_width)])
            stddevs = np.array([np.nanstd(data[i:i+interval_width])
                                for i in
                                range(0,self.options["num_channels"],
                                      interval_width)])
            min_ind = stddevs[stddevs.nonzero()].argmin()
            min_stddev = stddevs[min_ind]
            min_mean = means[min_ind]
            # determine bad channels and flag them
            bad_chans = np.where(np.abs(data) > min_mean +\
                                 self.options["rfi_mask"]*min_stddev)[0]
            if self.options["verbose"]:
                print("Log: eliminated {0} channels with RFI".\
                      format(len(bad_chans)))
            for c in bad_chans:
                self.channels[c].error = True
                self.elim_channels.append( (c, 'rfi_stokes_{0}'.format(stokes)) )

        # write eliminated channel list to a file
        if self.options["file_verbose"]:
            elim = {} #sorts, channel is only listed once
            for num,reason in self.elim_channels:
                elim[num] =  str(reason)
                
            with open(results_dir+"/parameters.txt","w") as f:
                for j in sorted(elim):
                    f.write("\n{0} ".format(j))
                    for k in elim[j]:
                       f.write ("{0}".format(k))
                f.write("\nParameters used to run the program\n")
                for j in self.options:
                    f.write("{0} = {1}\n".format(j, self.options[j]))
                

        # recompute Stokes averaged over time
        if self.options["verbose"]:
            print("Log: Recomputing average Stokes over time.")
        I_data = np.zeros(self.options["num_channels"])
        Q_data = np.zeros(self.options["num_channels"])
        U_data = np.zeros(self.options["num_channels"])
        V_data = np.zeros(self.options["num_channels"])
        for i in xrange(self.options["num_channels"]):
            if self.channels[i].error: continue
            I_data[i], Q_data[i], U_data[i], V_data[i] = \
              self.channels[i].average()
        if self.options["file_verbose"]:
            np.savez(results_dir+"/clean_time_avg",
                     channel=range(self.options["num_channels"]),
                     I_data = I_data,
                     Q_data = Q_data,
                     U_data = U_data,
                     V_data = V_data)
            chans = range(0,self.options["num_channels"])
            plt.stokes_plot(chans, "Channel", I_data, Q_data, U_data,
                            V_data,
                            results_dir+"/clean_time_avg.png")
            
        # now, detect sources in each bin as well as over the full
        # bandpass
        num_bins = int(self.options["band_width"]/
                       self.options["bin_width"])+1
        chans_per_bin = int(self.options["num_channels"]/num_bins)
        for b in range(num_bins+1):
            if b == num_bins:
                b = 999
                start_chan = 0
                end_chan = self.options["num_channels"]
            else:
                start_chan = b*chans_per_bin
                end_chan = (b+1)*chans_per_bin
                if end_chan > self.options["num_channels"]:
                    end_chan = self.options["num_channels"]
            # check if we're already outside edge buffer
            if (end_chan < self.options["edge_buff_chan"] or
                start_chan > (self.options["num_channels"] -
                              self.options["edge_buff_chan"])):
                continue
            if self.options["verbose"]:
                print("Log: Analyzing bin {0}".format(b))
            # results directory for this bin
            bin_results_dir = results_dir+"/bin{0:03d}".format(b)
            if not os.path.isdir(bin_results_dir):
                os.makedirs(bin_results_dir)
            # Average over channels
            if self.options["verbose"]:
                print("Log: Averaging Stokes over channels in this bin")
            first_good = 0
            for first_good in xrange(self.options["num_channels"]):  #makes sure the channel exisits before accessing
                if not self.channels[first_good].error:
                    break
                if first_good == self.options["num_channels"]-1:
                    print("Error: no channels")

            I_data = np.zeros(self.channels[first_good].num_points)
            Q_data = np.zeros(self.channels[first_good].num_points)
            U_data = np.zeros(self.channels[first_good].num_points)
            V_data = np.zeros(self.channels[first_good].num_points)
            num_good_points = 0.
            for c in xrange(start_chan,end_chan):
                if self.channels[c].error: continue
                I_data, Q_data, U_data, V_data = \
                  self.channels[c].add_points(I_data,Q_data,U_data,
                                              V_data)
                num_good_points += 1.
            if num_good_points == 0.: continue
            I_data /= num_good_points
            Q_data /= num_good_points
            U_data /= num_good_points
            V_data /= num_good_points
            if self.options["verbose"]:
                print("Log: Interpolating through missing data")
            # find and correct missing data
            # loop over all points
            i=0
            nan_start_stop = dict() #a dictionary to hold the start and stops of the nans
            while i < len(I_data):
                # if we find a nan, let's record it and figure out
                # how many nans there are, then linearly interpolate
                # through those missing data
                if I_data[i] < 0.: print(I_data[i])
                if math.isnan(I_data[i]):
                    j = i
                    while j < len(I_data):
                        # now we've found some data that is not
                        # a nan, loop though until we find another
                        # good number, then linearly interpolate
                        # over nans
                        if not math.isnan(I_data[j]):
                            nan_start_stop[i] = j #adds starts and stops to dictionary
                            # this takes in to consideration that
                            # the first nan could be the first data
                            # point. If so, just use a flat line
                            # between the beginning and the first
                            # non-nan
                            if i == 0:
                                first = j
                            else:
                                first = i-1
                            # calculate slope over linear interp.
                            I_slope = (I_data[j]-I_data[first])/\
                              (j - (i-1))
                            Q_slope = (Q_data[j]-Q_data[first])/\
                              (j - (i-1))
                            U_slope = (U_data[j]-U_data[first])/\
                              (j - (i-1))
                            V_slope = (V_data[j]-V_data[first])/\
                              (j - (i-1))
                            # apply linear interp.
                            for k in range(i,j):
                                I_data[k] = I_data[first] + I_slope*(k-i+1)
                                Q_data[k] = Q_data[first] + Q_slope*(k-i+1)
                                U_data[k] = U_data[first] + U_slope*(k-i+1)
                                V_data[k] = V_data[first] + V_slope*(k-i+1)
                            i = j-1 # start i from j now
                            break # break out and keep looking
                        j += 1
                    if j == len(I_data)-1:
                        # if we get here, we didn't find any non-nans
                        # before the end of the run
                        # so let's just use a flat line
                        I_data[i:] = I_data[i-1]
                        Q_data[i:] = Q_data[i-1]
                        U_data[i:] = U_data[i-1]
                        V_data[i:] = V_data[i-1]
                        nan_start_stop[i] = len(I_data)-1 #-1 b/c index is one less than the length
                        break # all done!
                
                i += 1
                
            if self.options["verbose"]:
                print("Log: Correcting coordinates.")
            RA, DEC, AST = get_coordinates(self.beam_num,
                                           **self.options)
            if self.options["file_verbose"]:
                np.savez(bin_results_dir+"/chan_avg",
                         chan_range=[start_chan,end_chan],
                         RA = RA,
                         DEC = DEC,
                         AST = AST,
                         I_data = I_data,
                         Q_data = Q_data,
                         U_data = U_data,
                         V_data = V_data)
                plt.stokes_plot(AST, "AST", I_data, Q_data, U_data,
                                V_data,
                                bin_results_dir+"/chan_avg.png")

            # smooth data
            if self.options["verbose"]:
                print("Log: Performing smoothing convolution.")
            angle = np.arange(2*self.options["smooth_con_width"]+1)
            angle = angle*10.*np.pi/(2.*self.options["smooth_con_width"])
            angle = angle - 5.*np.pi
            con = np.sin(angle)/angle
            con[self.options["smooth_con_width"]] = 1.
            I_data = np.convolve(I_data,con,mode="same")/np.sum(con)
            Q_data = np.convolve(Q_data,con,mode="same")/np.sum(con)
            U_data = np.convolve(U_data,con,mode="same")/np.sum(con)
            V_data = np.convolve(V_data,con,mode="same")/np.sum(con)
            # chop off edges after convolution
            if self.options["verbose"]:
                print("Log: Chopping off edges after convolution")
            RA = RA[self.options["edge_buff_time"]:
                    -self.options["edge_buff_time"]]
            DEC = DEC[self.options["edge_buff_time"]:
                      -self.options["edge_buff_time"]]
            AST = AST[self.options["edge_buff_time"]:
                      -self.options["edge_buff_time"]]
            I_data = I_data[self.options["edge_buff_time"]:
                            -self.options["edge_buff_time"]]
            Q_data = Q_data[self.options["edge_buff_time"]:
                            -self.options["edge_buff_time"]]
            U_data = U_data[self.options["edge_buff_time"]:
                            -self.options["edge_buff_time"]]
            V_data = V_data[self.options["edge_buff_time"]:
                            -self.options["edge_buff_time"]]
            if self.options["file_verbose"]:
                np.savez(bin_results_dir+"/smooth_chan_avg",
                         chan_range=[start_chan,end_chan],
                         RA = RA,
                         DEC = DEC,
                         AST = AST,
                         I_data = I_data,
                         Q_data = Q_data,
                         U_data = U_data,
                         V_data = V_data)
                plt.stokes_plot(AST, "AST", I_data, Q_data, U_data,
                                V_data,
                                bin_results_dir+"/smooth_chan_avg.png")
            
            # convolve for source detection
            if self.options["verbose"]:
                print("Log: Performing source detection convolution.")
            con = np.zeros(2*self.options["source_con_width"]+1)
            con[0] = -0.25
            con[self.options["source_con_width"]/2] = -0.25
            con[self.options["source_con_width"]] = 1.0
            con[3*self.options["source_con_width"]/2] = -0.25
            con[-1] = -0.25
            I_data_source = np.convolve(I_data,con,mode="same")
            if self.options["file_verbose"]:
                np.savez(bin_results_dir+"/source_chan_avg",
                         chan_range=[start_chan,end_chan],
                         RA = RA,
                         DEC = DEC,
                         AST = AST,
                         I_data = I_data_source)
                plt.single_stokes(AST, "AST", I_data_source,
                                  "Stokes I (K)",
                                  bin_results_dir+
                                  "/source_chan_avg.png")
            if self.options["verbose"]:
                print("Log: Locating sources.")
            #a good place to but in the test to see if we are close to dec change?
            #source_points_all is the array of indeces where a source is "found"
            source_points = np.where(I_data_source >
                                     self.options["source_mask"]*
                                     self.options["sigma"])[0]
            # storage for sources
            sources = []
            # i is the starting point for this source
            i=0
            while i < len(source_points):
                # j is the ending point for this source
                j = i+1
                # as long as [j] = [j-1] + 1, still on same source
                while (j < len(source_points) and
                       source_points[j] == source_points[j-1] + 1):
                    j += 1
                # get the necessary data for this source
                # first find max
                this_I_data = I_data_source[source_points[i]:
                                            source_points[j-1]]
                if len(this_I_data) == 0:
                    i = j
                    continue
                # max point in I_data_source array for this source
                max_point = this_I_data.argmax() + source_points[i]
                # now, get coords and data for fitting
                time_end = False
                base1_start = (max_point-
                               self.options["num_source_points"]-
                               self.options["point_sep"]-
                               self.options["num_outer_points"])
                if base1_start < 0: base1_start = 0
                base1_end = base1_start+self.options["num_outer_points"]
                if base1_end < 0: base1_end = 0
                source_start = max_point-self.options["num_source_points"]
                if source_start < 0: source_start = 0
                source_end = max_point+self.options["num_source_points"]+1
                if source_end > len(AST): source_end = len(AST)
                base2_start = (max_point+1+
                               self.options["num_source_points"]+
                               self.options["point_sep"])
                if base2_start > len(AST): base2_start = len(AST)
                base2_end = base2_start+self.options["num_outer_points"]
                if base2_end > len(AST): base2_end = len(AST)
                # source is near end of observation
                if base1_start < 0 or base2_end >= len(AST):
                    time_end = True
                this_RA = RA[base1_start:base1_end]
                this_RA = np.append(this_RA,RA[source_start:source_end])
                this_RA = np.append(this_RA,RA[base2_start:base2_end])
                this_DEC = DEC[base1_start:base1_end]
                this_DEC = np.append(this_DEC,DEC[source_start:source_end])
                this_DEC = np.append(this_DEC,DEC[base2_start:base2_end])
                this_AST = AST[base1_start:base1_end]
                this_AST = np.append(this_AST,AST[source_start:source_end])
                this_AST = np.append(this_AST,AST[base2_start:base2_end])
                this_I_data = I_data[base1_start:base1_end]
                this_I_data = np.append(this_I_data,I_data[source_start:source_end])
                this_I_data = np.append(this_I_data,I_data[base2_start:base2_end])
                this_Q_data = Q_data[base1_start:base1_end]
                this_Q_data = np.append(this_Q_data,Q_data[source_start:source_end])
                this_Q_data = np.append(this_Q_data,Q_data[base2_start:base2_end])
                this_U_data = U_data[base1_start:base1_end]
                this_U_data = np.append(this_U_data,U_data[source_start:source_end])
                this_U_data = np.append(this_U_data,U_data[base2_start:base2_end])
                this_V_data = V_data[base1_start:base1_end]
                this_V_data = np.append(this_V_data,V_data[source_start:source_end])
                this_V_data = np.append(this_V_data,V_data[base2_start:base2_end])
                all_RA = RA[base1_start:base2_end]
                all_DEC = DEC[base1_start:base2_end]
                all_AST = AST[base1_start:base2_end]
                all_I_data = I_data[base1_start:base2_end]
                all_Q_data = Q_data[base1_start:base2_end]
                all_U_data = U_data[base1_start:base2_end]
                all_V_data = V_data[base1_start:base2_end]
                #
                # Check if we change directions during this source
                dec_end = False
                ra_end = False
                # Estimated distance between each dec point
                dec_size = (np.max(all_DEC)-np.min(all_DEC))/(np.argmax(all_DEC)-np.argmin(all_DEC))
                # Estimated distance between each ra point
                ra_size = (np.max(all_RA)-np.min(all_RA))/(np.argmax(all_RA)-np.argmin(all_RA))
                # we don't want to be within this many points of a change
                point_req = self.options["num_source_points"]+self.options["point_sep"]+self.options["num_outer_points"]
                # we don't want to be within this many degrees of a change
                dec_req = dec_size * point_req
                ra_req = ra_size * point_req
                if (all_DEC < (self.options["min_DEC"]+dec_req)).any() or (all_DEC > (self.options["max_DEC"]-dec_req)).any():
                    dec_end = True
                if (all_RA < (self.options["min_RA"]+ra_req)).any() or (all_RA > (self.options["max_RA"]-ra_req)).any():
                    ra_end = True
                #
                # now, add it
                sources.append(source.Source(this_RA, this_DEC, this_AST,
                                             this_I_data, this_Q_data,
                                             this_U_data, this_V_data,
                                             all_RA, all_DEC, all_AST,
                                             all_I_data, all_Q_data,
                                             all_U_data, all_V_data,
                                             time_end, dec_end, ra_end))
                # start next search from where this one left off
                i = j
            if self.options["verbose"]:
                print("Log: Found {0} sources.".format(len(sources)))
                print("Log: Fitting good sources.")
            good_sources = []
            bad_sources = []
            for s in range(len(sources)):
                # fit and plot
                plt_filename = bin_results_dir+"/source{0:03d}".format(s)
                sources[s].fit(plt_filename,**self.options)
                if (sources[s].time_end or sources[s].dec_end or
                    not sources[s].good_fit or sources[s].ra_end):
                    bad_sources.append(s)
                else:
                    good_sources.append(s)
            if self.options["verbose"]:
                print("Log: Fit {0} good sources.".format(len(good_sources)))
                print("Log: Fit {0} bad sources.".format(len(bad_sources)))
            if self.options["file_verbose"]:
                with open(bin_results_dir+"/good_sources.txt","w") as f:
                    f.write("# SourceNum\tcenterRA\tcenterDEC\tpeakI\t\twidthDEC\n")
                    f.write("# ---------\tdeg\t\tdeg\t\tK\t\tdeg\n")
                    for s in good_sources: #jwk -  added tab delimiters 
                        f.write("{0:03d}\t\t{1:.3f}\t\t{2:.3f}\t\t{3:.3f}\t\t{4:.3f}\n".\
                                format(s,sources[s].center_RA,
                                       sources[s].center_DEC,
                                       sources[s].center_I,
                                       sources[s].fit_p[2]))
                with open(bin_results_dir+"/bad_sources.txt","w") as f:
                    f.write("SourceNum\tcenterRA\tcenterDEC\tReasons\n")
                    f.write("#--------\tdeg\t\tdeg\t\t-------\n")
                    for s in bad_sources:
                        if sources[s].dec_end:
                            sources[s].bad_reasons+="dec_change,"
                        if sources[s].ra_end:
                            sources[s].bad_reasons+="ra_change"
                        if sources[s].time_end:
                            sources[s].bad_reasons+="end_of_obs,"
                        f.write("{0:03d}\t\t{1:.3f}\t\t{2:.3f}\t\t{3}\n".\
                                format(s,sources[s].center_RA,
                                       sources[s].center_DEC,
                                       sources[s].bad_reasons))
            np.savez(bin_results_dir+"/sources",
                     sources=sources)
            
def get_coordinates(beam_num, **options):
    """Return the AST, RA, and DEC for the specified beam after
       performing the necessary corrections"""
    # just use some random channel number, but make it different
    # for each beam in case we multithread this - we probably don't
    # want to open the same file in two places at once
    while True:
        num = rand.randint(1,options["num_channels"])
        temp_chan = channel.Channel(num, 0, ** options)
        if temp_chan.error == False:
            break
    # first, get the RA and AST from beam 0 then apply corrections

    RA, skipDEC, AST = temp_chan.get_coordinates()  
    # correct RA and AST for AST offset
    for i in xrange(len(AST)-1):
        AST[i] = AST[i] + (AST[i+1] - AST[i])*options["ast_offset"]
        RA[i] = RA[i] + (RA[i+1] - RA[i])*options["ast_offset"]
    # now get the DEC for this beam
    temp_chan = channel.Channel(num, beam_num, **options)
    skipRA, DEC, skipAST = temp_chan.get_coordinates()
    # correct DEC for AST offset
    for i in xrange(len(DEC)-1):
        DEC[i] = DEC[i] + (DEC[i+1] - DEC[i])*options["ast_offset"]
    # correct RA for RA correction
    RA = RA + options["ra_corr"][beam_num]/(60. * np.cos(np.deg2rad(DEC)))
    return RA, DEC, AST
    
if __name__ == "__main__":
    sys.exit("Error: module not meant to be run at top level.")
