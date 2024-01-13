#!/usr/bin/env python3

import rospy
import subprocess

package_path = "/home/jetson/sanket_ws/src/verify"

if __name__ == '__main__':
    try:
        rospy.init_node("image_publisher")
        path = package_path+'/launch/sub_launch/camera_repair.launch'
        subprocess.run(['roslaunch',path])
        
        # rospy.sleep(5)
        # rospy.loginfo()
        # rospy.loginfo("=============================================")
        
        path = package_path+'/launch/sub_launch/camera_launch.launch'
        subprocess.run(['roslaunch',path])
        
        rospy.loginfo("capture and save successful")
    except:
        rospy.loginfo("Capture Failed")
        pass