#!/bin/sh

#Created by jwk to run make_clusters.py on 15 July 2014, improved 26 July 2014, make user specific 16 Aug 2014,22 Oct all calibrator, 16 Dec variables added 
# Modified by tvw to add his stuff too


if [ "$USER" = "jkania" ]; then 
quant=0.06
width=0.025
outpath="/n/fox/jkania/cluster/beam"
inpath="/n/fox/jkania/results/"
logpath="/n/fox/jkania/cluster/log"
mkdir -p $logpath
    for i in 0 #1 2 3 4 5 6
    do
:<<'END'
	python make_clusters.py --field S0957+161 --dates 55183 55184 55188 55189 55191 55192 55193 5519 4\
	    --beams $i  --verbose --file_verbose --quantile $quant --beam_width $width \
	    --source_filepath $inpath --cluster_filepath $outpath$i \
            > $logout/S0957+161_beam"$i"_log.dat &

	python make_clusters.py --field S1009+140 --dates 55183 55184 55187 55188 55189 55191 55192 55193 \
	    --beams $i  --verbose --file_verbose --quantile $quant --beam_width $width \
	    --source_filepath $inpath --cluster_filepath $outpath$i \
	    > logpath/S1009+140_beam"$i"_log.dat &

	python make_clusters.py --field S1026+064 --dates 55183 55184 55187 55188 55189 55191 55192 55193 \
	    --beams $i  --verbose --file_verbose --quantile $quant --beam_width $width \
	    --source_filepath $inpath --cluster_filepath $outpath$i \
	    > $logpath/S1026+064_beam"$i"_log.dat &

	python make_clusters.py --field S1041+027 --dates 55183 55184 55187 55188 55189 55191 55192 55193 \
	    --beams $i  --verbose --file_verbose --quantile $quant --beam_width $width \
	    --source_filepath $inpath --cluster_filepath $outpath$i \
	    > logpath/S1047+027_beam"$i"_log.dat &

	python make_clusters.py --field S1054+032 --dates 55183 55184 55187 55188 55189 55191 55192 55193 \
	    --beams $i  --verbose --file_verbose --quantile $quant --beam_width $width \
	    --source_filepath $inpath --cluster_filepath $outpath$i \
	    > logpath/S1047+027_beam"$i"_log.dat &
END
	python make_clusters.py --field S1106-008 --dates 55183 55184 55187 55188 55189 55191 55192 55193 \
	    --beams $i  --verbose --file_verbose --quantile $quant --beam_width $width \
	    --source_filepath $inpath --cluster_filepath $outpath$i > $logpath/S1106-008_beam"$i"_log.dat &
:<<'END' 
	python make_clusters.py --field S1123+055  --dates 55183 55184 55187 55188 55189 55191 55192 55193 \
	    --beams $i  --verbose --file_verbose --quantile $quant --beam_width $width \
	    --source_filepath $inpath --cluster_filepath $outpath$i> $logout/S1123+055_beam"$i"_log.dat &
END
	python make_clusters.py --field S1135-003 --dates 55183 55184 55187 55188 55189 55191 55192 55193 \
	    --beams $i  --verbose --file_verbose --quantile $quant --beam_width $width \
	    --source_filepath /n/fox/jkania/results --cluster_filepath $outpath$i \
	    > $logpath/S1135-003_beam"$i"_log.dat &

    #wait #so not to use up all of fox's resorces 
    done


elif [ "$USER" = "tghosh" ]; then
    #rm -r /n/fox/jkania/results_cluster

    #python2.7 make_clusters.py --field S1041+027 --dates 55183 55184 55187 55188 55189 55191 55192 55193 \
        --beams 0 --verbose --file_verbose --quantile 0.06 --beam_width 0.025  \
        --source_filepath /n/fox/jkania/results --cluster_filepath /n/fox/jkania/results_cluster

    echo -n "Would you like to transfer the files [y/n]: "
    read ans

    if [ "$ans" = "y" ]; then 
        echo "trasferring the files"
        #rsync -avzr --delete -e ssh /n/fox/jkania/results* jkania@remote.naic.edu:/share/reu2014/jkania
    fi
elif [ "$USER" = "twenger" ]; then
    python2.7 make_clusters.py --field S1041+027 --dates 55183 55184 55187 55188 55189 55191 55192 55193 \
        --beams 0 --verbose --file_verbose --quantile 0.06 --beam_width 0.025  \
        --source_filepath ../results --cluster_filepath ../results/cluster
else 
    echo "User specific, user not recognized"
fi 

echo "Cluster shell done"
