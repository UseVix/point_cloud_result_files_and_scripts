rosbag record /out -O ${2}_ES:${5}_DS:${6}_QP:${7} &
PID=$!
rosrun point_cloud_transport republish raw $2 in:=$3 out:=/out_${2}_ES:${5}_DS:${6}_QP:${7} &
PID0=$!
rosparam set /out_${2}_ES:${5}_DS:${6}_QP:${7}/draco/encode_speed $5
rosparam set /out_${2}_ES:${5}_DS:${6}_QP:${7}/draco/decode_speed $6
rosparam set /out_${2}_ES:${5}_DS:${6}_QP:${7}/draco/quantization_POSITION $7
rosbag play $1 -r $4
kill -2 $PID
kill -2 $PID0

