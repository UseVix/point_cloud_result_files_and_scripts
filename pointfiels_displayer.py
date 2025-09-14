#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 12:00:46 2025

@author: risalinux
"""

from pathlib import Path
# from rclpy.serialization import deserialize_message
# from rosbags.rosbag1 import Reader
# import sys
# import os 
# os.environ["PATH"] = "/home/risalinux/compression_ws/install/cloudini_lib/bin:" + os.environ.get("PATH", "")
# path="/media/risalinux/Seagate Basic1/Dataset/NewerCollege/quad_easy/bag/ros2_quad_easy/draco_ros2"
# # Verify
# print(os.environ["PATH"].split(":"))
# for p in "/home/risalinux/compression_ws/build/pct_compressed_point_cloud_bag_placer:/home/risalinux/compression_ws/install/pct_compressed_point_cloud_bag_placer/lib/python3.10/site-packages:/home/risalinux/compression_ws/build/ros2bag_extensions:/home/risalinux/compression_ws/install/ros2bag_extensions/lib/python3.10/site-packages:/home/risalinux/compression_ws/install/rosbag2_py_wrapper/local/lib/python3.10/dist-packages:/home/risalinux/compression_ws/install/point_cloud_transport_py/local/lib/python3.10/dist-packages:/home/risalinux/compression_ws/install/point_cloud_interfaces/local/lib/python3.10/dist-packages:/opt/ros/humble/lib/python3.10/site-packages:/opt/ros/humble/local/lib/python3.10/dist-packages/usr/lib/python310.zip:/usr/lib/python3.10:/usr/lib/python3.10/lib-dynload:/home/risalinux/.local/lib/python3.10/site-packages:/usr/local/lib/python3.10/dist-packages:/usr/lib/python3/dist-packages".split(":"):
#     if p not in sys.path:
#         sys.path.append(p)
# sys.path.insert(0, "/opt/ros/humble/lib/python3.10/site-packages")
# sys.path.insert(0, "/opt/ros/humble/local/lib/python3.10/dist-packages")
# sys.path.insert(0, "/home/risalinux/compression_ws/install/point_cloud_transport_py/local/lib/python3.10/dist-packages")
# sys.path.insert(0, "/home/risalinux/compression_ws/install/point_cloud_interfaces/local/lib/python3.10/dist-packages")
# sys.path.insert(0, "/home/risalinux/compression_ws/install/rclpy_message_converter/lib/python3.10/site-packages")
# sys.path = [p for p in sys.path if "src/point_cloud_transport" not in p]

# Example: find all .py files
# for path in Path("/media/risalinux/Seagate Basic/Dataset").rglob("*.bag"):
#     with Reader(path) as reader:
#         for connection_reader in reader.connections:
#             if connection_reader.msgtype == 'sensor_msgs/msg/PointCloud2':
#                 topic,msg,t=next(reader.messages(connections=[connection_reader]))
#                 dsmsg=deserialize_message(msg,'sensor_msgs/PointCloud2')
#                 print("#"*10)
#                 print(path+":")
#                 print(dsmsg.fields)
#                 print("#"*10)
import rosbag
liosamready={}
for path in Path("/root/Datasets").rglob("*.bag"):
    if path.stat().st_size<5000:
        continue
    print("#"*10)
    print(str(path)+":")
    with rosbag.Bag(path, 'r') as inbag:
        for point_topic in inbag.get_type_and_topic_info()[1]:
            if inbag.get_type_and_topic_info()[1][point_topic][0]=='sensor_msgs/PointCloud2':
                topic,msg,t=next(inbag.read_messages(topics=[point_topic]))
                print(msg.fields)
                print(type(msg.fields[0].name))
                print(type(msg.header))
                print(type(msg.data))
                print(msg.width)
                print(msg.height)
                print('-'*10)
                liosamready[str(path)]='"t"' in str(msg.fields) and '"ring"' in str(msg.fields)
                if msg.is_bigendian:
                    strendian="big"
                else:
                    strendian="little"
                for x in msg.fields:
                    if x.name=="t":
                        offset=x.offset
                if liosamready[str(path)]:
                    for x in range(10):
                        i=x+1
                        print(int.from_bytes(msg.data[i*offset:i*offset+4],strendian,signed=False))
                print("#"*10)
print(liosamready)
                
