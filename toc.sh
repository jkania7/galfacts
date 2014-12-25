#!/bin/bash

rsync -avz -e ssh --delete --exclude '.git'/*'/.sh*'/'.py*'/'#*' ./* jkania@fox.ras.ucalgary.ca:/n/fox/jkania/galfacts/
