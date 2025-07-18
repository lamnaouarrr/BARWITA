from gpiozero import OutputDevice, PWMOutputDevice
import warnings
import sys
import termios
import tty
import select
import threading
import time

# Suppress gpiozero fallback warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning, module="gpiozero")

def create_motor_pins():
    """Create motor control pins with fallback for PWM issues"""
    try:
        # Try to create PWM devices first
        ena = PWMOutputDevice(18)
        enb = PWMOutputDevice(25)
        print("PWM devices created successfully")
        return ena, enb, True
    except Exception as e:
        print(f"PWM creation failed: {e}")
        print("Falling back to regular OutputDevice (no speed control)")
        try:
            # Fallback to regular OutputDevice
            ena = OutputDevice(18)
            enb = OutputDevice(25)
            return ena, enb, False
        except Exception as e2:
            print(f"Failed to create OutputDevice: {e2}")
            print("GPIO initialization failed completely")
            return None, None, False

# Global variables for GPIO devices
ENA = ENB = IN1 = IN2 = IN3 = IN4 = None
PWM_AVAILABLE = False
PINS_INITIALIZED = False

def initialize_gpio():
    """Initialize all GPIO pins"""
    global ENA, ENB, IN1, IN2, IN3, IN4, PWM_AVAILABLE, PINS_INITIALIZED
    
    # Create motor pins with fallback
    ENA, ENB, PWM_AVAILABLE = create_motor_pins()
    
    # Only create direction pins if enable pins were successful
    if ENA is not None and ENB is not None:
        try:
            IN1 = OutputDevice(23)    # Input pin 1 for Motor A (direction control)
            IN2 = OutputDevice(24)    # Input pin 2 for Motor A (direction control)
            IN3 = OutputDevice(12)    # Input pin 3 for Motor B (direction control)
            IN4 = OutputDevice(16)    # Input pin 4 for Motor B (direction control)
            PINS_INITIALIZED = True
            print("All GPIO pins initialized successfully")
        except Exception as e:
            print(f"Failed to create direction control pins: {e}")
            PINS_INITIALIZED = False
            IN1 = IN2 = IN3 = IN4 = None
    else:
        print("Cannot create direction pins - enable pins failed")
        PINS_INITIALIZED = False
        IN1 = IN2 = IN3 = IN4 = None

# Initialize GPIO on import
initialize_gpio()

# Example motor control functions
def motor_a_forward(speed=1.0):
    """Move Motor A forward at specified speed (0.0 to 1.0)"""
    if not PINS_INITIALIZED:
        print("Error: GPIO pins not initialized")
        return
    try:
        IN1.on()
        IN2.off()
        if PWM_AVAILABLE:
            ENA.value = speed
        else:
            ENA.on()  # Full speed only
    except Exception as e:
        print(f"Error controlling Motor A forward: {e}")

def motor_a_backward(speed=1.0):
    """Move Motor A backward at specified speed (0.0 to 1.0)"""
    if not PINS_INITIALIZED:
        print("Error: GPIO pins not initialized")
        return
    try:
        IN1.off()
        IN2.on()
        if PWM_AVAILABLE:
            ENA.value = speed
        else:
            ENA.on()  # Full speed only
    except Exception as e:
        print(f"Error controlling Motor A backward: {e}")

def motor_a_stop():
    """Stop Motor A"""
    if not PINS_INITIALIZED:
        return
    try:
        IN1.off()
        IN2.off()
        ENA.off()
    except Exception as e:
        print(f"Warning: Error stopping Motor A: {e}")

def motor_b_forward(speed=1.0):
    """Move Motor B forward at specified speed (0.0 to 1.0)"""
    if not PINS_INITIALIZED:
        print("Error: GPIO pins not initialized")
        return
    try:
        IN3.on()
        IN4.off()
        if PWM_AVAILABLE:
            ENB.value = speed
        else:
            ENB.on()  # Full speed only
    except Exception as e:
        print(f"Error controlling Motor B forward: {e}")

def motor_b_backward(speed=1.0):
    """Move Motor B backward at specified speed (0.0 to 1.0)"""
    if not PINS_INITIALIZED:
        print("Error: GPIO pins not initialized")
        return
    try:
        IN3.off()
        IN4.on()
        if PWM_AVAILABLE:
            ENB.value = speed
        else:
            ENB.on()  # Full speed only
    except Exception as e:
        print(f"Error controlling Motor B backward: {e}")

