#Shell script created by Joseph Kania
#30 June 3014

#!/bin/sh

python2.7 find_sources.py --field S1 --date 55153 --beam 0 --num_channels 4096 --verbose --file_verbose --format binary --data_filepath /n/fox/processed

echo shellDone!
