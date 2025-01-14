import RPi.GPIO as GPIO
import time
import sys
import termios
import tty

# GPIO pin definitions
ENA = 18  # Enable pin for Motor A
IN1 = 23  # Input pin 1 for Motor A
IN2 = 24  # Input pin 2 for Motor A
ENB = 25  # Enable pin for Motor B
IN3 = 12  # Input pin 3 for Motor B
IN4 = 16  # Input pin 4 for Motor B

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Setup PWM
pwm_a = GPIO.PWM(ENA, 100)  # 100Hz
pwm_b = GPIO.PWM(ENB, 100)
pwm_a.start(0)  # Start with 0% duty cycle (motors stopped)
pwm_b.start(0)

def set_motor_forward(speed=50):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)
    print(f"Set motors forward with speed {speed}%")

def set_motor_backward(speed=50):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)
    print(f"Set motors backward with speed {speed}%")

def stop_motors():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    print("Motors stopped")

def getch():
    """Function to capture single keypress"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

try:
    print("Motor Control Initialized")
    print("Press 'w' to move forward, 's' to move backward, 'q' to quit.")
    while True:
        key = getch()
        if key == 'w':
            print("Moving Forward")
            set_motor_forward(50)  # Adjust speed as needed
        elif key == 's':
            print("Moving Backward")
            set_motor_backward(50)
        elif key == 'q':
            print("Stopping Motors and Exiting")
            stop_motors()
            break
        else:
            print("Invalid Key Pressed")
            stop_motors()
except KeyboardInterrupt:
    print("\nInterrupted by User")
finally:
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
    print("GPIO Cleaned Up")
