import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class StartupCmdVelTest(Node):
    def __init__(self) -> None:
        super().__init__("startup_cmd_vel_test")
        self.declare_parameter("linear_speed", 0.25)
        self.declare_parameter("duration_sec", 4.0)
        self.declare_parameter("publish_hz", 10.0)

        self.linear_speed = self.get_parameter("linear_speed").get_parameter_value().double_value
        duration_sec = self.get_parameter("duration_sec").get_parameter_value().double_value
        publish_hz = self.get_parameter("publish_hz").get_parameter_value().double_value

        self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.pulses = int(max(duration_sec * publish_hz, 1.0))
        self.sent = 0
        self.timer = self.create_timer(1.0 / max(publish_hz, 1.0), self.publish_cmd)
        self.get_logger().info(
            f"Driving forward at {self.linear_speed} m/s for {duration_sec:.1f}s to verify Gazebo motion."
        )

    def publish_cmd(self) -> None:
        msg = Twist()
        if self.sent < self.pulses:
            msg.linear.x = self.linear_speed
            self.cmd_pub.publish(msg)
        self.sent += 1
        if self.sent > self.pulses:
            stop = Twist()
            self.cmd_pub.publish(stop)
            self.timer.cancel()
            self.get_logger().info("Startup motion test finished.")


def main(args=None) -> None:
    rclpy.init(args=args)
    node = StartupCmdVelTest()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
