for ((i = 0 ; i < 11 ; i = i + 3 ));
do
	for ((j = 0 ; j < 11 ; j = j + 3 ));
	do
		for ((k = 12 ; k < 21 ; k = k + 2 ));
		do
			/root/Datasets/NewerCollege/quad_easy/bag/compression_placer.sh /root/Datasets/NewerCollege/quad_easy/bag/quad_easy.bag draco /os_cloud_node/points 0.2 $i $j $k
		done
	done
done
