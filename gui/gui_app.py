import tkinter as tk
import requests
import time

# Replace with your Pi’s IP and port.
PI_IP = "192.168.10.100"
PORT = 5000

# Speed increments and delay
SPEED_INCREMENT = 10  # Increment speed by 5% every time the key is pressed
SPEED_DELAY = 1    # Delay in seconds between each speed update

current_speed = 0  # Current speed (0 to 100)

def send_command(endpoint, speed=None):
    """
    Sends a POST request to the Pi's Flask endpoint.
    Optionally includes a speed in the JSON payload.
    """
    url = f"http://{PI_IP}:{PORT}/{endpoint}"
    payload = {}
    if speed is not None:
        payload["speed"] = speed
    try:
        resp = requests.post(url, json=payload)
        print(f"Sent {endpoint} (speed={speed}), got response:", resp.json())
    except requests.exceptions.RequestException as e:
        print(f"Error sending {endpoint}: {e}")

def forward():
    """Send forward command."""
    global current_speed
    if current_speed < 100:
        current_speed += SPEED_INCREMENT  # Increase speed gradually
    send_command("forward", current_speed)

def backward():
    """Send backward command."""
    global current_speed
    if current_speed < 100:
        current_speed += SPEED_INCREMENT  # Increase speed gradually
    send_command("backward", current_speed)

def stop():
    """Stop motors."""
    global current_speed
    current_speed = 0
    send_command("stop")

def key_press_repeat(event):
    """Handle repeated key presses for gradual speed increase."""
    key = event.keysym.lower()
    if key == 'w':
        forward()
    elif key == 's':
        backward()

def on_key_press(event):
    """Start the speed increase when key is pressed."""
    key_press_repeat(event)
    root.after(int(SPEED_DELAY * 1000), key_press_repeat, event)

def on_key_release(event):
    """Stop the motors when the key is released."""
    stop()

# Build the GUI
root = tk.Tk()
root.title("BARWITA Keyboard Control")

info_label = tk.Label(root, text="Hold W for Forward, S for Backward.\nRelease to Stop.")
info_label.pack(padx=20, pady=20)

# We bind keypress and keyrelease to the root window
root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)

root.mainloop()
