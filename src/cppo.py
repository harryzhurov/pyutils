#!/usr/bin/python3

import os
import sys
import shutil


idir = sys.argv[1]
odir = sys.argv[2]

#tree = os.walk(idir)

#for i in tree:
#    print(i)

olist = []

for subdir, dirs, files in os.walk(idir):
    for file in files:
        olist.append( os.path.join(subdir, file) )

olist.sort()
        
for i in olist:
    d = os.path.join(odir, os.path.dirname(i))
    if not os.path.exists(d):
        print('create dir: ' + d)
        os.makedirs(d)
    dstpath = os.path.join(d, os.path.basename(i))
    print('copy file: ' + dstpath)
    shutil.copyfile(i, dstpath)

