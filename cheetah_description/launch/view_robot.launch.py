#!/usr/bin/env python3
"""
Minimal launch file to visualize the cheetah robot in RViz2.

- Loads the pre-generated URDF: `urdf/robot_with_kinect.urdf`
- Starts `robot_state_publisher` with the `robot_description` parameter
- Starts `joint_state_publisher_gui` so you can move joints interactively
- Starts `rviz2` with `rviz/urdf_viewer.rviz`
"""
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_name = 'cheetah_description'

    default_urdf = PathJoinSubstitution([FindPackageShare(pkg_name), 'urdf', 'robot_with_kinect.urdf'])
    default_rviz = PathJoinSubstitution([FindPackageShare(pkg_name), 'rviz', 'urdf_viewer.rviz'])

    urdf_model = LaunchConfiguration('urdf_model', default=default_urdf)
    rviz_config = LaunchConfiguration('rviz_config', default=default_rviz)
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    # Load the URDF file content (robot is pre-generated URDF)
    robot_description = ParameterValue(Command(['xacro ', urdf_model]), value_type=str)

    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': use_sim_time}]
    )

    jsp_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': use_sim_time}]
    )

    ld = LaunchDescription()

    ld.add_action(DeclareLaunchArgument('urdf_model', default_value=default_urdf,
                                        description='Path to URDF file'))
    ld.add_action(DeclareLaunchArgument('rviz_config', default_value=default_rviz,
                                        description='Path to RViz config file'))
    ld.add_action(DeclareLaunchArgument('use_sim_time', default_value='false',
                                        description='Use sim time'))

    ld.add_action(rsp_node)
    ld.add_action(jsp_node)
    ld.add_action(rviz_node)

    return ld
