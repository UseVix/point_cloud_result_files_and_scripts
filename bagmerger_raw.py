#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 17:21:20 2025

@author: risalinux
"""

import rosbag
import sys
from tqdm import tqdm
with rosbag.Bag(sys.argv[2], 'a') as outbag:
    with rosbag.Bag(sys.argv[1], 'r') as inbag:
        for topic, msg, timestamp in tqdm(inbag.read_messages(), total=inbag.get_message_count()):
            outbag.write(topic, msg, timestamp)