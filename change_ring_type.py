#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 22:13:36 2025

@author: risalinux
"""

import sys
import rosbag
#from sensor_msgs import PointCloud2
import sensor_msgs.point_cloud2 as pc2
from tqdm import tqdm
with rosbag.Bag(sys.argv[1], 'r') as inbag:
    with rosbag.Bag(sys.argv[2], 'w') as outbag:
        for topic, msg, timestamp in tqdm(inbag.read_messages(), total=inbag.get_message_count()):
            #print(type(msg))
            if str(type(msg))=="<class 'tmpwntxs96z._sensor_msgs__PointCloud2'>":
                #print("hit")
                if msg.fields[6].datatype==4:
                    msg.fields[6].datatype=2
                else:
                    if msg.fields[6].datatype==2:
                        msg.fields[6].datatype=4
            outbag.write(topic, msg, timestamp)
                        