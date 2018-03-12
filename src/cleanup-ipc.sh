#!/bin/bash

for i in $(ipcs -s | grep $USER | awk '{print $2}'); do ipcrm sem $i; done 
for i in $(ipcs -m | grep $USER | awk '{print $2}'); do ipcrm -m $i; done 

