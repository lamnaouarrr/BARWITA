#!/bin/bash

# mjpg-streamer startup script for Raspberry Pi camera
# Streams video on port 8080

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting mjpg-streamer for Raspberry Pi camera...${NC}"

# Load camera module if needed
echo -e "${YELLOW}Loading camera module...${NC}"
sudo modprobe bcm2835-v4l2

# Wait a moment for the module to load
sleep 2

# Check if camera is available
if [ ! -e /dev/video0 ]; then
    echo -e "${RED}Error: Camera not found at /dev/video0${NC}"
    echo "Please check if the camera is properly connected and enabled in raspi-config"
    exit 1
fi

echo -e "${GREEN}Camera detected at /dev/video0${NC}"

# Kill any existing mjpg-streamer processes
echo -e "${YELLOW}Stopping any existing mjpg-streamer processes...${NC}"
sudo pkill -f mjpg_streamer

# Start mjpg-streamer
echo -e "${GREEN}Starting mjpg-streamer on port 8080...${NC}"
mjpg_streamer \
    -i "input_uvc.so -d /dev/video0 -r 640x480 -f 30" \
    -o "output_http.so -p 8080 -w /usr/local/share/mjpg-streamer/www" &

# Store the process ID
MJPG_PID=$!

# Wait a moment and check if the process is still running
sleep 3

if ps -p $MJPG_PID > /dev/null; then
    echo -e "${GREEN}mjpg-streamer started successfully!${NC}"
    echo -e "${GREEN}Stream available at: http://$(hostname -I | awk '{print $1}'):8080${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop the stream${NC}"
    
    # Wait for the process to finish or be interrupted
    wait $MJPG_PID
else
    echo -e "${RED}Failed to start mjpg-streamer${NC}"
    echo "Please check if mjpg-streamer is installed:"
    echo "sudo apt update && sudo apt install mjpg-streamer"
    exit 1
fi

echo -e "${YELLOW}mjpg-streamer stopped${NC}"