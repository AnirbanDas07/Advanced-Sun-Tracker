import cv2
import numpy as np
import math
import os
import csv
from datetime import datetime

class SunTracker:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.fov_horizontal = 60  # degrees
        self.fov_vertical = 45
        self.log_file = "logs/sun_positions.csv"
        self._setup_logging()

    def _setup_logging(self):
        os.makedirs("logs", exist_ok=True)
        file_exists = os.path.isfile(self.log_file)
        self.log = open(self.log_file, 'a')
        self.writer = csv.writer(self.log)
        if not file_exists:
            self.writer.writerow(['timestamp', 'x', 'y', 'azimuth', 'altitude'])

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def get_frame(self):
        ret, frame = self.cap.read()
        return cv2.flip(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), -1)

    def locate_sun(self, frame):
        _, thresholded = cv2.threshold(frame, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(largest)
            if radius > 5:
                cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0), 2)
                return int(x), int(y)
        return None, None

    def calculate_angles(self, x, y):
        dx = x - self.center_x
        dy = y - self.center_y

        angle_azimuth = (dx / self.width) * self.fov_horizontal
        angle_altitude = -(dy / self.height) * self.fov_vertical

        return round(angle_azimuth, 1), round(angle_altitude, 1)

    def log_position(self, x, y, azimuth, altitude):
        timestamp = datetime.now().isoformat()
        self.writer.writerow([timestamp, x, y, azimuth, altitude])

    def stop_camera(self):
        self.cap.release()
        self.log.close()
