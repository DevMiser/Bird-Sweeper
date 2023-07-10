# the following program is provided by DevMiser - https://github.com/DevMiser

from picamera import PiCamera
import time
import RPi.GPIO as GPIO

# Pins definitions
sensor_pin = 22
servo_pin = 18
relay_pin = 25

camera = PiCamera()
camera.resolution = (1280, 720)
camera.contrast = 10
time.sleep(2)

# Set up pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(sensor_pin, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(relay_pin, GPIO.OUT)

# Set pulse width modulation (PWM) frequency
frequency = 50

# Remember the current and previous button states
current_state = False
prev_state = False

def servo_move():
    servo = GPIO.PWM(servo_pin, frequency)
    servo.start(8.5)
    sweep = 1
    while sweep <= 1:
        servo.ChangeDutyCycle(7.3)
        time.sleep(0.5)
        servo.ChangeDutyCycle(8.5)
        time.sleep(0.5)
        sweep = sweep + 1
        print ("sweep activated")
        servo.stop()

try:
    while True:
        current_state = GPIO.input(sensor_pin)
        if (current_state == True) and (prev_state == False):
            moment = time.ctime()
            print("motion detected at: %s" % moment)
            file_name = "/home/pi/Desktop/Clips/video_" + str(moment) + ".h264"
            camera.start_recording(file_name)
            GPIO.output(relay_pin,GPIO.HIGH)
            time.sleep(2)
            servo_move()
            time.sleep(1)
            GPIO.output(relay_pin,GPIO.LOW)
            time.sleep(5)
            camera.stop_recording()
        prev_state = current_state
        time.sleep(1)

# When ctrl+c is pressed, this will be called
finally:
    GPIO.cleanup()
