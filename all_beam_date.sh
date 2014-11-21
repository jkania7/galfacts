#Shell script created by Joseph Kania 6 oct 2014
#make sure you have a clean /runout/ folder

#!/bin/sh
:<<'END'
for i in 55183 55184 55188 55189 55191 55192 55193 55194
do
    python find_sources.py --field S0957+161  --band band0 --date "$i" \
        --beam 0 1 2 3 4 5 6  --verbose --file_verbose \
        --exclude_channels  2748 2749 2750 2751 2752 2753  \
        --data_filepath /n/fox/processed/S1_CALS  --format ascii \
	--min_RA 146.25 --max_RA 150.5  --min_DEC 15.867 --max_DEC 16.367 > /n/fox/jkania/results/runout/S0957+161_"$i"_runout.dat &
done 

for i in 55183 55184 55187 55188 55189 55191 55192 55193
do
    python find_sources.py --field S1009+140 --band band0 --date "$i" \
        --beam 0 1 2 3 4 5 6  --verbose --file_verbose \
        --exclude_channels  2748 2749 2750 2751 2752 2753  \
        --data_filepath /n/fox/processed/S1_CALS  --format ascii \
	--min_RA 151.0 --max_RA 154.25 --min_DEC 13.783 --max_DEC 14.283 > /n/fox/jkania/results/runout/S1009+140_"$i"_runout.dat &
done 

wait #remove for larger computer

for i in 55183 55184 55187 55188 55189 55191 55192 55193 
do
    python find_sources.py --field S1026+064 --band band0 --date "$i" \
        --beam 0 1 2 3 4 5 6  --verbose --file_verbose \
        --exclude_channels  2748 2749 2750 2751 2752 2753  \
        --data_filepath /n/fox/processed/S1_CALS  --format ascii \
	--min_RA 155.25 --max_RA 158.25 --min_DEC 6.217 --max_DEC 6.717 > /n/fox/jkania/results/runout/S1026+064_"$i"_runout.dat &
done 

for i in 55183 55184 55187 55188 55189 55191 55192 55193 
do
    python find_sources.py --field S1041+027  --band band0 --date "$i" \
        --beam 0 1 2 3 4 5 6  --verbose --file_verbose \
        --exclude_channels  2748 2749 2750 2751 2752 2753  \
        --data_filepath /n/fox/processed/S1_CALS  --format ascii \
	--min_RA 158.75 --max_RA 161.75 --min_DEC 2.467 --max_DEC 2.967 > /n/fox/jkania/results/runout/S1041+027_"$i"_runout.dat &
done 

wait #remove later

for i in 55183 55184 55187 55188 55189 55191 55192 55193
do
    python find_sources.py --field  S1054+032 --band band0 --date "$i" \
        --beam 0 1 2 3 4 5 6  --verbose --file_verbose \
        --exclude_channels  2748 2749 2750 2751 2752 2753  \
        --data_filepath /n/fox/processed/S1_CALS  --format binary \
	--min_RA 162.00 --max_RA 164.75 --min_DEC 3.0 --max_DEC 3.50 > /n/fox/jkania/results/runout/S1054+032_"$i"_runout.dat &
done 

for i in 55183 55184 55187 55188 55189 55191 55192 55193
do
    python find_sources.py --field S1106-008  --band band0 --date "$i" \
        --beam 0 1 2 3 4 5 6  --verbose --file_verbose \
        --exclude_channels  2748 2749 2750 2751 2752 2753  \
        --data_filepath /n/fox/processed/S1_CALS  --format binary \
	--min_RA 165.25 --max_RA 168.5 --min_DEC -1.133 --max_DEC -0.633 > /n/fox/jkania/results/runout/S1106-008_"$i"_runout.dat &
done 

wait #remove later

for i in 55183 55184 55187 55188 55189 55191 55192 55193 
do
    python find_sources.py --field S1123+055 --band band0 --date "$i" \
        --beam 0 1 2 3 4 5 6  --verbose --file_verbose \
        --exclude_channels  2748 2749 2750 2751 2752 2753  \
        --data_filepath /n/fox/processed/S1_CALS  --format ascii \
	--min_RA 169.25 --max_RA 172.0 --min_DEC 5.25 --max_DEC 5.75 > /n/fox/jkania/results/runout/S1123+055_"$i"_runout.dat &
done 
END

for i in 55183 #55184 55187 55188 55189 55191 55192 55193 
do
    python find_sources.py --field S1135-003 --band band0 --date "$i" \
        --beam 0   --verbose --file_verbose \
        --exclude_channels  2748 2749 2750 2751 2752 2753  \
        --data_filepath /n/fox/processed/S1_CALS  --format binary \
	--min_RA 172.50 --max_RA 174.75 --min_DEC -0.60 --max_DEC -0.10 --results_filepath ../test
    #> /n/fox/jkania/results/runout/S1135-003_"$i"_runout.dat &
done 

wait #to get the timing right
echo shellDone!
