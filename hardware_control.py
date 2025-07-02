import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
servo_azimuth_pin = 11
servo_altitude_pin = 12

GPIO.setup(servo_azimuth_pin, GPIO.OUT)
GPIO.setup(servo_altitude_pin, GPIO.OUT)

pwm_azimuth = GPIO.PWM(servo_azimuth_pin, 50)  # 50Hz
pwm_altitude = GPIO.PWM(servo_altitude_pin, 50)

pwm_azimuth.start(0)
pwm_altitude.start(0)

def set_angle(pwm, angle):
    duty = angle / 18 + 2
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.3)
    pwm.ChangeDutyCycle(0)

def move_servos(azimuth_angle, altitude_angle):
    azimuth_deg = min(max(azimuth_angle + 90, 0), 180)
    altitude_deg = min(max(altitude_angle + 90, 0), 180)
    set_angle(pwm_azimuth, azimuth_deg)
    set_angle(pwm_altitude, altitude_deg)