def motor_b_stop():
    """Stop Motor B"""
    if not PINS_INITIALIZED:
        return
    try:
        IN3.off()
        IN4.off()
        ENB.off()
    except Exception as e:
        print(f"Warning: Error stopping Motor B: {e}")

def stop_all_motors():
    """Stop both motors"""
    motor_a_stop()
    motor_b_stop()

# Cleanup function (call this when your program ends)
def cleanup():
    """Clean up GPIO resources"""
    try:
        stop_all_motors()
    except Exception as e:
        print(f"Warning: Error stopping motors during cleanup: {e}")
    
    # Close devices safely
    devices = [ENA, IN1, IN2, ENB, IN3, IN4]
    device_names = ['ENA', 'IN1', 'IN2', 'ENB', 'IN3', 'IN4']
    
    for device, name in zip(devices, device_names):
        try:
            if device and hasattr(device, 'closed') and not device.closed:
                device.close()
        except Exception as e:
            print(f"Warning: Error closing {name}: {e}")

# Movement functions for both motors
def move_forward(speed=1.0):
    """Move both motors forward (car moves forward)"""
    motor_a_forward(speed)
    motor_b_forward(speed)
    print(f"Moving forward at speed {speed}")

def move_backward(speed=1.0):
    """Move both motors backward (car moves backward)"""
    motor_a_backward(speed)
    motor_b_backward(speed)
    print(f"Moving backward at speed {speed}")

def turn_left(speed=1.0):
    """Turn left by moving right motor forward and left motor backward"""
    motor_a_backward(speed)  # Left motor backward
    motor_b_forward(speed)   # Right motor forward
    print(f"Turning left at speed {speed}")

def turn_right(speed=1.0):
    """Turn right by moving left motor forward and right motor backward"""
    motor_a_forward(speed)   # Left motor forward
    motor_b_backward(speed)  # Right motor backward
    print(f"Turning right at speed {speed}")

# Motor testing functions
def test_motor_a():
    """Test Motor A individually"""
    print("Testing Motor A...")
    print("  Forward for 2 seconds...")
    motor_a_forward(0.5)
    import time
    time.sleep(2)
    
    print("  Backward for 2 seconds...")
    motor_a_backward(0.5)
    time.sleep(2)
    
    print("  Stopping Motor A")
    motor_a_stop()
    print("Motor A test complete")

def test_motor_b():
    """Test Motor B individually"""
    print("Testing Motor B...")
    print("  Forward for 2 seconds...")
    motor_b_forward(0.5)
    import time
    time.sleep(2)
    
    print("  Backward for 2 seconds...")
    motor_b_backward(0.5)
    time.sleep(2)
    
    print("  Stopping Motor B")
    motor_b_stop()
    print("Motor B test complete")

def test_both_motors():
    """Test both motors together"""
    import time
    print("Testing both motors...")
    
    print("  Moving forward for 2 seconds...")
    move_forward(0.5)
    time.sleep(2)
    
    print("  Moving backward for 2 seconds...")
    move_backward(0.5)
    time.sleep(2)
    
    print("  Turning left for 1 second...")
    turn_left(0.5)
    time.sleep(1)
    
    print("  Turning right for 1 second...")
    turn_right(0.5)
    time.sleep(1)
    
    print("  Stopping all motors")
    stop_all_motors()
    print("Both motors test complete")

def run_full_test():
    """Run comprehensive motor tests"""
    try:
        print("Starting motor control tests...")
        print("=" * 40)
        
        test_motor_a()
        print()
        
        test_motor_b()
        print()
        
        test_both_motors()
        print()
        
        print("All tests completed successfully!")
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Error during testing: {e}")
    finally:
        cleanup()

