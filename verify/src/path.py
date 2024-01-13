#!/usr/bin/env python

import rospy
import rospkg
import json

def find_package_path(package_name):
    rospack = rospkg.RosPack()
    try:
        package_path = rospack.get_path(package_name)
        rospy.loginfo(package_path)
        # print(f"The path to '{package_name}' is: {package_path}")
        rospy.loginfo(package_path)
        data = {
            "package_path": package_path
        }
        json_file_name = '/database/path.json'
        json_file_path = package_path+json_file_name
        with open(json_file_path,'w') as json_file:
            json.dump(data,json_file,indent=4)
        rospy.loginfo("Packge path saved")

    except rospkg.ResourceNotFound:
        # print(f"Error: Package '{package_name}' not found.")
        rospy.loginfo("Package not found")
        pass
    
if __name__ == '__main__':
    try:
        path = find_package_path('verify')
    except rospy.ROSInterruptException:
        pass