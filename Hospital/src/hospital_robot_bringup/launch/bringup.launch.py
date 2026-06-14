from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    simulation = PathJoinSubstitution(
        [FindPackageShare("hospital_robot_bringup"), "launch", "simulation.launch.py"]
    )
    navigation = PathJoinSubstitution(
        [FindPackageShare("hospital_robot_navigation"), "launch", "navigation.launch.py"]
    )
    delivery = PathJoinSubstitution(
        [FindPackageShare("hospital_robot_delivery"), "launch", "delivery.launch.py"]
    )
    rviz_config = PathJoinSubstitution(
        [FindPackageShare("hospital_robot_bringup"), "rviz", "hospital.rviz"]
    )

    return LaunchDescription(
        [
            IncludeLaunchDescription(PythonLaunchDescriptionSource(simulation)),
            TimerAction(
                period=6.0,
                actions=[IncludeLaunchDescription(PythonLaunchDescriptionSource(navigation))],
            ),
            TimerAction(
                period=20.0,
                actions=[IncludeLaunchDescription(PythonLaunchDescriptionSource(delivery))],
            ),
            TimerAction(
                period=16.0,
                actions=[
                    Node(
                        package="rviz2",
                        executable="rviz2",
                        arguments=["-d", rviz_config],
                        output="screen",
                    )
                ],
            ),
        ]
    )
