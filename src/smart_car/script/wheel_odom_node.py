#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from smartcar_msgs.msg import Status
from geometry_msgs.msg import Twist, TransformStamped, Quaternion
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster
import math
import numpy as np
class WheelOdomNode(Node):
    def __init__(self):
        super().__init__('wheel_odom_node')
        self.subscription = self.create_subscription(
            Status,
            '/smart_car/vehicle_status',
            self.listener_callback,
            10)
        self.cmd_vel_subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10)
        self.publisher = self.create_publisher(Odometry, '/smart_car/wheel/odom', 10)
        self.tf_broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.last_time = self.get_clock().now()
        self.position_x = 0.0
        self.position_y = 0.0
        self.theta = 0.0

        # Initialize attributes
        self.linear_velocity = 0.0
        self.angular_velocity = 0.0

    def listener_callback(self, msg:Status):
        self.get_logger().info(f"Received Status: steering_angle_rad={msg.steering_angle_rad}, engine_speed_rpm={msg.engine_speed_rpm}")
        self.linear_velocity = msg.engine_speed_rpm * 3.1415926535897932* 0.064 /60
        self.angular_velocity = self.linear_velocity *  np.tan(msg.steering_angle_rad) / 0.257
    def cmd_vel_callback(self, msg):
        # self.linear_velocity = msg.linear.x if not math.isnan(msg.linear.x) else 0.0
        # self.angular_velocity = msg.angular.z if not math.isnan(msg.angular.z) else 0.0
        self.get_logger().info(f"Received CmdVel: linear_velocity={self.linear_velocity}, angular_velocity={self.angular_velocity}")

    def timer_callback(self):
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9
        self.last_time = current_time

        if dt > 0:  # Avoid division by zero
            # Update position based on velocity commands
            self.position_x += self.linear_velocity * math.cos(self.theta) * dt
            self.position_y += self.linear_velocity * math.sin(self.theta) * dt
            self.theta += self.angular_velocity * dt
            self.theta = self.theta % (2 * math.pi)  # Wrap angle to [0, 2pi]

            # Create Odometry message
            odom_msg = Odometry()
            odom_msg.header.stamp = current_time.to_msg()
            odom_msg.header.frame_id = 'odom'
            odom_msg.child_frame_id = 'base_link'
            
            odom_msg.pose.pose.position.x = self.position_x
            odom_msg.pose.pose.position.y = self.position_y
            odom_msg.pose.pose.position.z = 0.0
            
            quaternion = self.quaternion_from_euler(0, 0, self.theta)
            if not self.is_quaternion_valid(quaternion):
                self.get_logger().error("Invalid quaternion detected!")
                return
            
            odom_msg.pose.pose.orientation = quaternion
            odom_msg.twist.twist.linear.x = self.linear_velocity
            odom_msg.twist.twist.angular.z = self.angular_velocity
            
            # Set covariance values
            odom_msg.pose.covariance = [
                0.1, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.1, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.01, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.01, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.01, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.1
            ]

            odom_msg.twist.covariance = [
                0.1, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.1, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.01, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.01, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.01, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.1
            ]

            self.publisher.publish(odom_msg)

            # Broadcast the transform
            t = TransformStamped()
            t.header.stamp = current_time.to_msg()
            t.header.frame_id = 'odom'
            t.child_frame_id = 'base_link'
            t.transform.translation.x = self.position_x
            t.transform.translation.y = self.position_y
            t.transform.translation.z = 0.0
            t.transform.rotation = quaternion

            # self.tf_broadcaster.sendTransform(t)

            self.get_logger().info(f"Published Odom: position_x={self.position_x}, position_y={self.position_y}, theta={self.theta}")

    def quaternion_from_euler(self, roll, pitch, yaw):
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        return Quaternion(x=qx, y=qy, z=qz, w=qw)

    def is_quaternion_valid(self, quaternion):
        return not (math.isnan(quaternion.x) or math.isnan(quaternion.y) or math.isnan(quaternion.z) or math.isnan(quaternion.w))

def main(args=None):
    rclpy.init(args=args)
    node = WheelOdomNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
