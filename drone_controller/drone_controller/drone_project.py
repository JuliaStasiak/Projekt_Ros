import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Pose, Point
import time

class DroneController(Node):
    def __init__(self):
        super().__init__('drone_controller')

        self.gt_pose_sub = self.create_subscription(
            Pose,
            '/drone/gt_pose',
            self.pose_callback,
            1)

        self.gt_pose = None

        self.command_pub = self.create_publisher(Twist, '/drone/cmd_vel', 10)

        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.starting_point = Point(x=0.0, y=0.0, z=5.0)

        self.start_time = time.time()

        self.flight_stage = 0

    def pose_callback(self, data):
        self.gt_pose = data

    def timer_callback(self):
        if self.gt_pose is not None:
            elapsed_time = time.time() - self.start_time

            if elapsed_time >= 16.0:
                self.flight_stage += 1
                self.start_time = time.time()

            self.execute_flight_stage()

    def execute_flight_stage(self):
        cmd = Twist()

        if self.flight_stage == 0:
            cmd.linear.z = 5.0
            cmd.linear.x = 0.0
        elif 0 < self.flight_stage < 5:
            cmd.linear.z = 5.0
            cmd.linear.x = 4.0
        elif self.flight_stage == 5:
            cmd.linear.z = 0.0
            cmd.linear.x = 0.0

        self.command_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)

    try:
        node = DroneController()
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("END.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()




