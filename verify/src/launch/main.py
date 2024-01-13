#!/usr/bin/env python3

import rospy
import subprocess

package_path = "/home/jetson/sanket_ws/src/verify"

if __name__ == '__main__':
    try:
        rospy.init_node('main')
        paths = ['/src/camera/move_and_cap.py',
                 '/src/puzzle_algo/Puzzle_algo.py',
                 '/src/convertor/path_to_joint_vars.py']

     
        for sub_path in paths:
            path = package_path+sub_path    
            subprocess.run(['python',path])
            
        path = package_path+"/src/joint_var_pub.py"    
        subprocess.run(['python3',path])
        
        rospy.loginfo("finished")
        
        
    except:
        # rospy.loginfo("Capture Failed")
        pass