#Shell script created by Joseph Kania                                                                                                                                                    #9 July 2014                                                                                                                       
#!/bin/sh                                                                                                                                                                                                                             

python2.7 find_sources.py --field S1 --band band0 --date 55153 --exclude_channels 2755 2756 2757 2758 2759 2760 2761 2762 2763 2764 2765 --beam 0 --num_channels 4096 --verbose --file_verbose --format binary --data_filepath /n/fox/processed

echo shellDone!
