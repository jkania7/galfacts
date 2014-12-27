#Shell script created by Joseph Kania 6 oct 2014
#make sure you have a clean /runout/ folder

#!/bin/bash
declare -a beams=(0 1 2 3 4 5 6)
exclude=(2748 2749 2750 2751 2752 2753)
inpath="/n/fox/processed/S1_CALS"
logpath="/n/fox/jkania/test/log"
mkdir -p $logpath
echo $beams
:<<'END' 
for i in 55183 55184 55188 55189 55191 55192 55193 55194
do
    python find_sources.py --field S0957+161  --band band0 --date $i \
        --beam $beams  --verbose --file_verbose \
        --exclude_channels  $exclude  --data_filepath $inpath  --format ascii \
	--min_RA 146.25 --max_RA 150.5  --min_DEC 15.867 --max_DEC 16.367 > $logpath/S0957+161_"$i"_log.dat &
done 

for i in 55183 55184 55187 55188 55189 55191 55192 55193
do
    python find_sources.py --field S1009+140 --band band0 --date $i \
        --beam $beams  --verbose --file_verbose \
        --exclude_channels  $exclude --data_filepath $inpath  --format ascii \
	--min_RA 151.0 --max_RA 154.25 --min_DEC 13.783 --max_DEC 14.283 > $logpath/S1009+140_"$i"_log.dat &
done 

wait #remove for larger computer

for i in 55183 55184 55187 55188 55189 55191 55192 55193 
do
    python find_sources.py --field S1026+064 --band band0 --date $i \
        --beam $beams  --verbose --file_verbose \
        --exclude_channels  $exclude  --data_filepath $inpath  --format ascii \
	--min_RA 155.25 --max_RA 158.25 --min_DEC 6.217 --max_DEC 6.717 > $logpath/S1026+064_"$i"_log.dat &
done 

for i in 55183 55184 55187 55188 55189 55191 55192 55193 
do
    python find_sources.py --field S1041+027  --band band0 --date $i \
        --beam $beams  --verbose --file_verbose \
        --exclude_channels  $exclude  --data_filepath $inpath  --format ascii \
	--min_RA 158.75 --max_RA 161.75 --min_DEC 2.467 --max_DEC 2.967 > $logpath/S1041+027_"$i"_log.dat &
done 

wait #remove later

for i in 55183 55184 55187 55188 55189 55191 55192 55193
do
    python find_sources.py --field  S1054+032 --band band0 --date $i \
        --beam $beams  --verbose --file_verbose \
        --exclude_channels  $exclude  --data_filepath /n/fox/processed/S1_CALS  --format binary \
	--min_RA 162.00 --max_RA 164.75 --min_DEC 3.0 --max_DEC 3.50 > $logpath/S1054+032_"$i"_log.dat &
done 

for i in 55183 55184 55187 55188 55189 55191 55192 55193
do
    python find_sources.py --field S1106-008  --band band0 --date $i \
        --beam $beams  --verbose --file_verbose \
        --exclude_channels  $exclude  --data_filepath $inpath  --format binary \
	--min_RA 165.25 --max_RA 168.5 --min_DEC -1.133 --max_DEC -0.633 > $logpath/S1106-008_"$i"_log.dat &
done 

wait #remove later
END
for i in 55183 55184 55187 55188 55189 55191 55192 55193 
do
    python find_sources.py --field S1123+055 --band band0 --date $i \
        --beam ${beams[@]}  --verbose --file_verbose \
        --exclude_channels  ${exclude[@]}  --data_filepath $inpath  --format ascii \
	--min_RA 169.25 --max_RA 172.0 --min_DEC 5.25 --max_DEC 5.75 --results_filepath ../test > $logpath/S1123+055_"$i"_log.dat &
done 

wait
echo -e "Done with S1123+055"

for i in 55183 55184 55187 55188 55189 55191 55192 55193 
do
    python find_sources.py --field S1135-003 --band band0 --date "$i" \
        --beam ${beams[@]}   --verbose --file_verbose \
        --exclude_channels  ${exclude[@]}  --data_filepath $inpath  --format binary \
	--min_RA 172.50 --max_RA 174.75 --min_DEC -0.60 --max_DEC -0.10 --results_filepath ../test > $logpath/S1135-003_"$i"_log.dat &

done 

wait #to get the timing right
echo -e "Done with S1135-003"
echo shellDone!
