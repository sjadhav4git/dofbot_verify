#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import subprocess



def camera_release():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open camera")
        command = 'fuser /dev/video0'
        print(command)
        process = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout, stderr= process.communicate()
        print("std_out")
        pid = str(stdout.decode())
        print("process id : ",pid, " using camera")
        # print("\nstd_error")
        # print(stderr.decode())
        print('killing process ',pid)            
        command = 'kill -9'+pid
        print(command)
        process = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout, stderr= process.communicate()
        print(stdout.decode())
        cap.release()
        rospy.loginfo('camera_released')
    else:
        cap.release()
        print('camera_available')
        rospy.loginfo('Camera_available')
    

def capture_and_publish():
    
    # Initialize the ROS node
    rospy.init_node('image_publisher', anonymous=True)

    # Create a publisher for the image topic
    image_pub = rospy.Publisher('/camera_image', Image, queue_size=10)

    
    # Initialize the OpenCV capture object
    cap = cv2.VideoCapture(0)  # 0 is the default camera index, modify if needed

    # Initialize the CvBridge
    bridge = CvBridge()

    # Set the loop rate (in Hz)
    rate = rospy.Rate(30)  # 10 Hz

    while not rospy.is_shutdown():
        # Capture a frame from the camera
        ret, frame = cap.read()

        if ret:
            try:
                # Convert the OpenCV image to a ROS image message
                ros_image = bridge.cv2_to_imgmsg(frame, "bgr8")

                # Publish the image
                image_pub.publish(ros_image)
            except CvBridgeError as e:
                rospy.logerr("Error converting OpenCV image: %s", str(e))

        # Sleep to maintain the loop rate
        rate.sleep()

    # Release the camera when the node is shut down
    cap.release()


if __name__ == '__main__':
    try:
        # Release camera first
        # camera_release()
        capture_and_publish()
    except rospy.ROSInterruptException:
        pass
