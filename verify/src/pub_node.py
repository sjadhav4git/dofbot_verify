#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def publisher_node():
    # Initialize the ROS node
    rospy.init_node('publisher_node', anonymous=True)

    # Create a publisher for the "chatter" topic
    pub = rospy.Publisher('chatter', String, queue_size=10)

    # Set the loop rate (in Hz)
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        # Publish a message to the "chatter" topic
        msg = "Hello, ROS!"
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        publisher_node()
    except rospy.ROSInterruptException:
        pass