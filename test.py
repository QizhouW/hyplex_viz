# author: Qizhou Wang
# datetime: 12/20/22 5:09 PM
# email: imjoewang@gmail.com
"""
This module tests the recorded image quality.
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









