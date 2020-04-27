"""
    It is main config file
"""

# Main config file
DEBUG = False  # Set to test mode

# Data sources
CSV_BASE_SOURCE = r'D:\Pliki z danymi\Bieżące przedsięwzięcia\Awasu\Raporty\json\all_unread_channels.json'
TEST_DATA = r'D:\Pliki z danymi\Bieżące przedsięwzięcia\Awasu\Raporty\json\test.json'
FILE_WTIH_DATA_TO_DATABASE = TEST_DATA if DEBUG else CSV_BASE_SOURCE

# Viewing
RESULT_PER_PAGE = 100
LATEST_ARTICLES_NUMBER = 100

# Awasu API
AWASU_API_KEYS = ['channelFolder', 'channels']
AWASU_API: str = "http://localhost:2604"  # nb: get this from config.py
TOKEN: str = "GYmh3B"