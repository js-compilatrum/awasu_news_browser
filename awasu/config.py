"""
    It is main config file
"""

# Main config file
DEBUG = False  # Set to test mode

# Data sources
CSV_BASE_SOURCE = r'PATH_WHERE_YOUR_SOURCE_JSON_IS_SAVED_all_unread_channels.json'
TEST_DATA = r'PATH_TO_TEST_FILE_test.json'
FILE_WTIH_DATA_TO_DATABASE = TEST_DATA if DEBUG else CSV_BASE_SOURCE

# Viewing
RESULT_PER_PAGE = 100
LATEST_ARTICLES_NUMBER = 100

# Awasu API
AWASU_API_KEYS = ['channelFolder', 'channels']
AWASU_API: str = "http://localhost:2604"  # URL for Awasu
TOKEN: str = "TOKEN_FROM_AWASU"