#Shell script created by Joseph Kania                                                                                                                                                                                        
#30 June 3014, improved 22 July 2014                                                                                                                                                                                                                
#!/bin/sh                                                                                                                                                                                                                    
rm -r ../results/S1041+027

for i in 55183 55184  55187  55188  55189  55191  55192  55193
do
    python2.7 find_sources.py --field S1041+027 --band band0 --date "$i"   --beam 0 1 2 3 4 5 6  --verbose --file_verbose --exclude_channels  2748 2749 2750 2751 2752 2753  --data_filepath /n/fox/processed/S1_CALS --num_source_points 12 --point_sep 1 --num_outer_points 10 --results_filepath ../results_test --rfi_mask 25 --format ascii
done 

echo -n "Would you like to transfer the results to AO? [y/n]: "
read ans

case $ans in
    "y" ) echo "transerring files"
	rsync -avzcr --delete -e ssh /n/fox/jkania/results* jkania@remote.naic.edu:/share/reu2014/jkania;;
    * )
	;;
esac

echo shellDone!
