#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 17:45:46 2025

@author: risalinux
"""

import rosbag
import sys

with rosbag.Bag(sys.argv[2], 'a') as outbag:
    for point_topic in outbag.get_type_and_topic_info()[1]:
        if outbag.get_type_and_topic_info()[1][point_topic][0]=='sensor_msgs/PointCloud2':
            break 
    for (topic, msg, t),(u,i,timestamp) in zip(rosbag.Bag(sys.argv[1]).read_messages(),outbag.read_messages(topics=[point_topic])):
        outbag.write(topic, msg, timestamp)