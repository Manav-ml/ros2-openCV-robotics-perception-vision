#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2
import numpy as np


class ShapeColorDetector(Node):

    def __init__(self):

        super().__init__('shape_color_detector')

        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            Image,
            '/camera/vision_camera/image_raw',
            self.image_callback,
            10
        )

        self.get_logger().info("Shape + Color Detector Started")
        
        
    def detect_objects(self, frame, hsv, lower, upper, color_name):

        mask = cv2.inRange(hsv, lower, upper)

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:

            area = cv2.contourArea(contour)

            if area > 500:

                # Calculate perimeter
                perimeter = cv2.arcLength(contour, True)

                # Approximate contour
                approx = cv2.approxPolyDP(
                    contour,
                    0.02 * perimeter,
                    True
                )

                vertices = len(approx)

                shape = "Unknown"

                                # Bounding box
                x, y, w, h = cv2.boundingRect(approx)

                # Prevent division by zero
                if perimeter != 0:

                    # Circularity
                    circularity = (
                        4 * np.pi * area
                    ) / (perimeter * perimeter)

                    # Aspect ratio
                    aspect_ratio = float(w) / h

                    # TRIANGLE
                    if vertices == 3:
                        shape = "Triangle"

                    # RECTANGLE
                    elif vertices == 4:
                        shape = "Rectangle"

                    # ROUND OBJECTS
                    elif circularity > 0.75:

                        # SPHERE
                        if 0.9 <= aspect_ratio <= 1.1:
                            shape = "Sphere"

                        # CYLINDER
                        else:
                            shape = "Cylinder"
               

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

                text = f"{color_name} {shape}"

                cv2.putText(
                    frame,
                    text,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )

        return mask


    def image_callback(self, msg):

        frame = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding='bgr8'
        )

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # RED
        red_lower = np.array([0, 120, 70])
        red_upper = np.array([10, 255, 255])

        # GREEN
        green_lower = np.array([40, 40, 40])
        green_upper = np.array([80, 255, 255])

        # BLUE
        blue_lower = np.array([100, 150, 0])
        blue_upper = np.array([140, 255, 255])

        red_mask = self.detect_objects(
            frame,
            hsv,
            red_lower,
            red_upper,
            "RED"
        )

        green_mask = self.detect_objects(
            frame,
            hsv,
            green_lower,
            green_upper,
            "GREEN"
        )

        blue_mask = self.detect_objects(
            frame,
            hsv,
            blue_lower,
            blue_upper,
            "BLUE"
        )

        cv2.imshow("Detected Objects", frame)

        cv2.imshow("Red Mask", red_mask)
        cv2.imshow("Green Mask", green_mask)
        cv2.imshow("Blue Mask", blue_mask)

        cv2.waitKey(1)


def main(args=None):

    rclpy.init(args=args)

    node = ShapeColorDetector()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
