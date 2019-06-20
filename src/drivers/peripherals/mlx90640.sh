#!/bin/bash
# run via ssh -X pi@...
# # xauth list | grep unix`echo $DISPLAY | cut -c10-12` > /tmp/xauth
# # sudo xauth add `cat /tmp/xauth`
# # sudo ./mlx90640.sh

. /home/pi/vkc-demo/bin/activate
python mlx90640.py
deactivate

