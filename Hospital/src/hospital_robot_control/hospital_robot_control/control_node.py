import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Path
from rclpy.node import Node


class ControlNode(Node):
    def __init__(self) -> None:
        super().__init__("control_node")
        self.declare_parameter("path_topic", "/plan")
        self.declare_parameter("cmd_vel_topic", "/cmd_vel")
        self.declare_parameter("max_linear_speed", 0.4)
        self.declare_parameter("max_angular_speed", 1.0)

        path_topic = self.get_parameter("path_topic").get_parameter_value().string_value
        cmd_vel_topic = self.get_parameter("cmd_vel_topic").get_parameter_value().string_value
        self.max_linear = self.get_parameter("max_linear_speed").get_parameter_value().double_value
        self.max_angular = self.get_parameter("max_angular_speed").get_parameter_value().double_value

        self.cmd_pub = self.create_publisher(Twist, cmd_vel_topic, 10)
        self.path_sub = self.create_subscription(Path, path_topic, self.path_callback, 10)

    def path_callback(self, msg: Path) -> None:
        cmd = Twist()
        if len(msg.poses) > 1:
            cmd.linear.x = self.max_linear
            cmd.angular.z = 0.0
        elif len(msg.poses) == 1:
            cmd.linear.x = 0.1
            cmd.angular.z = 0.0
        else:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
        cmd.linear.x = max(min(cmd.linear.x, self.max_linear), -self.max_linear)
        cmd.angular.z = max(min(cmd.angular.z, self.max_angular), -self.max_angular)
        self.cmd_pub.publish(cmd)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = ControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
