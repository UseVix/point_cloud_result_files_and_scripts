#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 18:14:20 2025

@author: risalinux
"""
from rosbags.rosbag2 import Reader
from rosbags.rosbag2 import Writer
pathtocompressed='/media/risalinux/Seagate Basic/Dataset/NewerCollege/quad_easy/bag/ros2_quad_easy/draco_ros2/draco_ros2_0.db3'
pathtobase='/media/risalinux/Seagate\ Basic/Dataset/NewerCollege/quad_easy/bag/ros2_quad_easy/ros2_output/ros2_output_0.mcap'
with Reader(pathtobase) as reader:
    for connection in reader.connections:
        point_connection=connection
        if point_connection.topic == 'sensor_msgs/msg/PointCloud2':
            break
    with Writer(pathtobase) as writer:
        for (connection, t, msg),(u,timestamp,i) in zip(Reader(pathtocompressed).messages(),reader.messages([point_connection])):
            writer.write(connection,timestamp,msg)
        
