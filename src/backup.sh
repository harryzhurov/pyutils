#!/bin/sh

rsync -rvz ~/pro root@5.128.60.74:/nas/vol2/backup
rsync -rvz ~/slon root@5.128.60.74:/nas/vol2/backup
rsync -rvz /pool/cad/kicad/tools root@5.128.60.74:/nas/vol2/backup
