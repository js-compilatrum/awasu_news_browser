'''
It's is Awasu simple config file. Put in in the same place where you can find out app.py and manipulators.py
'''
EXIST_DATA = True
PUB_DIR = r'D:\pub'  # Where save selected articles by Flask
NEWS_PER_PAGE = 500  # articles per page
LOCALHOST_URL = "http://127.0.0.1:5000"  # Use default from Flask serving or unicorn

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

'''
CONCEPT_DEBUG = False  # For normal work set to False, True if you like used prepared data
CSV_BASE_SOURCE = r'D:\awasu\all_unread_channels.json'  # Here ara articles saved from Awasu
''' 
It's important to use path configured in Awasu Reports creator or it will not be working
'''
CSV_TEST_DATA = r'D:\concept_debug.csv'  # Here are test data
'''
Warning!

In future release variable will be renamed as based format is change from CSV to JSON. Variable name is not
longer correct.
'''
OUTPUT_DIR = r'D:\selected'  # Where save selected articles as txt and csv
OPEN_IN_BROWSER_EVERYTIME = True  # If run in browser open interface in default browser
SEARCH_AGENT_PREFIX = "M >"
''' All channels name started with "M >" like "M > Continents" are matches as Search Agents.'''

# Security
TOKEN = "abc123"

# Awasu settings
AWASU_API_URL = "http://localhost:2604/"
AWASU_DEFAULT_CONFIG_PATH = r'C:\Users\User\AppData\Roaming\Awasu\config.ini'
