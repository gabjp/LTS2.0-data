#!/bin/bash

python dwnld_crops.py;
rc=$?;
echo rc; 
while [ $rc != 0 ]; do
python dwnld_crops.py;
rc=$?;
done