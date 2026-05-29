#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2
import numpy as np
import time


class MultiObjectTracker(Node):

    def __init__(self):

        super().__init__('multi_object_tracker')

        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            Image,
            '/camera/vision_camera/image_raw',
            self.image_callback,
            10
        )

        # Previous positions
        self.previous_positions = {}

        # Previous time
        self.previous_time = time.time()

        self.get_logger().info(
            "Multi Object Tracker Started"
        )


    def process_color(
        self,
        frame,
        hsv,
        lower,
        upper,
        color_name,
        box_color
    ):

        mask = cv2.inRange(
            hsv,
            lower,
            upper
        )

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )

        current_time = time.time()

        dt = current_time - self.previous_time

        for contour in contours:

            area = cv2.contourArea(contour)

            if area > 500:

                x, y, w, h = cv2.boundingRect(contour)

                # CENTER
                cx = int(x + w / 2)
                cy = int(y + h / 2)

                # PREVIOUS POSITION
                prev = self.previous_positions.get(
                    color_name,
                    (cx, cy)
                )

                prev_x, prev_y = prev

                # VELOCITY
                vx = (cx - prev_x) / dt
                vy = (cy - prev_y) / dt

                speed = np.sqrt(vx**2 + vy**2)

                # SAVE CURRENT POSITION
                self.previous_positions[color_name] = (
                    cx,
                    cy
                )

                # DRAW BOUNDING BOX
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    box_color,
                    2
                )

                # DRAW CENTER
                cv2.circle(
                    frame,
                    (cx, cy),
                    5,
                    box_color,
                    -1
                )

                # TEXT
                text = (
                    f"{color_name} "
                    f"X:{cx} Y:{cy} "
                    f"V:{speed:.1f}"
                )

                cv2.putText(
                    frame,
                    text,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    box_color,
                    2
                )

                # PRINT TERMINAL
                print(
                    f"{color_name} -> "
                    f"X:{cx} "
                    f"Y:{cy} "
                    f"Speed:{speed:.2f}"
                )

        self.previous_time = current_time

        return mask


    def image_callback(self, msg):

        frame = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding='bgr8'
        )

        hsv = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2HSV
        )

        # RED
        red_lower = np.array([0, 120, 70])
        red_upper = np.array([10, 255, 255])

        # GREEN
        green_lower = np.array([40, 40, 40])
        green_upper = np.array([80, 255, 255])

        # BLUE
        blue_lower = np.array([100, 150, 0])
        blue_upper = np.array([140, 255, 255])

        # PROCESS OBJECTS
        red_mask = self.process_color(
            frame,
            hsv,
            red_lower,
            red_upper,
            "RED",
            (0, 0, 255)
        )

        green_mask = self.process_color(
            frame,
            hsv,
            green_lower,
            green_upper,
            "GREEN",
            (0, 255, 0)
        )

        blue_mask = self.process_color(
            frame,
            hsv,
            blue_lower,
            blue_upper,
            "BLUE",
            (255, 0, 0)
        )

        # SHOW WINDOWS
        cv2.imshow(
            "Multi Object Tracking",
            frame
        )

        cv2.imshow("Red Mask", red_mask)
        cv2.imshow("Green Mask", green_mask)
        cv2.imshow("Blue Mask", blue_mask)

        cv2.waitKey(1)


def main(args=None):

    rclpy.init(args=args)

    node = MultiObjectTracker()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
