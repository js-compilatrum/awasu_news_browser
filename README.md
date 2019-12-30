# About

This is web interface for Awasu application. It's used to browse and basic export articles. Without Awasu will not work and some functionalities will be broken.

https://awasu.com/

## Installation

pip install requirements.txt

Withoud it can't work. After that create file

#### config.py
----
with positions like that:


EXIST_DATA = True
PUB_DIR = r'D:\pub'  # Where save selected articles by Flask
NEWS_PER_PAGE = 500 # articles per page
LOCALHOST_URL = "http://127.0.0.1:5000" # Use default from Flask serving or unicorn

BASE_SETTINGS_DIR = r'D:\py-module\settings'  # Settings dir

'''
Create at this dir txt file fx. ch_list_process.txt and put names of channels to use fx.

Box Office Mojo - Current Box Office Results
Box Office Mojo - Top Stories
CNS Movie Reviews
ComingSoon.net
Latest Movie Metascores on Metacritic
Movies – NewNowNext
New Movies In Theaters - IMDb


Default files are:
    ch_list_movies.txt
    ch_list_process.txt
    ch_process_list_lvl_2.txt


'''
CONCEPT_DEBUG = False # Debug, set True to use CSV_TEST_DATA
CSV_BASE_SOURCE = r'D:\json\all_unread_channels.json'  ##### Here ara articles saved from Awasu
CSV_TEST_DATA = r'D:\csv\concept_debug.csv'  ##### Here are test articles
OUTPUT_DIR = r'D:\articles\selected'  ##### Where save selected articles as txt and csv

TOKEN = "secret_Awasu_API_token"

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

If you like use Search Agents name it with prefix 'M > '. If you curious why I use M. It is because M is from Meta as I see from beginning agregation a lot of channels in other one.

#### Performance ####
It's typical than when updating script is slowing down. Typical processing time on second generation i7 quad core with 32 GB RAM is below 120 sec to get data from Awasu.

## History
-
### 0.1

Static generated files. No webserver.

### 0.2

Add Flask as web server.