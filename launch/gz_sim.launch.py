import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubsitution
from launch_ros.actions import Node

import xacro


def generate_launch_description():

    # 加载 XACRO 描述文件 到 URDF ( Process the URDF file )
    pkg_path = os.path.join(get_package_share_directory('panda_sar'))
    xacro_file = os.path.join(pkg_path,'description','robot.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file).toxml()
    
    # 创建 joint_state_publisher_gui 节点 ( Create a joint_state_publisher_gui node )
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={
            'gz_args': PathJoinSubsitution([
                pkg_project_gazebo,
                ''
            ])
        }
        )
    )

    # 创建 robot_state_publisher 节点 ( Create a robot_state_publisher node )
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        robot_description=robot_description_config,
        use_sim_time=True
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gz_sim = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(get_package_share_directory('pkg_ros_gz_sim'), 'launch', 'gz_sim.launch.py')),
                    launch_arguments={'gz_args': PathJoinSubsitution([
                        

                    ])}.items()

             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='ros_gz_sim', executable='ros_gz_spawn_model.launch.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity_name', 'panda_sar'],
                        output='screen')


    # Launch them all!
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
    ])