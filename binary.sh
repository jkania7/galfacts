#Shell script created by Joseph Kania
#30 June 3014

#!/bin/sh

python2.7 find_sources.py --field S1041+027 --band band0 --date 55183 --beam 0  --verbose --file_verbose --exclude_channels 2740 2741 2742 2743 2744 2745 2746 2747 2748 2749 2750 2751 2752 2753 2754 2755 2756 2757 2758 2759 2760 2761 2762 --data_filepath /n/fox/processed/S1_CALS

echo shellDone!
