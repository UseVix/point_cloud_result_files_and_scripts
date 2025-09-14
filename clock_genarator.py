#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 23:36:12 2025

@author: risalinux
"""

#!/usr/bin/env python3
import sys
import rosbag2_py
from rosgraph_msgs.msg import Clock
from rclpy.serialization import serialize_message

def generate_clock_bag(input_bag: str, output_bag: str):
    # Setup reader
    reader = rosbag2_py.SequentialReader()
    storage_options = rosbag2_py.StorageOptions(uri=input_bag, storage_id='sqlite3')
    converter_options = rosbag2_py.ConverterOptions('', '')
    reader.open(storage_options, converter_options)

    # Setup writer
    writer = rosbag2_py.SequentialWriter()
    storage_options_out = rosbag2_py.StorageOptions(uri=output_bag, storage_id='sqlite3')
    writer.open(storage_options_out, converter_options)

    # Add only the /clock topic to the new bag
    writer.create_topic(
        rosbag2_py.TopicMetadata(
            name="/clock",
            type="rosgraph_msgs/msg/Clock",
            serialization_format="cdr"
        )
    )

    # Iterate through messages in input bag and create clock messages
    while reader.has_next():
        topic, data, t = reader.read_next()

        # Convert nanoseconds to Clock message
        clock_msg = Clock()
        clock_msg.clock.sec = t // 1_000_000_000
        clock_msg.clock.nanosec = t % 1_000_000_000

        writer.write("/clock", serialize_message(clock_msg), t)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: generate_clock_bag.py <input_bag> <output_bag>")
        sys.exit(1)

    input_bag = sys.argv[1]
    output_bag = sys.argv[2]

    generate_clock_bag(input_bag, output_bag)
