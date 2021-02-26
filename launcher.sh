#! /bin/bash


#rfcomm bind rfcomm1 00:1D:A5:1B:27:CF
chmod 777 /dev/rfcomm0
python3 main.py
sleep 1000

