#Shell script created by Joseph Kania                                                                                                                                                                                        
#30 June 3014, improved 22 July 2014                                                                                                                                                                                                                
#!/bin/sh                                                                                                                                                                                                                    
rm -r ../results/S1041+027

for i in 55183 55184  55187  55188  55189  55191  55192  55193
do
    python2.7 find_sources.py --field S1041+027 --band band0 --date "$i"   --beam 0  --verbose --file_verbose --exclude_channels 2740 2741 2742 2743 2744 2745 2746 2747 2748 2749 2750 2751 2752 2753 2754 2755 2756 2757 2758 2759 2760 2761 2762 --data_filepath /n/fox/processed/S1_CALS --rfi_mask 15 --num_source_points 17 --point_sep 0 
done 

echo shellDone!
