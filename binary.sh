#Shell script created by Joseph Kania
#30 June 3014

#!/bin/sh

python2.7 find_sources.py --field S1041+027 --band band0 --date 55183 --beam 0 --num_channels 4096 --verbose --file_verbose --format binary --exclude_channels 2759 2760 2761 2762 2763 2764 2765 --data_filepath /n/fox/processed/S1_CALS

echo shellDone!