# Real-time keyboard control system
class KeyboardController:
    def __init__(self):
        self.running = False
        self.current_action = "stop"
        self.speed = 1.0
        self.last_key_time = time.time()
        self.key_timeout = 0.25 # Stop if no key pressed for 0.5 seconds

    def get_char_non_blocking(self):
        """Get a single character from stdin without waiting for enter"""
        try:
            if sys.platform.startswith('win'):
                import msvcrt
                if msvcrt.kbhit():
                    ch = msvcrt.getch()
                    if isinstance(ch, bytes):
                        ch = ch.decode('utf-8')
                    return ch.lower()
                return None
            else:
                import termios
                import tty
                import select
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setcbreak(fd)
                    if select.select([sys.stdin], [], [], 0.05) == ([sys.stdin], [], []):
                        ch = sys.stdin.read(1)
                        return ch.lower() if ch else None
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except Exception:
            return None
        return None

    # --- SPEED SETTINGS (even further reduced for safer operation) ---
    BASE_SPEED = 0.015  # Even further reduced base speed for forward/backward
    TURN_SPEED = 0.001  # Even further reduced speed for turning (left/right)
    # You can adjust these values for your hardware

    def _move_forward_raw(self):
        try:
            # W: Both motors physically forward
            # Motor A (Left - IN1, IN2) Forward: IN1.on(), IN2.off()
            # Motor B (Right - IN3, IN4) Forward (assuming IN3/IN4 inverted): IN3.off(), IN4.on()
            IN1.on(); IN2.off() 
            IN3.off(); IN4.on()
            if PWM_AVAILABLE:
                ENA.value = self.BASE_SPEED; ENB.value = self.BASE_SPEED
            else:
                ENA.on(); ENB.on()
        except: pass

    def _move_backward_raw(self):
        try:
            # S: Both motors physically backward
            # Motor A (Left - IN1, IN2) Backward: IN1.off(), IN2.on()
            # Motor B (Right - IN3, IN4) Backward (assuming IN3/IN4 inverted): IN3.on(), IN4.off()
            IN1.off(); IN2.on()
            IN3.on(); IN4.off()
            if PWM_AVAILABLE:
                ENA.value = self.BASE_SPEED; ENB.value = self.BASE_SPEED
            else:
                ENA.on(); ENB.on()
        except: pass

    def _turn_left_raw(self):
        try:
            # A: Left motor backward, Right motor forward
            # Motor A (Left - IN1, IN2) Backward: IN1.off(), IN2.on()
            # Motor B (Right - IN3, IN4) Forward (assuming IN3/IN4 inverted): IN3.off(), IN4.on()
            IN1.off(); IN2.on()
            IN3.off(); IN4.on()
            if PWM_AVAILABLE:
                ENA.value = self.TURN_SPEED; ENB.value = self.TURN_SPEED
            else:
                ENA.on(); ENB.on()
        except: pass

    def _turn_right_raw(self):
        try:
            # D: Left motor forward, Right motor backward
            # Motor A (Left - IN1, IN2) Forward: IN1.on(), IN2.off()
            # Motor B (Right - IN3, IN4) Backward (assuming IN3/IN4 inverted): IN3.on(), IN4.off()
            IN1.on(); IN2.off()
            IN3.on(); IN4.off()
            if PWM_AVAILABLE:
                ENA.value = self.TURN_SPEED; ENB.value = self.TURN_SPEED
            else:
                ENA.on(); ENB.on()
        except: pass

    def _stop_raw(self):
        try:
            stop_all_motors()
        except Exception:
            pass

    def motor_control_loop(self):
        """Continuous motor control based on current action"""
        while self.running:
            if not PINS_INITIALIZED:
                time.sleep(0.1)
                continue
            # Stop if no key pressed for timeout
            if time.time() - self.last_key_time > self.key_timeout:
                if self.current_action != "stop":
                    self.current_action = "stop"
                    self._print_status()
            # Execute current action
            if self.current_action == "forward":
                self._move_forward_raw()
            elif self.current_action == "backward":
                self._move_backward_raw()
            elif self.current_action == "left":
                self._turn_left_raw()
            elif self.current_action == "right":
                self._turn_right_raw()
            else:
                self._stop_raw()
            time.sleep(0.05)

    def start_realtime_control(self):
        if not PINS_INITIALIZED:
            print("Error: GPIO pins not initialized")
            return
        print("\n" + "="*50)
        print("REAL-TIME KEYBOARD CONTROL")
        print("="*50)
        print("Controls:")
        print("  W - Forward (hold to continue)")
        print("  S - Backward (hold to continue)")
        print("  A - Turn Left (hold to continue)")
        print("  D - Turn Right (hold to continue)")
        print("  Q - Quit")
        print(f"  Speed: {int(self.BASE_SPEED*100)}% (turning: {int(self.TURN_SPEED*100)}%)")
        print()
        print("INSTRUCTIONS:")
        print("- Hold down keys for continuous movement")
        print("- Release key to stop that movement")
        print("- Motors stop automatically after 0.5s of no input")
        print("="*50)
        self.running = True
        self.current_action = "stop"
        self.last_key_time = time.time()
        motor_thread = threading.Thread(target=self.motor_control_loop, daemon=True)
        motor_thread.start()
        print("Press W/A/S/D keys. Press Q to quit.")
        print("Status: STOPPED")
        try:
            while self.running:
                char = self.get_char_non_blocking()
                if char:
                    self.last_key_time = time.time()
                    if char == 'q':
                        print("\nExiting real-time control...")
                        break
                    elif char == 'w':
                        self.current_action = "forward"
                        self._print_status()
                    elif char == 's':
                        self.current_action = "backward"
                        self._print_status()
                    elif char == 'a':
                        self.current_action = "left"
                        self._print_status()
                    elif char == 'd':
                        self.current_action = "right"
                        self._print_status()
                    elif char == '\x1b':
                        break
                time.sleep(0.02)
        except KeyboardInterrupt:
            print("\nControl interrupted")
        finally:
            self.running = False
            stop_all_motors()
            print("\nMotors stopped")
    def _print_status(self):
        status_map = {
            "forward": "FORWARD",
            "backward": "BACKWARD",
            "left": "TURN LEFT",
            "right": "TURN RIGHT",
            "stop": "STOPPED"
        }
        status = status_map.get(self.current_action, "UNKNOWN")
        print(f"\rStatus: {status}                    ", end="", flush=True)

