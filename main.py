import cv2
from tracker import SunTracker
from hardware_control import move_servos

def main():
    tracker = SunTracker()
    tracker.start_camera()

    try:
        while True:
            frame = tracker.get_frame()
            x, y = tracker.locate_sun(frame)

            if x and y:
                angle_azimuth, angle_altitude = tracker.calculate_angles(x, y)
                print(f"Sun Position: Azimuth {angle_azimuth:.1f}°, Altitude {angle_altitude:.1f}°")
                tracker.log_position(x, y, angle_azimuth, angle_altitude)

                # Optional: Move servos on Raspberry Pi
                move_servos(angle_azimuth, angle_altitude)

            cv2.imshow('Sun Tracker', frame)

            if cv2.waitKey(1) == 27:  # ESC key
                break
    finally:
        tracker.stop_camera()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
