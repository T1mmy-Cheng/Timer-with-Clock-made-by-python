# Timer with Analog Clock

[cite_start]A feature-rich desktop application built with Python and PySide6, featuring a traditional analog interface alongside digital precision. [cite: 1]

## 🌟 Features

* [cite_start]**Dual Interface**: View time through a smooth-motion analog clock or a clear digital display. [cite: 1]
* [cite_start]**Three-in-One Utility**: Includes a Countdown Timer, a high-precision Stopwatch with lap recording, and a World Clock. [cite: 1]
* [cite_start]**Smart World Clock**: Automatically detects your local timezone (e.g., Hong Kong) and allows you to browse and view times across the globe. [cite: 1]
* [cite_start]**Adaptive Themes**: Supports both Light and Dark modes, with the ability to detect your system's preference automatically. [cite: 1]
* [cite_start]**Professional Metadata**: Fully compiled with version information and copyright details. [cite: 2]

## 🛠️ Installation

### Prerequisites
* Python 3.13+
* [cite_start]Dependencies: `PySide6`, `darkdetect`, `pytz`, `geocoder`, `geopy`, `timezonefinder`. [cite: 1]

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

[cite_start]To create a standalone Windows executable (`.exe`) with the custom icon and version metadata: [cite: 2]

```powershell
pyinstaller --noconsole --onefile --windowed --clean `
--icon="app_icon.ico" `
--version-file="dis.txt" `
--add-data "app_icon.ico;." `
--add-data "setting.png;." `
--add-data "stopwatch.png;." `
--add-data "3158183.png;." `
Timer.py
```

## 📝 File Information

* [cite_start]**Product Name**: Desktop Timer [cite: 2]
* [cite_start]**Internal Name**: timer_by_pyside [cite: 1, 2]
* [cite_start]**Current Version**: 3.1.0.0 [cite: 1, 2]
* [cite_start]**Developer**: Timmy Cheng [cite: 1, 2]

## 📜 License

© 2025-2026 Timmy Cheng. [cite_start]All rights reserved. [cite: 1, 2]

## Patch

Patch 2.1:Bug Fixed - countdown timer, 1 extra second bug is fixed

Patch 3.0: New Function - World Clock

Patch 3.1: World Clock - Default Location is your city
Bug Fixed - World Clock, now the back button will go back to your previous page

##Sample

[Main page](image.png)
