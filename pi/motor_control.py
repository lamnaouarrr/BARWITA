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
pwm_a = GPIO.PWM(ENA, 100)  # 100Hz
pwm_b = GPIO.PWM(ENB, 100)
pwm_a.start(0)  # Start with 0% duty cycle (motors stopped)
pwm_b.start(0)

def set_motor_forward(speed=50):
    """Set both motors forward at a given duty cycle speed."""
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)
    print(f"Set motors forward with speed {speed}%")

def set_motor_backward(speed=50):
    """Set both motors backward at a given duty cycle speed."""
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)
    print(f"Set motors backward with speed {speed}%")

def stop_motors():
    """Stop both motors entirely."""
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    print("Motors stopped")

# -- Flask routes --

@app.route("/")
def index():
    return jsonify({"message": "BARWITA Motor Control API is running!"})

@app.route("/forward", methods=["POST"])
def forward():
    # Optionally parse a 'speed' from JSON payload or default to 50
    data = request.get_json(silent=True)
    speed = data.get("speed", 50) if data else 50

    set_motor_forward(speed)
    return jsonify({"status": "Moving forward", "speed": speed})

@app.route("/backward", methods=["POST"])
def backward():
    data = request.get_json(silent=True)
    speed = data.get("speed", 50) if data else 50

    set_motor_backward(speed)
    return jsonify({"status": "Moving backward", "speed": speed})

@app.route("/stop", methods=["POST"])
def stop():
    stop_motors()
    return jsonify({"status": "Motors stopped"})

# Graceful shutdown or cleanup route (OPTIONAL)
@app.route("/cleanup", methods=["POST"])
def cleanup():
    """Optional route to clean up GPIO if you want to free resources."""
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
    return jsonify({"status": "GPIO cleaned up, server still running. Re-init needed."})

# Run the Flask server
if __name__ == "__main__":
    print("Motor Control via Flask HTTP endpoints.")
    try:
        app.run(host='0.0.0.0', port=5000)  # Listen on all interfaces, port 5000
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        stop_motors()
        pwm_a.stop()
        pwm_b.stop()
        GPIO.cleanup()
        print("GPIO Cleaned Up, shutting down.")
