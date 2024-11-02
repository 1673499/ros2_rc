from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

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

    return LaunchDescription([
        # Include the Gazebo launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gazebo_launch_file)
        )
    ])

if __name__ == '__main__':
    generate_launch_description()
