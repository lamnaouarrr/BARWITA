#!/bin/bash

# GPIO Libraries Installation Script for Raspberry Pi
# This script installs the necessary GPIO libraries for proper PWM support

echo "Installing GPIO libraries for Raspberry Pi..."
echo "============================================="

# Update package list
echo "Updating package list..."
sudo apt update

# Install system GPIO libraries
echo "Installing system GPIO libraries..."
sudo apt install -y python3-rpi.gpio python3-pigpio python3-lgpio

# Install pip versions in virtual environment if active
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Virtual environment detected: $VIRTUAL_ENV"
    echo "Installing GPIO libraries in virtual environment..."
    pip install RPi.GPIO pigpio lgpio
else
    echo "No virtual environment detected."
    echo "You can install GPIO libraries globally with:"
    echo "  sudo pip3 install RPi.GPIO pigpio lgpio"
    echo "Or activate your virtual environment first."
fi

# Enable pigpio daemon
echo "Enabling pigpio daemon..."
sudo systemctl enable pigpiod
sudo systemctl start pigpiod

echo ""
echo "Installation complete!"
echo "Libraries installed:"
echo "  - RPi.GPIO (Raspberry Pi GPIO library)"
echo "  - pigpio (Advanced GPIO library with better PWM)"
echo "  - lgpio (Modern GPIO library)"
echo ""
echo "You can now run your motor control script with proper PWM support."
echo "Restart your Python script to use the new libraries."
