#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 18:39:43 2025

@author: risalinux
"""

import rosbag
from tqdm import tqdm
from scipy.spatial.transform import Rotation as R
import numpy as np
orientation=[]
int_orientation=[]
#/media/risalinux/Seagate Basic/Dataset
import sys
path=sys.argv[1]
with rosbag.Bag(path) as inbag:
    for topic in inbag.get_type_and_topic_info()[1]:
        if inbag.get_type_and_topic_info()[1][topic][0]=='sensor_msgs/Imu':
            break
    print(topic)
    for topic,msg,t in tqdm(inbag.read_messages(topics=[topic]),total=inbag.get_type_and_topic_info()[1][topic][1]):
        print(t)
        print(msg.header.stamp.secs)
        try:
            transform=R.from_quat([msg.orientation.x,msg.orientation.y,msg.orientation.z,msg.orientation.w])
        except:
            print([msg.orientation.x,msg.orientation.y,msg.orientation.z,msg.orientation.w])
            print([msg.angular_velocity.x,msg.angular_velocity.y,msg.angular_velocity.z])
            continue
        vec=transform.as_matrix()@[0,0,1]
        orientation.append(vec)
        
        if len(int_orientation)==0:
            int_orientation.append(vec)
        else:
            angvec=np.array([msg.angular_velocity.x,msg.angular_velocity.y,msg.angular_velocity.z])
            transform=R.from_euler('xyz', angvec*(t-last_t))
            int_orientation.append((last_transform*transform).as_matrix()@[0,0,1])
        last_transform=transform
        last_t=t
import matplotlib.pyplot as plt
plt.plot(orientation)
plt.plot(int_orientation)
print(t)
            