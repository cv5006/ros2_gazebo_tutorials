from os import environ, path
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.actions import ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import ThisLaunchFileDir
from launch.conditions import IfCondition

from scripts import GazeboRosPaths


def generate_launch_description():
    model, plugin, media = GazeboRosPaths.get_paths()
    
    if 'GAZEBO_MODEL_PATH' in environ:
        model += ':'+environ['GAZEBO_MODEL_PATH']
    if 'GAZEBO_PLUGIN_PATH' in environ:
        plugin += ':'+environ['GAZEBO_PLUGIN_PATH']
    if 'GAZEBO_RESOURCE_PATH' in environ:
        media += ':'+environ['GAZEBO_RESOURCE_PATH']

    model += path.abspath(path.join(path.dirname(__file__), '../models'))
    
    env = {'GAZEBO_MODEL_PATH': model,
           'GAZEBO_PLUGIN_PATH': plugin,
           'GAZEBO_RESOURCE_PATH': media}
   
    #environ['GAZEBO_MODEL_PATH'] = model
    #model += ':' + environ['GAZEBO_MODEL_PATH']
    env = {'GAZEBO_MODEL_PATH' : model}
    
    spawner = Node(
        package = 'robot_spawner',            
        node_executable = 'spawner',
        node_name = 'spawner',
        output='screen' ## output option for debug
    )

    gazebo = ExecuteProcess(
        cmd=['gazebo','--verbose','-s','libgazebo_ros_factory.so'],
        #additional_env=env,
        output='screen'
    )
    #gzserver = IncludeLaunchDescription(
    #    PythonLaunchDescriptionSource(
    #            '/opt/ros/eloquent/share/gazebo_ros/launch/gzserver.launch.py'),
    #)
    return LaunchDescription([        
        gazebo,
        spawner,
        
        #gzserver        
    ])
