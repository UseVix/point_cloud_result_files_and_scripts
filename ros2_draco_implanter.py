#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 23:45:51 2025

@author: risalinux
"""

#sys.path.append("/opt/ros/humble/lib/python3.10/site-packages")
#sys.path.append("/home/risalinux/compression_ws/install/point_cloud_transport_py/local/lib/python3.10/dist-packages/point_cloud_transport_py/")
#sys.path.append("/home/risalinux/compression_ws/install/lib/python3.10/site-packages")
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

from point_cloud_transport_py import PointCloudCodec
from rosbags.rosbag2 import Reader
from rosbags.rosbag2 import Writer
#from point_cloud_transport_py.common import PointCloudCodec
#from point_cloud_transport_py import common
from point_cloud_transport_py import PointCloudCodec
from sensor_msgs.msg import PointCloud2
from point_cloud_interfaces.msg import CompressedPointCloud2
import sys
from rosbags.typesys import Stores, get_types_from_msg, get_typestore
from pathlib import Path
from rclpy.serialization import deserialize_message, serialize_message

from rosbags.serde import serialize_cdr, deserialize_cdr, ros1_to_cdr
from rclpy_message_converter import message_converter

pathtobase='/media/risalinux/Seagate\ Basic/Dataset/NewerCollege/quad_easy/bag/ros2_quad_easy/ros2_output/ros2_output_0.mcap'
def guess_msgtype(path: Path) -> str:
    """Guess message type name from path."""
    name = path.relative_to(path.parents[2]).with_suffix('')
    if 'msg' not in name.parts:
        name = name.parent / 'msg' / name.name
    return str(name)


typestore = get_typestore(Stores.ROS2_HUMBLE)
add_types = {}

for pathstr in ['/home/risalinux/compression_ws/src/point_cloud_transport_plugins/point_cloud_interfaces/msg/CompressedPointCloud2.msg']:
    msgpath = Path(pathstr)
    msgdef = msgpath.read_text(encoding='utf-8')
    add_types.update(get_types_from_msg(msgdef, guess_msgtype(msgpath)))

typestore.register(add_types)

def main():
    codec=PointCloudCodec()
    pathtobase=sys.argv[1]
    compression_plugin=sys.argv[2]
    pathtonew=sys.argv[3]
    #typestore = get_typestore(Stores.ROS2_HUMBLE)
    with Reader(pathtobase) as reader,Writer(pathtonew) as writer:
        for connection_reader in reader.connections:
            if connection_reader.msgtype == 'sensor_msgs/msg/PointCloud2':
                topic = connection_reader.topic+'/draco'
                msgtype = 'point_cloud_interfaces/msg/CompressedPointCloud2'
                connection_writer = writer.add_connection(topic, msgtype, typestore=typestore)
                for (con, timestamp, msg) in reader.messages(connections=[connection_reader]):
                    #writer.write(connection_writer,timestamp,msg)
                    """
                    compressed, err = codec.encode(msg, compression_plugin)
                    msg_ser= serialize_message(compressed, CompressedPointCloud2)
                    writer.write(connection_writer,timestamp,msg_ser)
                    """
                    # Convert rosbags msg → raw CDR bytes
                    # rosbags msg -> raw CDR
                    #cdr_des = typestore.deserialize_cdr(msg, connection_reader.msgtype)
                    # raw CDR -> ROS2 PointCloud2 (real message, with _TYPE_SUPPORT)
                    #pc2_msg = message_converter.convert_dictionary_to_ros_message(PointCloud2,convert_all_to_dicts(cdr_des.__dict__))
                    #ser_msg = serialize_message(pc2_msg)
                    compressed, err = codec.encode(compression_plugin,msg.decode('latin-1'))

                    

                    # Serialize compressed message for writer
                    deser_msg = deserialize_message(compressed,PointCloud2)
                    writer.write(connection_writer, timestamp, deser_msg)
            else:
                pass
                """
                connection_writer = writer.add_connection(connection_reader.topic, connection_reader.msgtype, typestore=typestore)
                for (con, timestamp, msg) in reader.messages(connections=[connection_reader]):
                    writer.write(connection_writer,timestamp,msg)
                """
            """
            if con.msgtype=='sensor_msgs/msg/PointCloud2':
                msgc = deserialize_message(msg, PointCloud2)
                compressed, err = codec.encode(msgc, compression_plugin)
                con.msgtype='point_cloud_interfaces/msg/CompressedPointCloud2'
                writer.write(con,timestamp,compressed)
            """

if __name__ == '__main__':
    main()
