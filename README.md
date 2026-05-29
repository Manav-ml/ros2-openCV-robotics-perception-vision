ROS2 + OpenCV Robotics Vision System

Overview

This project demonstrates a complete robotics perception pipeline using ROS2, Gazebo, and OpenCV.

A virtual camera is simulated in Gazebo and integrated with ROS2 image topics. OpenCV is used for real-time image processing including color detection, shape detection, object tracking, multi-object tracking, and velocity estimation.

This project serves as a foundation for advanced robotics perception systems such as AMRs, robotic arms, autonomous drones, and AI-based robotic vision.

---

# Features

## ROS2 + Gazebo Camera Simulation

* Virtual camera model in Gazebo
* ROS2 camera plugin integration
* Real-time image publishing

## OpenCV Integration

* ROS2 image topic subscription
* Image conversion using cv_bridge
* Real-time image visualization

## Color Detection

* HSV color segmentation
* Red object detection
* Green object detection
* Blue object detection

## Shape Detection

* Rectangle detection
* Circle/Sphere detection
* Cylinder-like object detection
* Contour analysis

## Object Tracking

* Bounding box tracking
* Centroid tracking
* Coordinate extraction

## Multi-Object Tracking

* Simultaneous tracking of multiple objects
* Independent tracking pipelines

## Velocity Estimation

Real-time motion estimation using:

Velocity = ΔPosition / ΔTime

* Dynamic motion analysis
* Speed estimation
* Frame-to-frame tracking

---

# Technologies Used

* ROS2 Humble
* Gazebo
* OpenCV
* Python
* cv_bridge
* sensor_msgs

---

# System Architecture

```plaintext
Gazebo Camera
      ↓
ROS2 Image Topic
      ↓
cv_bridge
      ↓
OpenCV Processing
      ↓
Detection + Tracking
```

---

# Project Structure

```plaintext
ros2-opencv-robotics-vision/
│── README.md
│── LICENSE
│── screenshots/
│── videos/
│── worlds/
│── models/
│── scripts/
│── launch/
│── docs/
```

---

# Implemented Scripts

## Color Detection

* Detects RGB objects using HSV masks

## Shape Detection

* Detects geometric shapes using contour approximation

## Object Tracking

* Tracks object center positions in real-time

## Multi-Object Tracking

* Tracks multiple objects simultaneously

## Velocity Estimation

* Calculates object movement speed dynamically

---

# Screenshots

## Gazebo World

(Add screenshot here)

## Color Detection

(Add screenshot here)

## Shape Detection

(Add screenshot here)

## Multi-Object Tracking

(Add screenshot here)

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/ros2-opencv-robotics-vision.git
```

## Navigate to Workspace

```bash
cd ros2-opencv-robotics-vision
```

## Install Dependencies

```bash
sudo apt install ros-humble-cv-bridge
sudo apt install ros-humble-image-transport
sudo apt install python3-opencv
```

---

# Running the Simulation

## Launch Gazebo World

```bash
gazebo worlds/vision_world.world
```

## Run Tracking Script

```bash
python3 scripts/multi_object_tracker.py
```

---

# Future Improvements

* ArUco Marker Detection
* Pose Estimation
* YOLO Object Detection
* Depth Camera Integration
* AMR Perception
* Robotic Arm Vision
* AI-based Object Classification

---

# Learning Outcomes

Through this project, the following concepts were learned:

* ROS2 perception pipeline
* Gazebo simulation integration
* OpenCV image processing
* Real-time robotics vision
* Multi-object tracking
* Motion estimation
* Computer vision fundamentals

---

# Author

## Manav Lamture

Robotics and Automation Engineer

LinkedIn:
(Add LinkedIn URL)

GitHub:
(Add GitHub URL)
a
