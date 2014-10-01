
#Shell script created by Joseph Kania on 29 Aug 2014

#!/bin/sh

echo "Hello $USER"

if [ "$USER" = "jkania" ]; then                                                                                     
    rm -r ../results/S1026+064

    for i in 55183 55184  55189  55189  55189  55191  55192 55193 55194
    do
        python2.7 find_sources.py --field S0957+161 --band band0 --date "$i"  \
            --beam 0 1 2 3 4 5 6  --verbose --file_verbose \
            --exclude_channels  2748 2749 2750 2751 2752 2753  \
            --data_filepath /n/fox/processed/S1_CALS  --format ascii
    done
    #echo -n "Would you like to transfer the results to AO? [y/n]: "
    #read ans

    #if [ "$ans" = "y" ]; then
     #   echo "transerring files"
      #  rsync -avzr --delete -e ssh /n/fox/jkania/results* jkania@remote.naic.edu:/share/reu2014/jkania/
    fi
elif[ "$USER" = "tghosh" ]; then
    rm -r ../results/S1026+064

    for i in 55183 55184  55187  55188  55189  55191  55192  55193
    do
        #python2.7 find_sources.py --field S1026+064 --band band0 --date "$i"  \
            --beam 0 1 2 3 4 5 6  --verbose --file_verbose \
            --exclude_channels  2748 2749 2750 2751 2752 2753  \
            --data_filepath /n/fox/processed/S1_CALS  --format ascii
    done
    echo -n "Would you like to transfer the results to AO? [y/n]: "
    read ans

    if [ "$ans" = "y" ]; then
        echo "transerring files"
        #rsync -avzr --delete -e ssh /n/fox/jkania/results* jkania@remote.naic.edu:/share/reu2014/jkania/
    fi
else
    echo "User specific script, you are not recognized"
fi



echo shellDone!
