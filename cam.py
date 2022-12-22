#!/usr/bin/env python3
# This example will show you how to enable trigger-mode
# and how to trigger images with via software trigger.
#
import h5py
import subprocess, os
script='tiscamera-env.sh'
pipe = subprocess.Popen(f"source ./{script}; env", stdout=subprocess.PIPE, shell=True)
output = pipe.communicate()[0]
env = dict((line.decode("utf-8").split("=", 1) for line in output.splitlines()))
os.environ.update(env)
import TIS
import cv2
import gi
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import os
gi.require_version("Gst", "1.0")
gi.require_version("GstVideo", "1.0")
from gi.repository import Gst, GstVideo


tmp=None
framecount = 0
#img=np.zeros((3000,4000),dtype=np.uint8)
ccstring = 'MP42'
fourcc = cv2.VideoWriter_fourcc(*ccstring)
out1 = cv2.VideoWriter(f'./{ccstring}_downsample.avi',fourcc, 30, (1000,1000),0)
out2 = cv2.VideoWriter(f'./{ccstring}_downsample2.avi',fourcc, 30, (1000,1000),0)
#cv2.VIDEOWRITER_PROP_QUALITY=0.5

def callback(appsink, user_data):
    """
    This function will be called in a separate thread when our appsink
    says there is data for us. user_data has to be defined
    when calling g_signal_connect. It can be used to pass objects etc.
    from your other function to the callback.
    """
    sample = appsink.emit("pull-sample")
    global framecount,tmp
    caps = sample.get_caps()
    if sample:
        gst_buffer = sample.get_buffer()
        try:
            (ret, buffer_map) = gst_buffer.map(Gst.MapFlags.READ)
            ### User defined operations based on the buffermap
            #d = gst_buffer.extract_dup(0, gst_buffer.get_size())
            img = np.ndarray((3000,4000,1),buffer=buffer_map.data,dtype=np.uint8)
            #img = img[::3,::4]
            #print(img.shape)
            #frame = cv2.flip(frame, 0)
            out1.write(img[::3,::4])
            out2.write(img[1::3,1::4])
            out2.write(img[1::3, 1::4])
            out2.write(img[1::3, 1::4])
            out2.write(img[1::3, 1::4])
            out2.write(img[1::3, 1::4])
            out2.write(img[1::3, 1::4])
            out2.write(img[1::3, 1::4])
            out2.write(img[1::3, 1::4])
            #filename=f'./channel0/{framecount}.png'
            #cv2.imwrite(filename, img)
            print(framecount)
            tmp=img
            framecount += 1

        finally:
            ## reload the buffer_map to the stream
            gst_buffer.unmap(buffer_map)
            pass

    return Gst.FlowReturn.OK

Gst.init(sys.argv)  # init gstreamer
Gst.debug_set_default_threshold(Gst.DebugLevel.WARNING)

serial = 17220805

pipeline = Gst.parse_launch("tcambin name=source"
                            " ! video/x-raw,format=GRAY8,width=4000,height=3000,framerate=30/1"
                            " ! videoconvert"
                            " ! appsink name=sink")
# test for error
if not pipeline:
    print("Could not create pipeline.")
    sys.exit(1)

# The user has not given a serial, so we prompt for one
if serial is not None:
    source = pipeline.get_by_name("source")
    source.set_property("serial", serial)

sink = pipeline.get_by_name("sink")

# tell appsink to notify us when it receives an image
sink.set_property("emit-signals", True)

user_data = "This is our user data"

# tell appsink what function to call when it notifies us
sink.connect("new-sample", callback, user_data)

pipeline.set_state(Gst.State.PLAYING)

print("Press Ctrl-C to stop.")

# We wait with this thread until a
# KeyboardInterrupt in the form of a Ctrl-C
# arrives. This will cause the pipline
# to be set to state NULL

time.sleep(10)

pipeline.set_state(Gst.State.NULL)
