#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from smartcar_msgs.msg import Status
from sensor_msgs.msg import JointState
import math

class JointStatePublisher(Node):
    def __init__(self):
        super().__init__('joint_state_publisher')
        self.declare_parameter('front_wheel_x', 0.5)
        self.declare_parameter('back_wheel_x', -0.5)
        self.declare_parameter('left_wheel_y', 0.3)
        self.declare_parameter('right_wheel_y', -0.3)

        self.front_wheel_x = self.get_parameter('front_wheel_x').value
        self.back_wheel_x = self.get_parameter('back_wheel_x').value
        self.left_wheel_y = self.get_parameter('left_wheel_y').value
        self.right_wheel_y = self.get_parameter('right_wheel_y').value

        self.subscription = self.create_subscription(
            Status,
            '/smart_car/vehicle_status',
            self.listener_callback,
            10)
        self.joint_state_publisher = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.steering_angle_rad = 0.0
        self.engine_speed_rpm = 0

    def listener_callback(self, msg):
        self.steering_angle_rad = msg.steering_angle_rad
        self.engine_speed_rpm = msg.engine_speed_rpm

    def timer_callback(self):
        # Calculate wheel rotation in radians per second
        wheel_rotation = (self.engine_speed_rpm / 60.0) * 2 * math.pi

        # Create JointState message
        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = [
            'front_left_wheel_joint', 'front_right_wheel_joint',
            'back_left_wheel_joint', 'back_right_wheel_joint',
            'front_left_wheel_steer_joint', 'front_right_wheel_steer_joint'
        ]
        joint_state.position = [
            wheel_rotation, wheel_rotation,
            wheel_rotation, wheel_rotation,
            self.steering_angle_rad, self.steering_angle_rad
        ]
        joint_state.velocity = [
            float(self.engine_speed_rpm), float(self.engine_speed_rpm),
            float(self.engine_speed_rpm), float(self.engine_speed_rpm),
            0.0, 0.0
        ]

        # Publish JointState message
        self.joint_state_publisher.publish(joint_state)

def main(args=None):
    rclpy.init(args=args)
    node = JointStatePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
