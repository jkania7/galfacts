#Created by jkania on 2 Aug 2014
#!/bin/sh

rsync -avz --delete -e ssh /share/reu2014/jkania/galfacts/*.py jkania@fox.ras.ucalgary.ca:/n/fox/jkania/galfacts
rsync -avz -e ssh /share/reu2014/jkania/galfacts/*.sh jkania@fox.ras.ucalgary.ca:/n/fox/jkania/galfacts

echo transferDone!