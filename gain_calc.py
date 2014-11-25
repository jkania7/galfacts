"""
gain_calc.py
Take calibration source clusters and use spectral fits to convert
from stokes I to flux density Jy. This will then be used in the
gain vs. dec calibration calculations.
23 Nov  2014 - Trey Wenger - Creation
"""
vers = "v1.0"

import sys
import os
import argparse
import numpy as np
import source
import cluster

def calc_sep(ra1,dec1,ra2,dec2,degs=False):
    """
    Calculate angular separation between two points on celestial
    sphere.
    Give degs=True if units are in degrees and returns in deg
    """
    if degs:
        ra1,ra2,dec1,dec2=np.deg2rad([ra1,ra2,dec1,dec2])
        
    sep = np.cos(np.pi/2.-dec1)*np.cos(np.pi/2.-dec2)
    sep += np.sin(np.pi/2.-dec1)*np.sin(np.pi/2.-dec2)*np.cos(ra1-ra2)
    sep = np.arccos(sep)
    if degs:
        sep = np.rad2deg(sep)
    return sep

def convert_sexid(sexid,dec=False):
    """
    Convert sexidecimal number to degrees
    if dec=False (RA), assume sexid is hhmmss.ss
    if dec=True (DEC), assume sexid is ddmmss.ss
    """
    modsexid = np.abs(sexid)
    degrees = int(np.floor(modsexid/10000.))
    modsexid -= degrees*10000.
    mins = int(np.floor(modsexid/100.))
    degrees += mins/60.
    modsexid -= mins*100.
    degrees += modsexid/3600.
    # check if RA
    if not dec: degrees = 15.*degrees # RA 15 degs per hour
    # check if negative
    if sexid < 0:
        degrees = -1.*degrees
    return degrees

def main(**options):
    print("gain_calc.py {0}".format(vers))
    # Read in spectral fits and nvss fits
    spectral_fits = np.genfromtxt(options['spectral_fits_file'],
                                  names=True,delimiter=',',
                                  dtype=None,autostrip=True)
    nvss_fits = np.genfromtxt(options['nvss_fits_file'],
                              names=True,dtype=None)
    # get the data for this source
    index = np.where(spectral_fits['source'] == options['field'])[0]
    if len(index) == 0:
        print "Error: source not found in spectral fits file."
        return
    spectral_fit = spectral_fits[index[0]]
    index = np.where(nvss_fits['Source'] == options['field'])[0]
    if len(index) == 0:
        print "Error: source not found in nvss fits file."
        return
    nvss_fit = nvss_fits[index[0]]

    # calculate flux normalization factor
    # Best flux is (nvss_1.4GHz/Chris_1.4GHz)*Chris(freq)
    logfreq = np.log10(1400.) # log10(flux_MHz)
    # log(flux(Jy)) = a0 + a1*log(freq(MHz)) or
    # log(flux(Jy)) = a0 + a1*log(freq(MHz)) + a2*exp(-log(freq(MHz)))
    if np.isnan(spectral_fit['a2']):
        chris_flux = spectral_fit['a0'] + spectral_fit['a1']*logfreq
        chris_flux = 10.**chris_flux
    else:
        chris_flux = spectral_fit['a0'] + spectral_fit['a1']*logfreq + spectral_fit['a2']*np.exp(-1.*logfreq)
        chris_flux = 10.**chris_flux
    nvss_flux = nvss_fit['S']/1.e3 # Jy
    norm_flux = nvss_flux/chris_flux
    if options["verbose"]:
        print("Normalized 1.4 GHz flux factor: {0:0.2f}".format(norm_flux))

    # For each beam, this source, each bin,
    # find the appropriate cluster and determine gain (K/Jy)
    num_bins = int(options["band_width"]/options["bin_width"])+1
    for beam in options["beams"]:
        for bn in xrange(num_bins):
            # determine mid-frequency for this bin
            start_freq = options["band_start_freq"]*bn
            mid_freq = start_freq + options["bin_width"]/2.
            # load cluster file
            cluster_file="{0}/beam{1}/{2}/bin{3:03d}/clusters.npz".\
              format(options["cluster_filepath"],beam,
                     options["field"],bn)
            if not os.path.isfile(cluster_file):
                if options["verbose"]:
                    print("Could not find cluster file for {0}, beam {1}, bin {2}.".\
                          format(options["field"],beam,bn))
                    print(cluster_file)
                continue
            data = np.load(cluster_file)
            clusters = data['clusters']
            # find the cluster that corresponds to the calibration source
            best_cluster,best_cluster_num = None,-1
            closest_pos = 999.
            for num,clust in enumerate(clusters):
                # compute distance between clust center and calib source
                nvss_ra = convert_sexi(nvss_fit['RA'],dec=False)
                nvss_dec = convert_sexi(nvss_fit['Dec'],dec=True)
                sep = calc_sep(clust.RA,clust.DEC,nvss_ra,nvss_dec,deg=True)
                if sep < closest_pos:
                    closest_pos = sep
                    best_cluster = clust
                    best_cluster_num = num
            if best_cluster is None:
                print("Error: did not find any good clusters for
                {0}, beam {1}, bin{2}".format(options['field'],
                                              beam,bn))
                continue
            elif sep > 0.001:
                print("Error: best cluster is more than 0.001 degrees
                from NVSS center in {0}, beam {1}, bin {2}".\
                format(options['field'],beam,bn))
                continue
            elif not clust.good_fit:
                print("Error: best cluster does not have good fit
                in {0}, beam {1}, bin {2}".\
                format(options['field'],beam,bn))
            print sep
            
    if options["verbose"]:
        print("Log: Done!")

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
        description="Convert cluster intensity to Jansky.",
        prog='gain_calc.py',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--version', action='version',
                        version='%(prog)s '+vers)
    required=parser.add_argument_group('required arguments:')
    required.add_argument('--field',type=str,
                          help="field to cluster",
                          required=True)
    semi_opt=parser.add_argument_group('arguments set to defaults:')
    semi_opt.add_argument('--cluster_filepath',type=str,
                          help='path where cluster results will go',
                          default="../results/clusters")
    semi_opt.add_argument('--results_filepath',type=str,
                          help='path where gain cal results will go',
                          default="../results/gaincal")
    semi_opt.add_argument('--beams',type=int,nargs="+",
                          help='beams to calibrate',
                          default=[0,1,2,3,4,5,6])
    semi_opt.add_argument('--bin_width',type=float,
                          help='width of analysis bins in MHz',
                          default=5.)
    semi_opt.add_argument('--band_width',type=float,
                          help='width of band in MHz',
                          default=172.5)
    semi_opt.add_argument('--band_start_freq',type=float,
                          help='starting frequency of band in MHz',
                          default=1535.973999) # value from freq.dat for band 0
    semi_opt.add_argument('--spectral_fits_file',type=str,
                          help='file containing spectral fits',
                          default="spectral_fits.txt")
    semi_opt.add_argument('--nvss_fits_file',type=str,
                          help='file containing nvss fits',
                          default="nvss_fits.txt")
    optional=parser.add_argument_group('other optional arguments:')
    optional.add_argument('-v','--verbose',help="verbose analysis",
                          action="store_true")
    optional.add_argument('-f','--file_verbose',
                          help="make lots of intermediate files",
                          action="store_true")
    args = vars(parser.parse_args())
    main(**args)
