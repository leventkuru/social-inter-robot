#!/usr/bin/env python


#This Program is tested on Gazebo Simulator
#This script uses the cv_bridge package to convert images coming on the topic
#sensor_msgs/Image to OpenCV messages and then convert their colors from RGB to HSV
#then apply a threshold for hues near the color yellow to obtain the binary image
#to be able to see only the yellow line and then follow that line
#It uses an approach called proportional and simply means

import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion
from math import atan2

x = 0.0
y = 0.0
theta = 0.0

def newOdom (msg):
    global x
    global y
    global theta

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y. rot_z, rot_w])

class Follower:

        def __init__(self):


                self.bridge = cv_bridge.CvBridge()
                cv2.namedWindow("window", 1)

                self.image_sub = rospy.Subscriber('camera/rgb/image_raw',
                        Image, self.image_callback)

                self.cmd_vel_pub = rospy.Publisher('/cmd_vel',
                        Twist, queue_size=1)

                self.twist = Twist()

        def image_callback(self, msg):
            

                image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                lower_yellow = numpy.array([ 10, 10, 10])
                upper_yellow = numpy.array([255, 255, 250])
                mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
                h, w, d = image.shape
                search_top = 3*h/4
                search_bot = 3*h/4 + 20
                mask[0:int(search_top), 0:w] = 0
                mask[int(search_bot):h, 0:w] = 0

                M = cv2.moments(mask)
                if M['m00'] > 0:
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
#The proportional controller is implemented in the following four lines which
#is reposible of linear scaling of an error to drive the control output.
                        err = cx - w/2
                        self.twist.linear.x = 0.2
                        self.twist.angular.z = -float(err) / 100
                        self.cmd_vel_pub.publish(self.twist)
                cv2.imshow("window", image)
                cv2.waitKey(3)

rospy.init_node('line_follower')
follower = Follower()
rospy.spin()