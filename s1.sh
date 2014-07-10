#Shell script created by Joseph Kania                                                                                                                                                    #9 July 2014                                                                                                                       
#!/bin/sh                                                                                                                                                                                                                             

python2.7 find_sources.py --field S1 --band band0 --rfi_mask 20 --source_mask 8 --date 55153 --exclude_channels 2745 2746 2747 2748 2749 2750 2751 2752 2753 2754 2755 --beam 0 --num_channels 4096 --verbose --file_verbose --format binary --data_filepath /n/fox/processed

echo shellDone!
