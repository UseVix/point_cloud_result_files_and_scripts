find -name "*draco_ros2_*" -type d -exec ros2 bag info {} \; | grep -E "Files|Bag size" >> saved_sizes.txt
find -name "*only_lidar_packets*" -type d -exec ros2 bag info {} \; | grep -E "Files|Bag size" >> saved_sizes.txt
