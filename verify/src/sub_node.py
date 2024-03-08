#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def callback(data):
    # Callback function to handle incoming messages
    rospy.loginfo("Received: %s", data.data)

def subscriber_node():
    # Initialize the ROS node
    rospy.init_node('subscriber_node', anonymous=True)

    # Create a subscriber for the "chatter" topic
    rospy.Subscriber('chatter', String, callback)

    # Spin to keep the script alive and receive messages
    rospy.spin()

if __name__ == '__main__':
    try:
        subscriber_node()
    except rospy.ROSInterruptException:
        pass