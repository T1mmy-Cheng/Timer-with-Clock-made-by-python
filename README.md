# Timer-with-Clock-made-by-python
This is a timer with clock made by python.
The first version is made with 'Thinker' module. 
The following update is made with 'Pyside6' module. 

-Python Version: 3.13

Module
---
**Module needed:**
- pyside6
- pytz
- geocoder
- geopy
- TimezoneFinder

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all needed modules. 
```bash
pip install pyside6 pytz geocoder geopy TimezoneFinder
```


Compile to .exe file
---
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pyinstaller
```bash
pip install pyinstaller
```

If you need to compile it into .exe file:
1. Open Terminal or PowerShell
2. Navigate to your file path
   ```bash
   cd "your/file/path/"
   ```
3. Compile it
   ```bash
   pyinstaller --clean Timer.spec
   ```

Patch
---
Patch 2.1:Bug Fixed - countdown timer, 1 extra second bug is fixed

Patch 3.0: New Function - World Clock

Patch 3.1: World Clock - Default Location is your city
Bug Fixed - World Clock, now the back button will go back to your previous page

Sample
---
[Main page](image.png)
