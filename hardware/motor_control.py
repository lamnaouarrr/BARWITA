from gpiozero import OutputDevice, PWMOutputDevice

# Motor A pins
ENA = PWMOutputDevice(18)  # Enable pin for Motor A (PWM for speed control)
IN1 = OutputDevice(23)    # Input pin 1 for Motor A (direction control)
IN2 = OutputDevice(24)    # Input pin 2 for Motor A (direction control)

# Motor B pins
ENB = PWMOutputDevice(25)  # Enable pin for Motor B (PWM for speed control)
IN3 = OutputDevice(12)    # Input pin 3 for Motor B (direction control)
IN4 = OutputDevice(16)    # Input pin 4 for Motor B (direction control)

# Example motor control functions
def motor_a_forward(speed=1.0):
    """Move Motor A forward at specified speed (0.0 to 1.0)"""
    IN1.on()
    IN2.off()
    ENA.value = speed

def motor_a_backward(speed=1.0):
    """Move Motor A backward at specified speed (0.0 to 1.0)"""
    IN1.off()
    IN2.on()
    ENA.value = speed

def motor_a_stop():
    """Stop Motor A"""
    IN1.off()
    IN2.off()
    ENA.off()

def motor_b_forward(speed=1.0):
    """Move Motor B forward at specified speed (0.0 to 1.0)"""
    IN3.on()
    IN4.off()
    ENB.value = speed

def motor_b_backward(speed=1.0):
    """Move Motor B backward at specified speed (0.0 to 1.0)"""
    IN3.off()
    IN4.on()
    ENB.value = speed

def motor_b_stop():
    """Stop Motor B"""
    IN3.off()
    IN4.off()
    ENB.off()

def stop_all_motors():
    """Stop both motors"""
    motor_a_stop()
    motor_b_stop()

# Cleanup function (call this when your program ends)
def cleanup():
    """Clean up GPIO resources"""
    stop_all_motors()
    ENA.close()
    IN1.close()
    IN2.close()
    ENB.close()
    IN3.close()
    IN4.close()