# About

This is web interface for Awasu application. It's used to browse and basic export articles. Without Awasu will not work and some functionalities will be broken.

https://awasu.com/

## Installation

pip install -r requirements.txt

Withoud it can't work. After that create file

#### config.py
Open awasu directory, change example config.py and put in root (app.py, manipulators.py locations).

#### Details how run read in Flask documentation:
https://flask.palletsprojects.com/en/1.1.x/quickstart/

Default:
C:\path\to\app>set FLASK_APP=hello.py
python -m flask run

or try simple:
python app.py (it's work for me on Windows 7)

Tested on Python 3.7.2 and 3.8.1

### Awasu configuration

---
Use JSON.template an Awasu => 3.2 from awasu directory:

#### Search Agents ####

If you like use Search Agents name it with prefix 'M > ' (add one with name in this convention to start working with, in other place [SA] option will be failed). If you curious why I use M. It is because M is from Meta as I see from beginning agregation a lot of channels in other one.

#### Performance ####
It's typical than when updating script is slowing down. Typical processing time on second generation i7 quad core with 32 GB RAM is below 120 sec to get data from Awasu.

## History
-
### 0.3
Create layout based on Pandas DataFrame as backend.

### 0.2

Add Flask as web server.

### 0.1

Static generated files. No webserver.

