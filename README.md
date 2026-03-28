# Timer-with-Clock-made-by-python
This is a timer with clock made by python.
The first version is made with 'Thinker' module. 
The following update is made with 'Pyside6' module. 

Python Version: 3.13

Module
---
Module needed-->pyside6, pytz, geocoder, geopy, TimezoneFinder

If you don't have these modules, copy this to your terminal: 
```bash
pip install pyside6 pytz geocoder geopy TimezoneFinder
```


Compile to .exe file
---
If you need to compile it into .exe file:
1. Open Terminal or PowerShell
2. Copy these to your shell

  ```bash
   cd "your/file/path/"
   ```
3. ```bash
   pyinstaller --noconsole --onefile --windowed --clean --icon=app_icon.ico Timer.py --version-file=dis.txt --add-data "setting.png;." --add-data "stopwatch.png;." --add-data "3158183.png;."
   ```

Patch
---
Patch 2.1:Bug Fixed - countdown timer, 1 extra second bug is fixed

Patch 3.0: New Function - World Clock

Patch 3.1: World Clock - Default Location is your city
Bug Fixed - World Clock, now the back button will go back to your previous page
