import RPi.GPIO as GPIO
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

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

# Setup PWM (for speed control)
pwm_a = GPIO.PWM(ENA, 100)  # 1000Hz
pwm_b = GPIO.PWM(ENB, 100)
pwm_a.start(0)  # Start with 0% duty cycle (motors stopped)
pwm_b.start(0)

def stop_motors():
    """Stop both motors entirely."""
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    print("Motors stopped")

def accelerate_forward(final_speed=100, step=10, delay=1):
    """
    Gradually ramp speed from 0% to final_speed% for forward motion.
    - step: increments of duty cycle
    - delay: pause between increments
    """
    # Set direction pins for forward
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

    current_speed = 0
    while current_speed <= final_speed:
        pwm_a.ChangeDutyCycle(current_speed)
        pwm_b.ChangeDutyCycle(current_speed)
        time.sleep(delay)
        current_speed += step
        print(f"Current speed: {current_speed}%")
    print(f"Accelerated forward up to {final_speed}%")

def accelerate_backward(final_speed=100, step=10, delay=0.05):
    """
    Gradually ramp speed from 0% to final_speed% for backward motion.
    - step: increments of duty cycle
    - delay: pause between increments
    """
    # Set direction pins for backward
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

    current_speed = 0
    while current_speed <= final_speed:
        pwm_a.ChangeDutyCycle(current_speed)
        pwm_b.ChangeDutyCycle(current_speed)
        time.sleep(delay)
        current_speed += step
    print(f"Accelerated backward up to {final_speed}%")

@app.route("/")
def index():
    return jsonify({"message": "BARWITA Motor Control API with Acceleration"})

@app.route("/forward", methods=["POST"])
def forward():
    # Parse a 'speed' from JSON or default to 100
    data = request.get_json(silent=True)
    speed = data.get("speed", 100) if data else 100

    # Safely stop motors first if you prefer
    stop_motors()
    # Then accelerate forward
    accelerate_forward(final_speed=speed)
    return jsonify({"status": "Moving forward", "speed": speed})

@app.route("/backward", methods=["POST"])
def backward():
    data = request.get_json(silent=True)
    speed = data.get("speed", 100) if data else 100

    stop_motors()
    accelerate_backward(final_speed=speed)
    return jsonify({"status": "Moving backward", "speed": speed})

@app.route("/stop", methods=["POST"])
def stop():
    stop_motors()
    return jsonify({"status": "Motors stopped"})

@app.route("/cleanup", methods=["POST"])
def cleanup():
    """Optional route to clean up GPIO if you want to free resources."""
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
    return jsonify({"status": "GPIO cleaned up, server still running. Re-init needed."})

if __name__ == "__main__":
    print("Motor Control with Acceleration via Flask HTTP endpoints.")
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        stop_motors()
        pwm_a.stop()
        pwm_b.stop()
        GPIO.cleanup()
        print("GPIO Cleaned Up, shutting down.")
