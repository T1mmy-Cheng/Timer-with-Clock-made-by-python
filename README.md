# Timer with Analog Clock

A feature-rich desktop application built with Python and PySide6, featuring a traditional analog interface alongside digital precision.

## 🌟 Features

* **Dual Interface**: View time through a smooth-motion analog clock or a clear digital display.
* **Three-in-One Utility**: Includes a Countdown Timer, a high-precision Stopwatch with lap recording, and a World Clock.
* **Smart World Clock**: Automatically detects your local timezone (e.g., Hong Kong) and allows you to browse and view times across the globe.
* **Adaptive Themes**: Supports both Light and Dark modes, with the ability to detect your system's preference automatically.
* **Professional Metadata**: Fully compiled with version information and copyright details.

## 🛠️ Installation

### Prerequisites
* Python 3.13+
* Dependencies: `PySide6`, `darkdetect`, `pytz`, `geocoder`, `geopy`, `timezonefinder`.

### Setup
1. Clone the repository or download the source files.
2. Install the required packages:
   ```bash
   pip install PySide6 darkdetect pytz geocoder geopy timezonefinder
   ```
3. Run the application:
   ```bash
   python Timer.py
   ```

## 📦 Building the Executable

To create a standalone Windows executable (`.exe`) with the custom icon and version metadata:

1. Install pyinstaller for compiling:
   ```powershell
   pip install pyinstaller 
   ```
2. Navigate the source files:
   ```powershell
   cd "your/file/path/"
   ```
3. Compiling to a standalone Windows executable (`.exe`) file:
   ```powershell
   pyinstaller --clean Timer.spec
   ```

## 📝 File Information

* **Product Name**: Timer.exe
* **Internal Name**: timer_by_pyside
* **Current Version**: 3.1.0.0
* **Developer**: Timmy Cheng

## 📜 License

© 2025-2026 Timmy Cheng. All rights reserved.


## Sample

[Main page](image.png)
