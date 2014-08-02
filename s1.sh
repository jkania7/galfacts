#Shell script created by Joseph Kania                                                                                                                                                  
#9 July 2014, impoved 22 July 2014                                                                                                                    
#!/bin/sh                                                                                                                                                                                                                             
rm -r ../results/S1

python2.7 find_sources.py --field S1 --band band0 --date 55153 --exclude_channels 2755 2756 2757 2758 2759 2760 2761 2762 2763 2764 2765 --beam 0 --num_channels 4096 --verbose --file_verbose --format binary --data_filepath /n/fox/processed

echo -n "Would you like to transfer the results to AO? [y/n]: "
read ans

case $ans in
    "y" ) echo "trasferring files"
	rsync -avzcr --delete -e ssh /n/fox/jkania/results* jkania@remote.naic.edu:/share/reu2014/jkania/;;
     * ) 
	;;
esac

echo shellDone!
