#ros2 bag info draco_ros2_0_0_12/ | grep "/os_cloud_node/points/draco_" | cut -d" " -f4 | while read -r line; do
    # Do something with "$line"
#    kiss_icp_pipeline /media/risalinux/Seagate Basic/Dataset/NewerCollege/quad_easy/bag/ros2_quad_easy -t $line
#done
find -name "*draco_ros2_*" -type d -exec kiss_icp_pipeline {} \;
