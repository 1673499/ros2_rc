from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import xacro

def generate_launch_description():
    # Set the GAZEBO_MODEL_PATH environment variable
    gazebo_model_path = os.environ.get('GAZEBO_MODEL_PATH', '')
    new_model_path = os.path.join(get_package_share_directory('smart_car'), 'world')
    os.environ['GAZEBO_MODEL_PATH'] = f"{gazebo_model_path}:{new_model_path}"
    print(f"GAZEBO_MODEL_PATH: {os.environ['GAZEBO_MODEL_PATH']}")

    # Path to the Gazebo launch file
    gazebo_launch_file = os.path.join(
        get_package_share_directory('gazebo_ros'),
        'launch',
        'gazebo.launch.py'
    )
    print(f"Gazebo launch file path: {gazebo_launch_file}")

    # Path to your world file
    world_file_path = os.path.join(
        get_package_share_directory('smart_car'),
        'world',
        'smalltown.world'
    )
    print(f"World file path: {world_file_path}")

    # Get the path to the URDF file
    urdf_file = os.path.join(
        get_package_share_directory('smart_car'),
        'urdf',
        'smartcar.urdf.xacro'
    )

    # Process the xacro file
    robot_description_config = xacro.process_file(urdf_file)
    robot_description = {'robot_description': robot_description_config.toxml()}

    return LaunchDescription([
        # Include the Gazebo launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gazebo_launch_file),
            launch_arguments={'world': world_file_path}.items()
        ),
        # Node to publish robot state
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[robot_description]
        ),
        # Node to publish joint states
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen'
        ),
        # Spawn the robot entity into the Gazebo world
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'smart_car', '-topic', 'robot_description'],
            output='screen',
        ),
        # Add teleop_twist_keyboard node
        Node(
            package='teleop_twist_keyboard',
            executable='teleop_twist_keyboard',
            name='teleop_twist_keyboard',
            output='screen',
            remappings=[('/cmd_vel', '/cmd_vel')]
        )
    ])

if __name__ == '__main__':
    generate_launch_description()
