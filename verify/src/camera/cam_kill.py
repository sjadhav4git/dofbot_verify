#!/usr/bin/env python3

import cv2
import subprocess
import rospy

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

if __name__ == '__main__':
    try:
        # Release camera first
        camera_release()
        
        
    except rospy.ROSInterruptException:
        pass
