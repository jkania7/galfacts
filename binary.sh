#Shell script created by Joseph Kania
#30 June 3014

#!/bin/sh

python2.7 find_sources.py --field S1041+027 --band band0 --date 55183 --beam 0 --num_channels 4096 --verbose --file_verbose --format binary --exclude_channels 2750 2751 2752 2753 2754 2755 2756 2757 2758 2759 2760 2761 2762 2763 3764 2765 --data_filepath /n/fox/processed/S1_CALS

echo shellDone!
