import tkinter as tk
import requests

# Replace with your Pi’s IP and port.
PI_IP = "192.168.10.100"
PORT = 5000

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

def forward(speed=70):
    """Send forward command."""
    send_command("forward", speed)

def backward(speed=70):
    """Send backward command."""
    send_command("backward", speed)

def stop():
    """Stop motors."""
    send_command("stop")

# Key event handlers

def on_key_press(event):
    """
    Called when any key is pressed. We check if it's 'w' or 's'
    and issue the corresponding motor command.
    """
    key = event.keysym.lower()  # e.g. 'W' -> 'w'
    if key == 'w':
        forward(70)  # adjust speed if needed
    elif key == 's':
        backward(70)

def on_key_release(event):
    """
    Called when any key is released. If it's 'w' or 's', we stop motors.
    """
    key = event.keysym.lower()
    if key in ['w', 's']:
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
