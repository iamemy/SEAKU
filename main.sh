#!/bin/bash

# Call raspivid in stream mode to
# redirect its output as cvlc input for
# sending the camera stream through IP.
raspivid -o - -n -t 0 -hf -w 1080 -h 720 -fps 24 | cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8888}' :demux=h264 > vlc.log 2>&1 &

# Run the Python code for interfacing
# the sensors and write the screen.
python interface.py
