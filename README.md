# BARWITA

**B**uilding **A** **R**emote-Controlled Car **W**ith **I**nternet **T**echnology and **A**utomation

BARWITA is a comprehensive remote-controlled car project powered by a Raspberry Pi 4 Model B. This project integrates motor control, camera streaming, 4G connectivity, and a web-based interface to enable seamless remote operation and real-time monitoring over the internet. Whether you're a hobbyist diving into robotics or an enthusiast expanding your IoT skills, BARWITA offers a hands-on guide to building and customizing your own internet-connected smart car.

## Introduction

BARWITA is designed to provide a comprehensive experience in building an advanced remote-controlled car with internet connectivity. Leveraging the power of the Raspberry Pi 4, this project encompasses hardware assembly, software development, network configuration, and web interface design. The goal is to create a robust platform that can be controlled remotely from anywhere in the world using 4G connectivity, with real-time camera streaming and vehicle telemetry.

The project follows a structured 12-week development roadmap, progressing from basic hardware assembly to advanced features like internet control, sensor integration, and a game-like web interface.

## Project Components

### Hardware Components
- **Raspberry Pi 4 Model B** - Main control unit
- **DC Motors** - Vehicle propulsion system
- **Motor Driver** - DC motor control interface
- **Servo Motors** - Camera pan/tilt mechanism
- **Raspberry Pi Camera Module V2** - Live video streaming
- **Waveshare Air780E 4G Module** - Internet connectivity (*not yet assembled*)
- **TFT LCD Screen** - Local display interface (*not yet assembled*)
- **LEDs** - Status indicators (*not yet assembled*)
- **Switch** - Power/control switching (*not yet assembled*)
- **Toy Car Chassis** - Vehicle frame
- **Breadboard and Jumper Wires** - Electrical connections
- **Power Supply** - System power management

### Software Components
- **Raspberry Pi OS** - Operating system
- **WebIOPi** - Web-based GPIO control framework
- **mjpg-streamer** - Camera streaming service (*planned*)
- **Custom Python Scripts** - Motor and servo control logic

## Getting Started

### Prerequisites

Before beginning, ensure you have the following:

**Hardware Requirements:**
- All components listed above
- MicroSD Card (16GB or larger, Class 10 recommended)
- MicroSD Card Reader
- Ethernet Cable
- Computer with internet access
- Multimeter for testing connections

**Software Requirements:**
- [Raspberry Pi Imager](https://www.raspberrypi.org/software/)
- SSH client (PuTTY for Windows, Terminal for macOS/Linux)
- Git for version control

### Installation

1. **Flash Raspberry Pi OS:**
   - Use Raspberry Pi Imager to flash Raspberry Pi OS onto the microSD card
   - Configure Wi-Fi settings during installation (SSID, password, country code: CN)
   - Enable SSH for remote access

2. **Initial System Setup:**
   - Insert microSD card into Raspberry Pi 4 Model B
   - Connect Ethernet cable for initial setup
   - Power up the system
   - Access via SSH (hostname: `barwita`, IP: `192.168.1.223`)

3. **Install WebIOPi:**
   - Download and install WebIOPi framework
   - Initialize Git repository in `~/Desktop/WebIOPi-0.7.1/BARWITA`

## Project Roadmap

### ✅ Week 1-2: Hardware Setup (COMPLETED)
- **Completed Tasks:**
  - Assembled toy car chassis with DC motors and wheels
  - Mounted Raspberry Pi 4 Model B and motor driver
  - Installed servo motors for camera positioning
  - Connected Raspberry Pi Camera Module V2
  - Established breadboard connections with jumper wires
  - Tested all connections with multimeter
  - Flashed and configured Raspberry Pi OS
  - Set up Ethernet/Wi-Fi connectivity (hostname: `barwita`, IP: `192.168.1.223`, country: `CN`)
  - Installed WebIOPi framework
  - Initialized Git repository in `~/Desktop/WebIOPi-0.7.1/BARWITA`

### 🔄 Week 3: Install and Configure WebIOPi (IN PROGRESS)
- **Current Tasks:**
  - Creating `BARWITA` project folder structure
  - Setting up GitHub repository integration
  - Configuring GPIO pins for motor control
  - Configuring GPIO pins for servo control
  - Configuring GPIO pins for LED indicators
  - Setting up basic web interface framework

### 📋 Week 4: Integrate Camera Streaming (PLANNED)
- Install and configure mjpg-streamer
- Embed camera stream into WebIOPi interface
- Test real-time video streaming functionality

### 📋 Week 5: Implement Motor and Servo Control (PLANNED)
- Adapt and integrate motor driver control code
- Program servo motors for camera pan/tilt functionality
- Implement directional movement controls (forward, backward, left, right)

### 📋 Week 6: Enable Internet Control with 4G (PLANNED)
- Assemble and configure Waveshare Air780E 4G module
- Establish internet connectivity through cellular network
- Enable remote access from external networks
- Configure port forwarding and security protocols

### 📋 Week 7-8: Develop Game-Like Interface (PLANNED)
- Customize WebIOPi dashboard with advanced controls
- Implement real-time statistics display (battery level, speed, connection status)
- Create responsive web interface for mobile and desktop access

### 📋 Week 9: Add Sensors for Stats (PLANNED)
- Integrate voltage sensor for battery monitoring
- Optional: Add rotary encoders for speed measurement
- Optional: Integrate GPS module for location tracking
- Assemble TFT LCD screen for local status display

### 📋 Week 10-11: Testing and Optimization (PLANNED)
- Comprehensive system testing under various conditions
- Performance optimization and bug fixes
- Interface refinement and user experience improvements
- Assemble and integrate remaining components (LEDs, switch)

### 📋 Week 12: Final Deployment (PLANNED)
- Implement secure connection protocols
- Complete project documentation with diagrams and guides
- Create demonstration videos
- Prepare final project showcase

## Current Status

**Hardware Assembly:** Core components (Raspberry Pi, motors, camera, servo) are assembled and functional. Waveshare Air780E 4G module, TFT LCD screen, LEDs, and switch are not yet integrated into the system.

**Software Development:** Raspberry Pi OS is configured with WebIOPi installed. Currently working on GPIO configuration and basic web interface setup.

**Network Configuration:** Local network connectivity established. Internet connectivity via 4G module planned for Week 6.

## Future Documentation

As BARWITA progresses through its development phases, detailed documentation will be added:

- **Hardware Assembly Guides:** Step-by-step instructions with wiring diagrams
- **Software Configuration:** Detailed setup procedures and code explanations  
- **API Documentation:** WebIOPi interface and control endpoints
- **Troubleshooting Guide:** Common issues and solutions
- **Enhancement Tutorials:** Adding new features and capabilities

## Contributing

Contributions are welcome! If you have suggestions, improvements, or additional features to propose, feel free to open an issue or submit a pull request.

1. Fork the Repository
2. Create a Feature Branch (`git checkout -b feature/YourFeature`)
3. Commit Your Changes (`git commit -m "Add Your Feature"`)
4. Push to the Branch (`git push origin feature/YourFeature`)  
5. Open a Pull Request

Please ensure that your contributions adhere to the project's coding standards and include appropriate documentation.

## License

This project is licensed under the [MIT License](LICENSE).

---

*Last Updated: Week 3 - WebIOPi Configuration Phase*
