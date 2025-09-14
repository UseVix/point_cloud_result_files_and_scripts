#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 19:49:01 2025

@author: risalinux
"""
import sys
import os

def is_type_from_rosbags(obj):
    return obj.__class__.__module__[0:7]=='rosbags'
def convert_all_to_dicts(dict_to_convert):
    fieldstodelete=['__msgtype__','INT8','INT16','INT32','UINT8','UINT16','UINT32','FLOAT32','FLOAT64']
    for x in dict_to_convert:
        if is_type_from_rosbags(dict_to_convert[x]):
            dict_to_convert[x]=convert_all_to_dicts(dict_to_convert[x].__dict__)
        if type(dict_to_convert[x])==list:
            for i in range(len(dict_to_convert[x])):
                if is_type_from_rosbags(dict_to_convert[x][i]):
                    dict_to_convert[x][i]=convert_all_to_dicts(dict_to_convert[x][i].__dict__)
    for y in fieldstodelete:
        if y in dict_to_convert:
            dict_to_convert.pop(y)
    return dict_to_convert


# Prepend to PATH
os.environ["PATH"] = "/home/risalinux/compression_ws/install/cloudini_lib/bin:" + os.environ.get("PATH", "")
path="/media/risalinux/Seagate Basic1/Dataset/NewerCollege/quad_easy/bag/ros2_quad_easy/draco_ros2"
# Verify
print(os.environ["PATH"].split(":"))
for p in "/home/risalinux/compression_ws/build/pct_compressed_point_cloud_bag_placer:/home/risalinux/compression_ws/install/pct_compressed_point_cloud_bag_placer/lib/python3.10/site-packages:/home/risalinux/compression_ws/build/ros2bag_extensions:/home/risalinux/compression_ws/install/ros2bag_extensions/lib/python3.10/site-packages:/home/risalinux/compression_ws/install/rosbag2_py_wrapper/local/lib/python3.10/dist-packages:/home/risalinux/compression_ws/install/point_cloud_transport_py/local/lib/python3.10/dist-packages:/home/risalinux/compression_ws/install/point_cloud_interfaces/local/lib/python3.10/dist-packages:/opt/ros/humble/lib/python3.10/site-packages:/opt/ros/humble/local/lib/python3.10/dist-packages/usr/lib/python310.zip:/usr/lib/python3.10:/usr/lib/python3.10/lib-dynload:/home/risalinux/.local/lib/python3.10/site-packages:/usr/local/lib/python3.10/dist-packages:/usr/lib/python3/dist-packages".split(":"):
    if p not in sys.path:
        sys.path.append(p)
sys.path.insert(0, "/opt/ros/humble/lib/python3.10/site-packages")
sys.path.insert(0, "/opt/ros/humble/local/lib/python3.10/dist-packages")
sys.path.insert(0, "/home/risalinux/compression_ws/install/point_cloud_transport_py/local/lib/python3.10/dist-packages")
sys.path.insert(0, "/home/risalinux/compression_ws/install/point_cloud_interfaces/local/lib/python3.10/dist-packages")
sys.path.insert(0, "/home/risalinux/compression_ws/install/rclpy_message_converter/lib/python3.10/site-packages")
sys.path = [p for p in sys.path if "src/point_cloud_transport" not in p]
print(sys.path)
import point_cloud_transport_py
from rosbags.rosbag2 import Reader
from sensor_msgs.msg import PointCloud2
from rclpy.serialization import deserialize_message, serialize_message
codec = point_cloud_transport_py.PointCloudCodec()
with Reader(path) as reader:
    pc2=[]
    cpc2=[]
    for connection_reader in reader.connections:

        print(connection_reader.msgtype)
        if connection_reader.msgtype == 'sensor_msgs/msg/PointCloud2':
            for (con, timestamp, msg) in reader.messages(connections=[connection_reader]):
                pc2.append(timestamp)
                if len(pc2)>50:
                    break
        if connection_reader.msgtype == 'point_cloud_interfaces/msg/CompressedPointCloud2':
            for (con, timestamp, msg) in reader.messages(connections=[connection_reader]):
                cpc2.append(timestamp)
                if len(cpc2)>50:
                    break
                #writer.write(connection_writer,timestamp,msg)


