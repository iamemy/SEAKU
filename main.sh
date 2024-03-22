#!/bin/bash

# Determine if a process is already
# using raspivid, and kill it.
if [ $(ps -aux | grep /usr/bin/vlc -c) -gt 1 ]; then
    ps -aux | grep /usr/bin/vlc | grep -o -E '[0-9]+' | head -n 1 | xargs kill
fi

# Call raspivid in stream mode to
# redirect its output as cvlc input for
# sending the camera stream through IP.
raspivid -o - -n -t 0 -hf -w 1080 -h 720 -fps 24 | cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8888}' :demux=h264 > vlc.log 2>&1 &

# Stop the program if any
# of the instructions fails,
# to avoid starting the
# python code if the video failed.
if [ $? -ne 0 ]; then
    echo "Please retry in 5 seconds"
    exit 1
fi

# Run the Python code for interfacing
# the sensors and write the screen.
sudo python3 interface.py
