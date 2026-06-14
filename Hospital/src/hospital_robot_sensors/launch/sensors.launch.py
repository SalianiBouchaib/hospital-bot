from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    params = PathJoinSubstitution(
        [FindPackageShare("hospital_robot_sensors"), "config", "sensor_params.yaml"]
    )
    return LaunchDescription(
        [
            Node(
                package="hospital_robot_sensors",
                executable="sensor_node",
                name="sensor_node",
                output="screen",
                parameters=[params],
            )
        ]
    )
