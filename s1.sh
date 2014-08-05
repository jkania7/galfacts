#Shell script created by Joseph Kania                                                                                                                                                  
#9 July 2014, impoved 22 July, 4 Aug 2014                                                                                                                    
#!/bin/sh                                                                                                                                                                                                                             
rm -r ../results/S1

python2.7 find_sources.py --field S1 --band band0 --date 55153 --beam 0 --verbose --file_verbose --exclude_channels 2748 2749 2750 2751 2752 2753 --data_filepath /n/fox/processed/ --num_source_points 12 --point_sep 1 --num_outer_points 10 --rfi_mask 15 --format binary

echo -n "Would you like to transfer the results to AO? [y/n]: "
read ans

case $ans in
    "y" ) echo "trasferring files"
	rsync -avzcr --delete -e ssh /n/fox/jkania/results* jkania@remote.naic.edu:/share/reu2014/jkania/;;
     * ) 
	;;
esac

echo shellDone!
