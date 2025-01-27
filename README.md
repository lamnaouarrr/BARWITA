# BARWITA


**BARWITA** is a remote-controlled car project powered by a Raspberry Pi 4 Model B. This project integrates motor control, camera streaming, and a graphical user interface (GUI) to enable seamless remote operation and real-time monitoring. Whether you're a hobbyist looking to dive into robotics or an enthusiast aiming to expand your IoT skills, BARWITA offers a comprehensive guide to building and customizing your own smart car.

---

## Table of Contents

- [BARWITA](#barwita)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
      - [1. Flash Raspberry Pi OS to the MicroSD Card](#1-flash-raspberry-pi-os-to-the-microsd-card)
      - [2. Initial Headless Setup Using Ethernet](#2-initial-headless-setup-using-ethernet)
  - [Project Roadmap](#project-roadmap)
  - [Future Documentation](#future-documentation)
  - [Contributing](#contributing)
  - [License](#license)

---

## Introduction

BARWITA is designed to provide a hands-on experience in building a remote-controlled car with advanced features. Leveraging the power of the Raspberry Pi 4, this project encompasses various aspects of hardware assembly, software development, and network configuration. The goal is to create a robust platform that can be expanded with additional functionalities such as obstacle avoidance, autonomous navigation, and more.

---

## Getting Started

Follow these instructions to set up the initial configuration of BARWITA. This guide covers the essential steps to prepare your Raspberry Pi for headless operation, allowing you to manage it remotely without the need for a connected monitor, keyboard, or mouse.

### Prerequisites

Before you begin, ensure you have the following hardware and software components:

- **Hardware:**
  - Raspberry Pi 4 Model B (4GB RAM recommended)
  - microSD Card (16GB or larger, Class 10 recommended)
  - MicroSD Card Reader
  - Ethernet Cable (for initial setup)
  - Computer with internet access
  - USB Power Supply for Raspberry Pi
  - Optional: Wi-Fi adapter (if not using built-in Wi-Fi)

- **Software:**
  - [Raspberry Pi Imager v1.8.5](https://www.raspberrypi.org/software/)
  - [PuTTY](https://www.putty.org/) (for Windows users)
  - [Angry IP Scanner](https://angryip.org/) (for network scanning)

### Installation

#### 1. Flash Raspberry Pi OS to the MicroSD Card

1. **Download Raspberry Pi OS:**
   - Visit the [Raspberry Pi Downloads](https://www.raspberrypi.org/software/operating-systems/) page.
   - Download the **Raspberry Pi OS Lite** version for a minimal setup.

2. **Install Raspberry Pi Imager:**
   - Download and install [Raspberry Pi Imager v1.8.5](https://www.raspberrypi.org/software/) on your computer.

3. **Set Up Wi-Fi during Raspberry Pi OS Installation:**
   - Open **Raspberry Pi Imager**.
   - Select **Raspberry Pi OS Lite** as the operating system.
   - Choose the microSD card as the storage device.
   - Click on the **gear icon** (Advanced Options) to open the configuration menu.
   - Enable **Set Wi-Fi SSID and Password**.
   - Enter your **Wi-Fi SSID** and **Wi-Fi Password**.
   - Set the **Country Code** (for example, `CN` for China).
   - Optionally, enable **SSH** to allow remote access.
   - Click **Save** and then **Write** to flash the OS onto the SD card.
   - Wait for the process to complete and safely eject the SD card.

#### 2. Initial Headless Setup Using Ethernet

1. **Insert the microSD Card:**
   - Place the flashed microSD card into your Raspberry Pi 4 Model B.

2. **Connect Ethernet Cable:**
   - Plug in the Ethernet cable from your Raspberry Pi to your router or switch. This ensures internet connectivity during the initial setup.

3. **Power Up the Raspberry Pi:**
   - Connect the USB power supply to boot up the Raspberry Pi.

4. **Find the Raspberry Pi’s IP Address:**
   - Open **Angry IP Scanner** on your computer.
   - Scan your local network to identify the Raspberry Pi's IP address. For example, `192.168.10.50`.

5. **Connect via SSH Using PuTTY (Windows) or Terminal (macOS/Linux):**
   - **Windows:**
     - Open **PuTTY**.
     - Enter the IP address (e.g., `192.168.10.50`) in the "Host Name" field.
     - Click **"Open"** to initiate the connection.
   - **macOS/Linux:**
     - Open **Terminal**.
     - Enter the command:
       ```bash
       ssh pi@192.168.10.50
       ```
     - Press **Enter**.

6. **Authenticate:**
   - **Username:** `pi`
   - **Password:** `raspberry`
   - **Note:** It is highly recommended to change the default password immediately after the first login for security purposes.

---

## Project Roadmap

BARWITA is structured to guide you through the development of a fully functional remote-controlled car. Below is a high-level overview of the project's roadmap, with detailed documentation to be filled in as each phase progresses.

### **Phase 1: Headless Raspberry Pi Setup**
- **Completed:**
  - Installed Raspberry Pi OS on the microSD card.
  - Configured initial internet access via Ethernet.
  - Established headless SSH access using PuTTY.
  - Configured Wi-Fi for wireless headless operation during installation.
  - Assigned a static IP address to the Raspberry Pi.

### **Phase 2: Physical Assembly of the Car**
- Mounting DC motors, wheels, Raspberry Pi, motor driver, TFT LCD screen, and other components onto the chassis.
- Establishing basic wiring setups for motor control and power management.

### **Phase 3: Software Development**
- Developing Python scripts for motor control, enabling forward, backward, left, and right movements.
- Setting up camera streaming using the Raspberry Pi Camera Module V2.
- Creating a graphical user interface (GUI) for remote control.

### **Phase 4: Communication Protocols**
- Establishing communication between the PC and Raspberry Pi using Flask APIs or WebSockets.
- Ensuring real-time command transmission and feedback.

### **Phase 5: Integration and Testing**
- Combining all software components and testing their interactions.
- Conducting comprehensive tests to ensure reliability and performance.

### **Phase 6: Advanced Features (Future Expansion)**
- Implementing obstacle avoidance using ultrasonic sensors.
- Developing autonomous navigation capabilities.
- Enhancing security features for communication protocols.
- Adding battery level indicators and power management optimizations.

### **Phase 7: Documentation and Deployment**
- Finalizing project documentation, including wiring diagrams and code explanations.
- Recording demonstration videos showcasing BARWITA’s functionalities.
- Preparing the project for inclusion in professional portfolios and GitHub repositories.

---

## Future Documentation

As BARWITA progresses through its development phases, detailed documentation will be added to guide users through each step. This includes:

- **Hardware Assembly Guides:** Step-by-step instructions with images for mounting components.
- **Software Tutorials:** Detailed explanations of Python scripts and GUI development.
- **Network Configuration:** Advanced network setups for robust remote access.
- **Troubleshooting:** Common issues and their resolutions.
- **Enhancements:** Guides for adding new features and optimizing performance.

---

## Contributing

Contributions are welcome! If you have suggestions, improvements, or additional features to propose, feel free to open an issue or submit a pull request.

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/YourFeature
   ```
3. **Commit Your Changes**
   ```bash
   git commit -m "Add Your Feature"
   ```
4. **Push to the Branch**
   ```bash
   git push origin feature/YourFeature
   ```
5. **Open a Pull Request**

Please ensure that your contributions adhere to the project's coding standards and include appropriate documentation.

---

## License

This project is licensed under the [MIT License](LICENSE).
