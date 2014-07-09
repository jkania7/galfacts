#Shell script created by Joseph Kania
#30 June 3014

#!/bin/sh

python2.7 find_sources.py --field S1041+027 --band band0 --date 55183 --beam 0 1 2 3 4 5 6 --num_channels 4096 --verbose --file_verbose --format binary --data_filepath /n/fox/processed/S1_CALS

echo shellDone!
