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
        self.keys_pressed = set()
        self.speed = 0.7
        
    def get_char(self):
        """Get a single character from stdin without waiting for enter"""
        try:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.cbreak(fd)
                if select.select([sys.stdin], [], [], 0.1) == ([sys.stdin], [], []):
                    ch = sys.stdin.read(1)
                    return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except:
            # Fallback for non-Unix systems or when termios is not available
            return None
        return None
    
    def motor_control_loop(self):
        """Continuous motor control based on pressed keys"""
        while self.running:
            if not PINS_INITIALIZED:
                time.sleep(0.1)
                continue
                
            # Check current key states and control motors accordingly
            if 'w' in self.keys_pressed and 's' not in self.keys_pressed:
                # Forward
                self._move_forward_raw()
            elif 's' in self.keys_pressed and 'w' not in self.keys_pressed:
                # Backward
                self._move_backward_raw()
            elif 'd' in self.keys_pressed and 'a' not in self.keys_pressed:
                # Turn right (right wheel backward, left wheel forward)
                self._turn_right_raw()
            elif 'a' in self.keys_pressed and 'd' not in self.keys_pressed:
                # Turn left (left wheel backward, right wheel forward)
                self._turn_left_raw()
            elif 'w' in self.keys_pressed and 'd' in self.keys_pressed:
                # Forward-right (slight right turn while moving forward)
                self._move_forward_right_raw()
            elif 'w' in self.keys_pressed and 'a' in self.keys_pressed:
                # Forward-left (slight left turn while moving forward)
                self._move_forward_left_raw()
            elif 's' in self.keys_pressed and 'd' in self.keys_pressed:
                # Backward-right
                self._move_backward_right_raw()
            elif 's' in self.keys_pressed and 'a' in self.keys_pressed:
                # Backward-left
                self._move_backward_left_raw()
            else:
                # No movement keys pressed, stop motors
                self._stop_raw()
            
            time.sleep(0.05)  # 20Hz update rate
    
    def _move_forward_raw(self):
        """Raw forward movement without error checking"""
        try:
            IN1.on(); IN2.off(); IN3.on(); IN4.off()
            if PWM_AVAILABLE:
                ENA.value = self.speed; ENB.value = self.speed
            else:
                ENA.on(); ENB.on()
        except: pass
    
    def _move_backward_raw(self):
        """Raw backward movement without error checking"""
        try:
            IN1.off(); IN2.on(); IN3.off(); IN4.on()
            if PWM_AVAILABLE:
                ENA.value = self.speed; ENB.value = self.speed
            else:
                ENA.on(); ENB.on()
        except: pass
    
    def _turn_right_raw(self):
        """Raw right turn (left motor forward, right motor backward)"""
        try:
            IN1.on(); IN2.off(); IN3.off(); IN4.on()
            if PWM_AVAILABLE:
                ENA.value = self.speed; ENB.value = self.speed
            else:
                ENA.on(); ENB.on()
        except: pass
    
    def _turn_left_raw(self):
        """Raw left turn (left motor backward, right motor forward)"""
        try:
            IN1.off(); IN2.on(); IN3.on(); IN4.off()
            if PWM_AVAILABLE:
                ENA.value = self.speed; ENB.value = self.speed
            else:
                ENA.on(); ENB.on()
        except: pass
    
    def _move_forward_right_raw(self):
        """Forward with slight right turn"""
        try:
            IN1.on(); IN2.off(); IN3.on(); IN4.off()
            if PWM_AVAILABLE:
                ENA.value = self.speed; ENB.value = self.speed * 0.6  # Slow down right motor
            else:
                ENA.on(); ENB.on()
        except: pass
    
    def _move_forward_left_raw(self):
        """Forward with slight left turn"""
        try:
            IN1.on(); IN2.off(); IN3.on(); IN4.off()
            if PWM_AVAILABLE:
                ENA.value = self.speed * 0.6; ENB.value = self.speed  # Slow down left motor
            else:
                ENA.on(); ENB.on()
        except: pass
    
    def _move_backward_right_raw(self):
        """Backward with slight right turn"""
        try:
            IN1.off(); IN2.on(); IN3.off(); IN4.on()
            if PWM_AVAILABLE:
                ENA.value = self.speed; ENB.value = self.speed * 0.6
            else:
                ENA.on(); ENB.on()
        except: pass
    
    def _move_backward_left_raw(self):
        """Backward with slight left turn"""
        try:
            IN1.off(); IN2.on(); IN3.off(); IN4.on()
            if PWM_AVAILABLE:
                ENA.value = self.speed * 0.6; ENB.value = self.speed
            else:
                ENA.on(); ENB.on()
        except: pass
    
    def _stop_raw(self):
        """Raw stop without error checking"""
        try:
            IN1.off(); IN2.off(); IN3.off(); IN4.off()
            ENA.off(); ENB.off()
        except: pass
    
    def start_realtime_control(self):
        """Start real-time keyboard control"""
        if not PINS_INITIALIZED:
            print("Error: GPIO pins not initialized")
            return
        
        print("\n" + "="*50)
        print("REAL-TIME KEYBOARD CONTROL")
        print("="*50)
        print("Controls:")
        print("  W - Forward")
        print("  S - Backward") 
        print("  A - Turn Left")
        print("  D - Turn Right")
        print("  W+A - Forward Left")
        print("  W+D - Forward Right")
        print("  S+A - Backward Left")
        print("  S+D - Backward Right")
        print("  Q - Quit")
        print(f"  Speed: {self.speed * 100:.0f}%")
        print()
        print("Hold keys to move continuously...")
        print("Press Q to exit")
        print("="*50)
        
        self.running = True
        
        # Start motor control thread
        motor_thread = threading.Thread(target=self.motor_control_loop, daemon=True)
        motor_thread.start()
        
        try:
            while self.running:
                char = self.get_char()
                if char:
                    char = char.lower()
                    
                    if char == 'q':
                        print("\nExiting real-time control...")
                        break
                    elif char in ['w', 'a', 's', 'd']:
                        if char not in self.keys_pressed:
                            self.keys_pressed.add(char)
                            self._print_status()
                    elif char == '\x1b':  # ESC key
                        break
                
                # Check if keys are still being held (this is a simplified approach)
                # In a real implementation, you'd need proper key release detection
                time.sleep(0.02)
                
        except KeyboardInterrupt:
            print("\nControl interrupted")
        finally:
            self.running = False
            self._stop_raw()
            print("Motors stopped")
    
    def _print_status(self):
        """Print current movement status"""
        if not self.keys_pressed:
            print("Status: STOPPED")
        else:
            keys_str = '+'.join(sorted(self.keys_pressed)).upper()
            print(f"Status: {keys_str}")

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
            print("5. Real-time keyboard control (hold keys)")
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
