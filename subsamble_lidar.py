import rosbag
import numpy as np
import rospy
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2, PointField

# OS LIDAR vertical angle mapping (example)
def get_ring_angles(lidar_type="OS-128"):
    """
    Returns approximate vertical angles for each ring.
    Adjust based on your specific OS model.
    """
    if lidar_type == "OS-128":
        return np.linspace(-45, 45, 128)  # Approximate OS-128 angles
    elif lidar_type == "OS-64":
        return np.linspace(-30, 30, 64)  # Approximate OS-64 angles
    else:
        raise ValueError("Unknown LIDAR type")

# VLP-16 angles
VLP16_ANGLES = np.array([15, 13, 11, 9, 7, 5, 3, 1, -1, -3, -5, -7, -9, -11, -13, -15])

def filter_pointcloud_for_vlp16(msg, lidar_type="OS-128"):
    """
    Filters PointCloud2 data to simulate a VLP-16 by selecting points within ±15°.
    """
    # Convert PointCloud2 to NumPy array
    pc_data = list(pc2.read_points(msg, field_names=["x", "y", "z", "intensity", "t", "reflectivity", "ring", "ambient", "range"], skip_nans=True))
    pc_array = np.array(pc_data, dtype=np.float32)

    # Get vertical angles for the OS LiDAR
    ring_angles = get_ring_angles(lidar_type)
    
    # Find OS rings that best match the VLP-16 rings
    selected_rings = []
    for vlp_angle in VLP16_ANGLES:
        closest_ring = np.argmin(np.abs(ring_angles - vlp_angle))  # Find closest OS ring
        selected_rings.append(closest_ring)

    selected_rings = np.unique(selected_rings)  # Ensure unique selection

    # Filter points that belong to selected VLP-16 rings
    filtered_points = np.array([p for p in pc_array if int(p[6]) in selected_rings], dtype=np.float32)
    filtered_points = filtered_points[:, [0, 1, 2, 3, 6]]  # Keep only x, y, z, intensity, and ring
#    filtered_points[:, 4] = filtered_points[:, 4].astype(np.int32)  # Convert ring to INT32
#    filtered_points[:, 4] = int(filtered_points[:, 4]) # Convert ring to INT32
#    filtered_points[:, 4] = filtered_points[:, 4].astype(np.int32)  # Convert each ring to INT32


    # Define new PointCloud2 message
    fields = [
        PointField(name="x", offset=0, datatype=PointField.FLOAT32, count=1),
        PointField(name="y", offset=4, datatype=PointField.FLOAT32, count=1),
        PointField(name="z", offset=8, datatype=PointField.FLOAT32, count=1),
        PointField(name="intensity", offset=12, datatype=PointField.FLOAT32, count=1),
        PointField(name="ring", offset=16, datatype=PointField.FLOAT32, count=1),
    ]

    # Create new PointCloud2 message
    filtered_pc_msg = pc2.create_cloud(msg.header, fields, filtered_points)
    return filtered_pc_msg

def process_rosbag(input_bag, output_bag, topic_name, lidar_type="OS-128"):
    """
    Reads a ROS bag, filters the PointCloud2 data to simulate a VLP-16, and writes to a new bag.
    """
    with rosbag.Bag(output_bag, 'w') as outbag:
        with rosbag.Bag(input_bag, 'r') as inbag:
            for topic, msg, t in inbag.read_messages(topics=[topic_name]):
                if topic == topic_name:
                    filtered_pc = filter_pointcloud_for_vlp16(msg, lidar_type)
                    outbag.write(topic, filtered_pc, t)

# Example usage
if __name__ == "__main__":
    input_bag_file = "quad_easy.bag"  # Path to input ROS bag
    output_bag_file = "vlp16_simulated.bag"  # Output bag
    topic_name = "/os_cloud_node/points"  # PointCloud2 topic

    process_rosbag(input_bag_file, output_bag_file, topic_name, lidar_type="OS-128")
    print(f"Filtered data saved to {output_bag_file}")
