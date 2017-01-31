#!/usr/bin/env python
import roslib; roslib.load_manifest('perception')
from perception.srv import *
from move_base_msgs.msg import MoveBaseGoal
import rospy
import tf
import math

def generate_d3_points(req):
    rospy.logdebug('Got a request')

    tf_list = tf.TransformListener()
    trans = None
    rot = None
    radius = 1

    while not (trans and rot):
        try:
            (trans, rot) = tf_list.lookupTransform('/map', '/base_link',
                                                   rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

    dest = [MoveBaseGoal()] * (req.points)
    for i, p in enumerate(dest):
        p.target_pose.header.frame_id = 'map'

        p.target_pose.pose.position.x = math.cos(2 * math.pi / req.points * i) * radius + trans[0]
        p.target_pose.pose.position.y = math.sin(2 * math.pi / req.points * i) * radius + trans[1]
        p.target_pose.pose.position.z = 0

        p.target_pose.pose.orientation.x = 0
        p.target_pose.pose.orientation.y = 0
        p.target_pose.pose.orientation.z = 0
        p.target_pose.pose.orientation.w = 1

    rospy.logdebug('Responding with: ', dest)
    return D3PointsResponse(destinations=dest)

def D3Points_server():
    rospy.init_node('d3_points_server')

    s = rospy.Service('d3_points', D3Points, generate_d3_points)
    rospy.loginfo("Ready to generate D3 points.")

    rospy.spin()

if __name__ == "__main__":
    D3Points_server()
