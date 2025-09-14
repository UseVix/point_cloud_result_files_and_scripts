for ((i = 0 ; i < 11 ; i = i + 3 ));
do
	for ((j = 0 ; j < 11 ; j = j + 3 ));
	do
		for ((k = 12 ; k < 21 ; k = k + 2 ));
		do
			echo Compression Speed $i
		        echo Decompression Speed $j
			echo Quantization bits $k
			ros2 run bag_reading_and_converting_cpp bag_draco_different_configs draco_ros2 draco_ros2_${i}_${j}_${k} draco $i $j $k
		done
	done
done
for ((i = 2 ; i < 7 ; i = i + 2 ));
do	
	cloudini_rosbag_converter -f ros2_output/ros2_output_0.mcap -o cloudini_bags/compressed_rosbag_${i}.mcap -c -r 0.$i
done
