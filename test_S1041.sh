#Shell script created by Joseph Kania
#30 June 3014, improved 22 July 2014

#!/bin/sh
echo "Hello $USER"

if [ "$USER" = "jkania" ]; then
    rm -r ../results_test
 
    python2.7 find_sources.py --field S1041+027 --band band0 --date 55183 \
	--beam 0  --verbose --file_verbose --exclude_channels  2749 2750 2751 2752  \
	--data_filepath /n/fox/processed/S1_CALS  --results_filepath ../results_test \
	--format ascii --min_DEC 2.52 --max_DEC 2.92 --min_RA 158.80 --max_RA 161.70

    echo -n "Would you like to transfer the results to AO? [y/n]: "
    read ans    
    if [ "$ans" = "y" ]; then
	echo "transerring files"
	rsync -avzr --delete -e ssh /n/fox/jkania/results* jkania@remote.naic.edu:/share/reu2014/jkania/
    fi
elif [ "$USER" = "tghosh" ]; then 
    rm -r ../results_test
    #tghosh's statment
    #python2.7 find_sources.py --field S1041+027 --band band0 --date 55183 \
	--beam 0  --verbose --file_verbose --exclude_channels  2749 2750 2751 2752 \
	--data_filepath /n/fox/processed/S1_CALS  --results_filepath ../results_test \
	--format ascii --min_DEC 2.52 --max_DEC 2.92 --min_RA 158.80 --max_RA 161.70

    echo -n "Would you like to transfer the results to AO? [y/n]: "
    read ans
    if [ "$ans" = "y" ]; then
        echo "transerring files"
	#tghosh rsync
        #rsync -avzr --delete -e ssh /n/fox/jkania/results* jkania@remote.naic.edu:/share/reu2014/jkania/
    fi
else 
    echo "This script is user specific, user not recoginized"
fi 
echo shellDone!
