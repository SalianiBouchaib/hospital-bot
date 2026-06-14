import os
import tempfile

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    bringup_share = get_package_share_directory("hospital_robot_bringup")
    description_share = get_package_share_directory("hospital_robot_description")
    world = os.path.join(bringup_share, "worlds", "hospital.world")
    xacro_file = os.path.join(description_share, "urdf", "robot.urdf.xacro")
    robot_description = xacro.process_file(xacro_file).toxml()

    urdf_file = os.path.join(tempfile.gettempdir(), "hospital_robot_spawn.urdf")
    with open(urdf_file, "w", encoding="utf-8") as urdf_out:
        urdf_out.write(robot_description)

    return LaunchDescription(
        [
            ExecuteProcess(
                cmd=[
                    "gazebo",
                    "--verbose",
                    world,
                    "-s",
                    "libgazebo_ros_init.so",
                    "-s",
                    "libgazebo_ros_factory.so",
                ],
                output="screen",
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[{"use_sim_time": True, "robot_description": robot_description}],
            ),
            TimerAction(
                period=4.0,
                actions=[
                    Node(
                        package="gazebo_ros",
                        executable="spawn_entity.py",
                        arguments=[
                            "-entity",
                            "hospital_robot",
                            "-file",
                            urdf_file,
                            "-timeout",
                            "120.0",
                            "-unpause",
                            "-x",
                            "0.0",
                            "-y",
                            "0.0",
                            "-z",
                            "0.05",
                        ],
                        output="screen",
                    )
                ],
            ),
        ]
    )
