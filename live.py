# author: Qizhou Wang
# datetime: 12/20/22 4:29 PM
# email: imjoewang@gmail.com
"""
This module
"""
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
gi.require_version("Tcam", "1.0")
gi.require_version("Gst", "1.0")
from gi.repository import Tcam, Gst

Gst.init(sys.argv)
Gst.debug_set_default_threshold(Gst.DebugLevel.WARNING)

pipeline = Gst.parse_launch("tcambin name=bin "
                            " ! video/x-raw,format=GRAY8,width=1920,height=1080,framerate=30/1"
                            " ! videoconvert"
                            " ! ximagesink sync=false")

camera = pipeline.get_by_name("bin")
camera.set_property("serial", 17220805)
pipeline.set_state(Gst.State.PLAYING)
time.sleep(2)
pipeline.set_state(Gst.State.NULL)

