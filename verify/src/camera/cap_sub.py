#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import rospkg

# def find_package_path(package_name):
#     rospack = rospkg.RosPack()
#     try:
#         package_path = rospack.get_path(package_name)
#         rospy.loginfo(package_path)
#         # print(f"The path to '{package_name}' is: {package_path}")
#         rospy.loginfo(package_path)
#         rospy.loginfo("Packge path saved")
#         return package_path
#     except rospkg.ResourceNotFound:
#         # print(f"Error: Package '{package_name}' not found.")
#         rospy.loginfo("Package not found")
#         pass



def image_callback(msg):
    try:
        # Convert ROS Image message to OpenCV format
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

        # Display the image (you can replace this with your processing logic)
        cv2.imshow("Camera Image", cv_image)
        cv2.waitKey(1)  # Wait for a short time to update the display
        # rospy.loginfo(path)
        # cv2.imwrite(path, cv_image)
        
        
    except CvBridgeError as e:
        rospy.logerr("Error converting ROS Image to OpenCV format: %s", str(e))


def image_subscriber():
    # Initialize the ROS node
    rospy.init_node('image_subscriber', anonymous=True)

    # Subscribe to the camera image topic
    
    rospy.Subscriber('/camera_image', Image, image_callback)

    # Spin to keep the script from exiting
    rospy.spin()

if __name__ == '__main__':
    try:
        # path = find_package_path('verify')
        # path = path+'/database/img.jpg'
        image_subscriber()
    except rospy.ROSInterruptException:
        pass