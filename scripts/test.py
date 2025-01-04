import RPi.GPIO as GPIO
import time

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
PWM_FREQUENCY = 100  # 100Hz is generally suitable for DC motors
pwm_a = GPIO.PWM(ENA, PWM_FREQUENCY)
pwm_b = GPIO.PWM(ENB, PWM_FREQUENCY)
pwm_a.start(0)  # Start with motors stopped
pwm_b.start(0)

def run_forward(speed=60):
    """
    Function to run both motors forward at a specified speed.
    :param speed: PWM duty cycle (0 to 100)
    """
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)
    print(f"Motors running forward at {speed}% speed.")

def stop_motors():
    """
    Function to stop both motors.
    """
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    print("Motors stopped.")

try:
    print("Starting motor test...")
    run_forward(speed=100)    # Run motors forward at 60% speed
    time.sleep(5)            # Run for 5 seconds
    stop_motors()            # Stop motors after 5 seconds
except KeyboardInterrupt:
    # If the script is interrupted, ensure motors are stopped
    stop_motors()
    print("Motor test interrupted by user.")
finally:
    # Clean up GPIO settings
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
    print("GPIO cleaned up.")
