# author: Qizhou Wang
# datetime: 12/20/22 3:48 PM
# email: imjoewang@gmail.com
"""
This module
"""

import os


def set_env():
    os.environ['PKG_CONFIG_PATH']="/usr/lib/x86_64-linux-gnu/pkgconfig"
    GST_PLUGIN_PATH_1_0 = "/usr/lib/x86_64-linux-gnu/gstreamer-1.0"
    LD_RUN_PATH = "/usr/lib"
    GI_TYPELIB_PATH = "/usr/lib/x86_64-linux-gnu/girepository-1.0:"
    LD_LIBRARY_PATH = "/usr/lib:/usr/lib/tcam-0"