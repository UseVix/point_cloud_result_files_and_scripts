#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  1 17:57:51 2025

@author: risalinux
"""
import rosbags
from rosbags.rosbag2 import Reader
from rosbags.rosbag2 import Writer
import sys
from pathlib import Path
from rosbags.typesys import Stores, get_types_from_msg, get_typestore
from geometry_msgs.msg import TransformStamped,Quaternion, Vector3
import numpy as np
from tf2_msgs.msg import TFMessage

def guess_msgtype(path: Path) -> str:
    """Guess message type name from path."""
    name = path.relative_to(path.parents[2]).with_suffix('')
    if 'msg' not in name.parts:
        name = name.parent / 'msg' / name.name
    return str(name)

from tqdm import tqdm
typestore = get_typestore(Stores.ROS2_HUMBLE)
add_types = {}

for pathstr in ['/home/risalinux/compression_ws/src/point_cloud_transport_plugins/point_cloud_interfaces/msg/CompressedPointCloud2.msg']:
    msgpath = Path(pathstr)
    msgdef = msgpath.read_text(encoding='utf-8')
    add_types.update(get_types_from_msg(msgdef, guess_msgtype(msgpath)))

typestore.register(add_types)


pathtobase=sys.argv[1]
pathtosave=sys.argv[2]

with Reader(pathtobase) as reader:
    for connection in reader.connections:
        if connection.msgtype == 'sensor_msgs/msg/Imu':
            print(reader.messages([connection]))
            break
    with Writer(pathtosave) as writer:
        topic = '/tf'
        msgtype = 'tf2_msgs/msg/TFMessage'
        connection_writer = writer.add_connection(topic, msgtype, typestore=typestore)
        connection_writer_static = writer.add_connection('/tf_static', msgtype, typestore=typestore)
        integrated=np.array([0.0,0.0,0.0])
        double_integrated=np.array([0.0,0.0,0.0])
        integrated_angle=np.array([0.0,0.0,0.0])
        vector_acceleration=None
        for (con, t, msg) in tqdm(reader.messages([connection]),total=connection.msgcount):
            message=TransformStamped()
            #message.transform.rotation=msg.orientation
            if vector_acceleration is None:
                vector_acceleration=np.empty(3)
                vector_angular=np.empty(3)
                print(t)
            else:
                tdif=(t-last_t)/(10**9)
                double_integrated=(tdif**2)/2*vector_acceleration+integrated*tdif+double_integrated
                integrated=vector_acceleration*tdif+integrated
                integrated_angle=integrated_angle+tdif*vector_angular
            msg=rosbags.serde.deserialize_cdr(msg,con.msgtype)
            vector_acceleration[0]=msg.linear_acceleration.x
            vector_acceleration[1]=msg.linear_acceleration.y
            vector_acceleration[2]=msg.linear_acceleration.z
            vector_angular[0]=msg.angular_velocity.x
            vector_angular[1]=msg.angular_velocity.y
            vector_angular[2]=msg.angular_velocity.z
            message.transform.rotation.x=integrated_angle[0]
            message.transform.rotation.x=integrated_angle[1]
            message.transform.rotation.x=integrated_angle[2]
            last_t=t
            message.transform.translation.x=double_integrated[0]
            message.transform.translation.y=double_integrated[1]
            message.transform.translation.z=double_integrated[2]
            message.header.stamp.sec=msg.header.stamp.sec
            message.header.stamp.nanosec=msg.header.stamp.nanosec
            timestamp=msg.header.stamp.sec*(10**9)+msg.header.stamp.nanosec
            message.header.frame_id='odom'
            message.child_frame_id='base_link'
            tf2msg=TFMessage()
            tf2msg.transforms.append(message)
            message=rosbags.serde.serialize_cdr(tf2msg,msgtype)
            writer.write(connection_writer,timestamp,message)
            message=TransformStamped()
            message.transform.translation=Vector3(x=0.001, y=0.000, z=0.091)
            message.transform.rotation=Quaternion(x=0.000, y=0.000, z=0.000, w=1.000)
            message.header.frame_id='base_link'
            message.child_frame_id='os_sensor'
            tf2msg=TFMessage()
            tf2msg.transforms.append(message)
            message=rosbags.serde.serialize_cdr(tf2msg,msgtype)
            writer.write(connection_writer_static,timestamp,message)
            