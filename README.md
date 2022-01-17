# social-inter-robot
Things to install and operating instructions for the project to run;
1. To use turtlebot3 waffle_pi, "git clone -b noetic-devel https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git" command should be run to ~/catkin_ws/src/ directory on terminal.
2. To install the audiocommon package, run the command "sudo apt-get install ros-noetic-audio-common" on the terminal.
3. To run the audicommon package, the command "sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev" must be run on the terminal.
4. Run the "gedit ~/.bashrc" command in the catkin_ws directory and write "source /opt/ros/noetic/setup.bash" and "source ~/catkin_ws/devel/setup.bash" on the bottom line of the file.
5. Compiling should be done with the "catkin_make" command, where a new terminal is opened.
6. While running, the "roscore" command should be run in a terminal opened in the ~/catkin_ws/ directory.
7. To view the robot and the map on the gazebo, the command "roslaunch social-inter-robot kindergarten.launch" should be run on the ~/catkin_ws directory.
8. For the appearance of the robot on rviz, the command "roslaunch social-inter-robot turtlebot3_gazebo_rviz.launch" should be run on the ~/catkin_ws directory.
9. After opening Gazebo and Rviz, "python3 line_follower.py" command should be run on ~/catkin_ws/src/social-inter-robot/src directory to observe the robot's movement and audio outputs.
