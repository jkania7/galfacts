#Created by jwk to run make_clusters.py on 15 July 2014

#!/bin/sh

python make_clusters.py --field S1041+027 --dates 55183 55184 55187 55188 55189 55191 55192 55193 --beams 0 --verbose --file_verbose --quantile 0.06 --beam_width 0.025  --source_filepath /n/fox/jkania/results --cluster_filepath /n/fox/jkania/beam0_clusters

echo "Cluster shell done"
