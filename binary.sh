#Shell script created by Joseph Kania
#30 June 3014

#!/bin/sh

python2.7 find_sources.py --field S1 --date 55153 --beam 0 --exclude_channels 1369 1370 1371 1372 1373 1374 1375 1376 1377 1378 1379 1380 1381 --verbose --file_verbose --format binary --data_filepath /n/fox/processed

echo shellDone!
