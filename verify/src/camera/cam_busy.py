#!/usr/bin/env python3

import cv2
import subprocess
import rospy

def cam_busy():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imshow('img',frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        
        cam_busy()
        
    except rospy.ROSInterruptException:
        pass
