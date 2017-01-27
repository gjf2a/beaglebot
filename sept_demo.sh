#!/bin/bash

# Set up the motors
LEFT_FORWARD=66
RIGHT_FORWARD=67
LEFT_REVERSE=69
RIGHT_REVERSE=68
cd /sys/class/gpio
echo $LEFT_FORWARD  > export
echo $RIGHT_FORWARD > export
echo $LEFT_REVERSE  > export
echo $RIGHT_REVERSE > export

cd gpio$LEFT_FORWARD
echo out > direction
cd ../gpio$RIGHT_FORWARD
echo out > direction
cd ../gpio$LEFT_REVERSE
echo out > direction
cd ../gpio$RIGHT_REVERSE
echo out > direction
cd ..


# Set up the IR

# Debian 3.8.13
# 
# IIO
# echo cape-bone-iio > /sys/devices/bone_capemgr.9/slots

AIN=AIN1
AIN_PATH=/sys/devices/ocp.3/helper.15/$AIN

# Ubuntu
#AIN=1_raw
#AIN_PATH=/sys/bus/iio/devices/iio\:device0/in_voltage$AIN

MIN_SAFE=1250

cd gpio$LEFT_FORWARD
echo 1 > value
cd ..

COUNTER=100
while [ $COUNTER -gt 0 ]; do
    IR=`cat $AIN_PATH`
    echo $IR
    if [ $IR -gt $MIN_SAFE ]; then
        cd gpio$RIGHT_REVERSE
        echo 0 > value
        cd ../gpio$RIGHT_FORWARD
        echo 1 > value
        cd ..
	echo 'Straight'
    else 
        cd gpio$RIGHT_FORWARD
        echo 0 > value
        cd ../gpio$RIGHT_REVERSE
        echo 1 > value
        cd ..
	echo 'Turn'
    fi 
    let COUNTER=COUNTER-1
done

cd gpio$LEFT_FORWARD
echo 0 > value
cd ../gpio$RIGHT_FORWARD
echo 0 > value
cd ../gpio$LEFT_REVERSE
echo 0 > value
cd ../gpio$RIGHT_REVERSE
echo 0 > value
cd ..
echo $LEFT_FORWARD  > unexport
echo $RIGHT_FORWARD > unexport
echo $LEFT_REVERSE  > unexport
echo $RIGHT_REVERSE > unexport
