#!/bin/sh

#Created by jwk to run make_clusters.py on 15 July 2014, improved 26 July 2014, make user specific 16 Aug 2014
# Modified by tvw to add his stuff too


if [ "$USER" = "jkania" ]; then 
    rm -r /n/fox/jkania/results_cluster
    
    python2.7 make_clusters.py --field S1041+027 --dates 55183 55184 55187 55188 55189 55191 55192 55193 \
	--beams 0 --verbose --file_verbose --quantile 0.06 --beam_width 0.025 \
	--source_filepath /n/fox/jkania/results --cluster_filepath /n/fox/jkania/results_cluster

    echo -n "Would you like to transfer the files [y/n]: "
    read ans

    if [ "$ans" = "y" ]; then 
	echo "trasferring the files"
	rsync -avzr --delete -e ssh /n/fox/jkania/results* jkania@remote.naic.edu:/share/reu2014/jkania
    fi
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