def manual_control_simple():
    """Simple manual control with single key presses"""
    print("\nSimple Manual Control Mode:")
    print("Commands: w(forward), s(backward), a(left), d(right), x(stop), q(quit)")
    print("Note: Press enter after each command")
    
    while True:
        try:
            cmd = input("Enter command: ").strip().lower()
            if cmd == "q":
                break
            elif cmd == "w":
                move_forward(0.7)
                print("Moving forward...")
            elif cmd == "s":
                move_backward(0.7)
                print("Moving backward...")
            elif cmd == "a":
                turn_left(0.7)
                print("Turning left...")
            elif cmd == "d":
                turn_right(0.7)
                print("Turning right...")
            elif cmd == "x":
                stop_all_motors()
                print("Stopped")
            else:
                print("Invalid command. Use: w/s/a/d/x/q")
        except KeyboardInterrupt:
            break
    stop_all_motors()
    print("Manual control ended")

# Main execution for testing
if __name__ == "__main__":
    print("DC Motor Control with gpiozero")
    print("Pin Configuration:")
    print("  Motor A: ENA=18, IN1=23, IN2=24")
    print("  Motor B: ENB=25, IN3=12, IN4=16")
    print(f"  PWM Support: {'Available' if PWM_AVAILABLE else 'Not Available (Full speed only)'}")
    print(f"  GPIO Pins: {'Initialized' if PINS_INITIALIZED else 'Failed to Initialize'}")
    print()
    
    if not PINS_INITIALIZED:
        print("ERROR: GPIO pins failed to initialize!")
        print("This usually means:")
        print("1. Not running on a Raspberry Pi")
        print("2. Missing GPIO libraries")
        print("3. Permission issues")
        print()
        print("To fix this on Raspberry Pi:")
        print("  sudo apt update")
        print("  sudo apt install python3-rpi.gpio python3-pigpio")
        print("  # or")
        print("  pip install RPi.GPIO pigpio")
        print()
        print("Exiting...")
        exit(1)
    
    if not PWM_AVAILABLE:
        print("NOTE: Running without PWM support. Motors will run at full speed only.")
        print("To enable PWM, install proper GPIO libraries:")
        print("  sudo apt update")
        print("  sudo apt install python3-rpi.gpio python3-pigpio")
        print("  # or")
        print("  pip install RPi.GPIO pigpio")
        print()
    
    try:
        while True:
            print("\nSelect an option:")
            print("1. Test Motor A only")
            print("2. Test Motor B only")
            print("3. Test both motors")
            print("4. Run full test sequence")
            print("5. Real-time keyboard control (experimental)")
            print("6. Simple manual control (press enter)")
            print("0. Exit")
            
            choice = input("Enter choice (0-6): ").strip()
            
            if choice == "1":
                test_motor_a()
            elif choice == "2":
                test_motor_b()
            elif choice == "3":
                test_both_motors()
            elif choice == "4":
                run_full_test()
            elif choice == "5":
                controller = KeyboardController()
                controller.start_realtime_control()
            elif choice == "6":
                manual_control_simple()
            elif choice == "0":
                break
            else:
                print("Invalid choice")
    
    except KeyboardInterrupt:
        print("\nProgram interrupted")
    finally:
        cleanup()
        print("GPIO cleanup completed")
