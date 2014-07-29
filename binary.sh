#Shell script created by Joseph Kania
#30 June 3014, improved 22 July 2014

#!/bin/sh

rm -r ../results_test

python2.7 find_sources.py --field S1041+027 --band band0 --date 55183 --beam 0  --verbose --file_verbose --exclude_channels  2749 2750 2751 2752  --data_filepath /n/fox/processed/S1_CALS --num_source_points 12 --point_sep 1 --num_outer_points 10 --results_filepath ../results_test --rfi_mask 15 --format ascii

echo -n "Would you like to transfer the results to AO? [y/n]: "
read ans

case $ans in
    "y" ) echo "transerring files"
	rsync -avzcr --delete -e ssh /n/fox/jkania/results* jkania@remote.naic.edu:/share/reu2014/jkania/results;;
    * )
	;;
esac

echo shellDone!
