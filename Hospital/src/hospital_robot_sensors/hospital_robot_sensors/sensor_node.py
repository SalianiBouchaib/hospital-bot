import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class SensorNode(Node):
    def __init__(self) -> None:
        super().__init__("sensor_node")
        self.declare_parameter("scan_topic", "/scan")
        self.declare_parameter("frame_id", "lidar_link")
        self.declare_parameter("scan_rate_hz", 10.0)
        self.declare_parameter("range_min", 0.15)
        self.declare_parameter("range_max", 12.0)
        self.declare_parameter("num_readings", 360)

        scan_topic = self.get_parameter("scan_topic").get_parameter_value().string_value
        self.frame_id = self.get_parameter("frame_id").get_parameter_value().string_value
        self.range_min = self.get_parameter("range_min").get_parameter_value().double_value
        self.range_max = self.get_parameter("range_max").get_parameter_value().double_value
        self.num_readings = self.get_parameter("num_readings").get_parameter_value().integer_value
        scan_rate_hz = self.get_parameter("scan_rate_hz").get_parameter_value().double_value

        self.scan_pub = self.create_publisher(LaserScan, scan_topic, 10)
        self.phase = 0.0
        self.timer = self.create_timer(1.0 / max(scan_rate_hz, 1.0), self.publish_scan)

    def publish_scan(self) -> None:
        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.frame_id
        msg.angle_min = 0.0
        msg.angle_max = 2.0 * math.pi
        msg.angle_increment = (msg.angle_max - msg.angle_min) / float(self.num_readings)
        msg.time_increment = 0.0
        msg.scan_time = 0.1
        msg.range_min = self.range_min
        msg.range_max = self.range_max

        values = []
        for i in range(self.num_readings):
            angle = float(i) / float(self.num_readings) * 2.0 * math.pi
            dynamic = 0.8 * math.sin(angle * 4.0 + self.phase)
            reading = max(self.range_min, min(self.range_max, 5.0 + dynamic))
            values.append(reading)
        self.phase += 0.1
        msg.ranges = values
        msg.intensities = [100.0] * self.num_readings
        self.scan_pub.publish(msg)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = SensorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
