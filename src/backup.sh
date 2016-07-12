#!/bin/sh

RSYNC=$(which rsync)

$RSYNC -rvz ~/pro root@5.128.60.74:/nas/vol2/backup
$RSYNC -rvz ~/slon root@5.128.60.74:/nas/vol2/backup
$RSYNC -rvz /pool/cad/kicad/tools root@5.128.60.74:/nas/vol2/backup

date --rfc-3339=seconds >> ~/backup.log
