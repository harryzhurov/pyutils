#!/usr/bin/python3

import os
import sys
import shutil
from pathlib import Path

idir = Path(sys.argv[1]).absolute()
odir = Path(sys.argv[2]).absolute()

print('copy files from "' + str(idir) + '" to "' + str(odir) + '"')

tree = [x for x in Path(idir).rglob('*') if x.is_file()]
tree.sort()

for i in tree:
    dstpath = str(i).replace(str(idir), str(odir))
    print('copy file: ' + str(i) + ' -> ' + dstpath)
    if not Path(dstpath).parent.exists():
        Path(dstpath).parent.mkdir(parents=True)
    shutil.copyfile(i, dstpath)

