#!/bin/bash
#script to start python startup script and background screen

/usr/bin/feh  -Y -x -q -D 5 -B black -F -Z -z -r /home/pi/Pictures
/usr/bin/python3 /home/pi/startupscript.py