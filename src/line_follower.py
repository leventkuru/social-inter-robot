#!/usr/bin/env python


#This Program is tested on Gazebo Simulator
#This script uses the cv_bridge package to convert images coming on the topic
#sensor_msgs/Image to OpenCV messages and then convert their colors from RGB to HSV
#then apply a threshold for hues near the color yellow to obtain the binary image
#to be able to see only the yellow line and then follow that line
#It uses an approach called proportional and simply means

import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

class Follower:

        def __init__(self):


                self.bridge = cv_bridge.CvBridge()
                cv2.namedWindow("window", 1)

                self.image_sub = rospy.Subscriber('camera/rgb/image_raw',
                        Image, self.image_callback)

                self.cmd_vel_pub = rospy.Publisher('/cmd_vel',
                        Twist, queue_size=1)

                self.twist = Twist()

        def color_definer(self, image_hsv):


            blue_lower = numpy.array([110, 0, 0])
            blue_upper = numpy.array([130, 255, 255])
            blue_mask = cv2.inRange(image_hsv, blue_lower, blue_upper)
            blue_count = numpy.count_nonzero(blue_mask)
            if blue_count > 0:
                included = "blue"
                return included, blue_mask

            green_lower = numpy.array([36,0,0])
            green_upper = numpy.array([86,255,255])
            green_mask = cv2.inRange(image_hsv, green_lower, green_upper)
            green_count = numpy.count_nonzero(green_mask)
            if green_count > 0:
                included = "green"
                return included, green_mask

            # lower boundary RED color range values; Hue (0 - 10)
            lower1 = numpy.array([0, 100, 20])
            upper1 = numpy.array([10, 255, 255])
 
            # upper boundary RED color range values; Hue (160 - 180)
            lower2 = numpy.array([160,100,20])
            upper2 = numpy.array([179,255,255])
 
            lower_mask = cv2.inRange(image_hsv, lower1, upper1)
            upper_mask = cv2.inRange(image_hsv, lower2, upper2)
 
            red_full_mask = lower_mask + upper_mask
            red_count = numpy.count_nonzero(red_full_mask)
            if red_count > 0:
                included = "red"
                return included, red_full_mask


            yellow_lower = numpy.array([20, 10, 10])
            yellow_upper = numpy.array([30, 255, 250])
            yellow_mask = cv2.inRange(image_hsv, yellow_lower, yellow_upper)
            yellow_count = numpy.count_nonzero(yellow_mask)
            if yellow_count > 0:
                included = "yellow"
                return included, yellow_mask

            lower_yellow = numpy.array([ 10, 10, 10])
            upper_yellow = numpy.array([255, 255, 250])
            nc_mask = cv2.inRange(image_hsv, lower_yellow, upper_yellow)
            return "No color", nc_mask

            

        def image_callback(self, msg):
            

                image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                color, mask = self.color_definer(hsv)
                print(color)
                h, w, d = image.shape
                search_top = 3*h/4
                search_bot = 3*h/4 + 20
                mask[0:int(search_top), 0:w] = 0
                mask[int(search_bot):h, 0:w] = 0

                M = cv2.moments(mask)
                if color is not "No color":
                    if M['m00'] > 0:
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
                        err = cx - w/2
                        self.twist.linear.x = 0.3
                        self.twist.angular.z = -float(err) / 100
                        self.cmd_vel_pub.publish(self.twist)
                else:
                    self.twist.linear.x = 0.0
                    self.cmd_vel_pub.publish(self.twist)
                cv2.imshow("window", image)
                cv2.waitKey(3)

rospy.init_node('line_follower')
follower = Follower()
rospy.spin()