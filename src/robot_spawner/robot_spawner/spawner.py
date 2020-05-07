import os
import sys
import rclpy

from rclpy.node import Node
from std_srvs.srv import Empty

from ament_index_python.packages import get_package_share_directory
from gazebo_msgs.srv import SpawnEntity


class Spawner(Node):

    def __init__(self):
        super().__init__('spawner')
        self.srv = self.create_service(Empty, 'spawn', self.spawn_callback)
        self.cli = self.create_client(SpawnEntity, "/spawn_entity")
        #call_async()


        sdf_file_path = os.path.join(
            "/home","seo",".gazebo", "models", "H_LowerLimb", "model.sdf")

        self.request = SpawnEntity.Request()
        self.request.name = 'test'
        self.request.xml = open(sdf_file_path, 'r').read()
        self.request.robot_namespace = 'ns'
        self.request.initial_pose.position.x = 0.0
        self.request.initial_pose.position.y = 0.0
        self.request.initial_pose.position.z = 0.0

    # callback func must have args; request, response
    # and return response. Or, type execption will be thrown!
    def spawn_callback(self, request, response):
        self.get_logger().info("Sending Request...")
        future = self.cli.call_async(self.request)
        
        return response


def main(args=None):
    rclpy.init(args=args)

    node = Spawner()

    rclpy.spin(node)

    node.destroy_node

    rclpy.shutdown()

if __name__ == '__main__':
    main()