from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    params = PathJoinSubstitution(
        [FindPackageShare("hospital_robot_control"), "config", "control_params.yaml"]
    )
    return LaunchDescription(
        [
            Node(
                package="hospital_robot_control",
                executable="control_node",
                name="control_node",
                output="screen",
                parameters=[params],
            )
        ]
    )
