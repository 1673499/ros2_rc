# CMake generated Testfile for 
# Source directory: /home/ros2/ros2_rc/src/navigation2/nav2_behavior_tree/test
# Build directory: /home/ros2/ros2_rc/build/nav2_behavior_tree/test
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(test_bt_conversions "/usr/bin/python3" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/ros2/ros2_rc/build/nav2_behavior_tree/test_results/nav2_behavior_tree/test_bt_conversions.gtest.xml" "--package-name" "nav2_behavior_tree" "--output-file" "/home/ros2/ros2_rc/build/nav2_behavior_tree/ament_cmake_gtest/test_bt_conversions.txt" "--command" "/home/ros2/ros2_rc/build/nav2_behavior_tree/test/test_bt_conversions" "--gtest_output=xml:/home/ros2/ros2_rc/build/nav2_behavior_tree/test_results/nav2_behavior_tree/test_bt_conversions.gtest.xml")
set_tests_properties(test_bt_conversions PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/ros2/ros2_rc/build/nav2_behavior_tree/test/test_bt_conversions" TIMEOUT "60" WORKING_DIRECTORY "/home/ros2/ros2_rc/build/nav2_behavior_tree/test" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/ros2/ros2_rc/src/navigation2/nav2_behavior_tree/test/CMakeLists.txt;1;ament_add_gtest;/home/ros2/ros2_rc/src/navigation2/nav2_behavior_tree/test/CMakeLists.txt;0;")
subdirs("../gtest")
subdirs("plugins/condition")
subdirs("plugins/decorator")
subdirs("plugins/control")
subdirs("plugins/action")
