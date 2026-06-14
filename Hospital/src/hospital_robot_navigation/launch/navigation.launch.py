from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    nav2_launch = PathJoinSubstitution(
        [FindPackageShare("nav2_bringup"), "launch", "bringup_launch.py"]
    )
    map_yaml = PathJoinSubstitution(
        [FindPackageShare("hospital_robot_navigation"), "config", "map.yaml"]
    )
    params_yaml = PathJoinSubstitution(
        [FindPackageShare("hospital_robot_navigation"), "config", "nav2_params.yaml"]
    )

    return LaunchDescription(
        [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(nav2_launch),
                launch_arguments={
                    "map": map_yaml,
                    "use_sim_time": "true",
                    "autostart": "true",
                    "use_composition": "False",
                    "use_velocity_smoother": "True",
                    "params_file": params_yaml,
                }.items(),
            ),
        ]
    )
