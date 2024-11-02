from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
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

    # Path to the Nav2 parameters file
    nav2_params_file = os.path.join(
        get_package_share_directory('smart_car'),
        'config',
        'nav2_params.yaml'
    )

    # Path to the RViz configuration file
    rviz_config_file = os.path.join(
        get_package_share_directory('smart_car'),
        'config',
        'rviz_config.rviz'
    )

    # Declare the map YAML file argument
    declare_map_yaml_cmd = DeclareLaunchArgument(
        'map',
        default_value=os.path.join(get_package_share_directory('smart_car'), 'map', 'smalltown_world.yaml'),
        description='Full path to map file to load'
    )

    return LaunchDescription([
        declare_map_yaml_cmd,
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
            parameters=[{'robot_description': xacro.process_file(
                os.path.join(get_package_share_directory('smart_car'), 'urdf', 'smartcar.urdf.xacro')).toxml()}]
        ),
        # Spawn the robot entity into the Gazebo world
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'smart_car', '-topic', 'robot_description'],
            output='screen',
        ),
        # Teleoperation node
        Node(
            package='teleop_twist_keyboard',
            executable='teleop_twist_keyboard',
            name='teleop_twist_keyboard',
            output='screen',
            remappings=[('/cmd_vel', '/cmd_vel')]
        ),
        # EKF node for localization
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[os.path.join(get_package_share_directory('smart_car'), 'config', 'ekf.yaml')]
        ),
        # Joint state publisher node
        Node(
            package='smart_car',
            executable='joint_state_publisher.py',
            name='joint_state_publisher',
            output='screen'
        ),
        # Wheel odometry node
        Node(
            package='smart_car',
            executable='wheel_odom_node.py',
            name='wheel_odom_node',
            output='screen'
        ),
        # Map server node
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[{'yaml_filename': os.path.join(get_package_share_directory('smart_car'), 'map', 'smalltown_world.yaml')}]
        ),
        # Include RViz launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('smart_car'), 'launch', 'rviz_launch.py')),
            launch_arguments={
                'namespace': 'smart_car',
                'use_namespace': 'true',
                'use_sim_time': 'true',
                'rviz_config': rviz_config_file,
            }.items()
        ),
        # Include bringup launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('smart_car'), 'launch', 'bringup_launch.py')),
            launch_arguments={
                'namespace': 'smart_car',
                'use_namespace': 'true',
                'slam': 'False',
                'map': os.path.join(get_package_share_directory('smart_car'), 'map', 'smalltown_world.yaml'),
                'use_sim_time': 'true',
                'params_file': nav2_params_file,
                'autostart': 'true',
                'use_composition': 'False',
                'use_respawn': 'false',
            }.items()
        )
    ])

if __name__ == '__main__':
    generate_launch_description()
