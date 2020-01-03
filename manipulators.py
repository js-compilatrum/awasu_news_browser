import json
from collections import namedtuple
from os import listdir
from os import path
import re

import arrow
# import modin.pandas as pd # this line enable multi core support for Pandas: https://modin.readthedocs.io/en/latest/
import pandas as pd
import requests
from tqdm import tqdm

from config import AWASU_API_URL
from config import AWASU_DEFAULT_CONFIG_PATH
from config import BASE_SETTINGS_DIR
from config import CONCEPT_DEBUG
from config import CSV_BASE_SOURCE
from config import CSV_TEST_DATA
from config import TOKEN

CLEANING_KEY_PATTER = re.compile(r"^'{1,}\"{1,}(.*)\"{1,}'{1,}$")
Articles_data = namedtuple('ArticlesData', 'exist articles_data indexes count')


class AwasuDataProcessor:
    """
    Load and manipulate data from Awasu
    """
    row_format: str

    def __init__(self):
        self.config_data: str = self.get_config()
        self.nodes = self.get_nodes()
        self.settings: str = self.load_settings()
        self.df_column_names = {'channel': 'Channel Name',
                                'published': 'Published',
                                'url': 'Item URL',
                                'title': 'Item Title'
                                }
        self.df = self.create_df()
        self.full_df = False

        self.top_folders = self.set_toplevel()
        self.selected_arts = pd.DataFrame(columns=['channel', 'title', 'url', 'published'])
        self.row_head_format: str = 'Channel Name,Published,Home URL,Item Title,Item URL'  # for old CSV template only!
        self.keys: list[str] = []
        self.global_limit: bool = False
        self.articles = len(self.df)
        self.channels = self.df.groupby('Channel Name').count()
        self.subfolders = self.load_subfolders()

    def get_news(self):
        """
        Return All articles in Pandas DataFrame
        :return: DF created after initialisation
        """
        return self.df

    @property
    def current_time(self):
        return arrow.now().format('HH:mm') + " "

    @staticmethod
    def get_config():
        """
        Get awasu config.ini
        :return: Loaded config data
        """
        config_path = AWASU_DEFAULT_CONFIG_PATH
        with open(config_path) as awasu_config_file:
            config_data: str = awasu_config_file.read()

        return config_data

    def set_global_limit(self, limit):
        """
        Restrict data to specified limit to faster loading
        :param limit: how many articles by channel
        :return: None
        """
        self.global_limit = limit

        if self.global_limit:
            limited_df = self.df
            self.full_df = self.df
            limited_df = limited_df.groupby('Channel Name').head(int(self.global_limit)).reset_index(drop=True)
            self.df = limited_df

    def remove_global_limit(self):
        """
        Remove limit DataFrame size restriction
        :return:
        """
        if self.full_df.empty:
            self.df = self.full_df

    def get_nodes(self):
        """
        Create nodes from Awasu config to map flat folder relations
        :return: list of nodes with:
            'name' - Folder name
            'guid' - GUID folder code
            'position' - position in level hierarchy 0 = root
        """

        lines = str(self.config_data).split('\n')
        nodes = []

        for line in lines:
            # Node-0.13.3=99A9F8F8-1ABE-438B-A82E-E4D9CBC9367F:Academic Data
            if line.startswith("Node-"):
                node = {}

                node_data = line.replace("Node-", "")
                node_position = str(node_data.split("=")[0])
                node_name_data = str(node_data.split("=")[1]).split(":")

                node['name'] = node_name_data[1]
                node['guid'] = node_name_data[0]
                node['position'] = node_position

                nodes.append(node)

        return nodes

    def set_toplevel(self) -> list:
        """
        Set Awasu root (top level) folders
        :return: list of main folders (categories)
        """
        top_folders = []
        for folder in self.nodes:
            if str(folder['position']).count('.') == 1:
                top_folders.append(folder)

        return top_folders

    def find_with_position(self, position):
        """
        Find folders in nodes by node position
        :param position: node code fx. 0.1 - first below root
        :return: folder list with name, guid and position
        """
        founded = []
        folder_list = self.get_nodes()
        if str(position).find('.') == -1:
            raise ValueError(f'Wrong position format for "{position}". I can not find node matcher "."!')

        for item in folder_list:
            if str(item['position']).startswith(position):
                founded.append(item)
            #  TODO: Check algorithm, because 0.1 and 0.12, 0.13 is matched
        return founded

    def match_by_position(self, folder_position):
        """
        Get channels by guid from Awasu by API call
        :param folder_position: nodes position
        :return: get channels from Awasu by GUID
        """

        found_match_guid = ""
        guid = self.find_with_position(folder_position)
        for channel_id in guid:
            found_match_guid += f"{channel_id['guid']},"

        found_match_guid = found_match_guid[:-1]  # remove last ','
        # TODO: Add it as API Call
        folders_api_call = f"{AWASU_API_URL}channels/list?token={TOKEN}&format=json&folderId={found_match_guid}"

        return requests.get(folders_api_call).json()

    def get_channels_names(self, position_to_find):
        """
        Return names inside folder with specified Guid
        :param position_to_find:
        :param guid_to_find: code of folder to find in format x.x fx. 0.2
        :return:
        """
        names = []
        channels = self.match_by_position(position_to_find)

        for channel in channels['channels']:
            names.append(str(channel['name']).replace('\n', ''))
        names = sorted(names)
        return names

    @staticmethod
    def format_awasu_date(wrong_data):
        """
        Convert date from Awasu to one format if other option than noCaption is used
        :param wrong_data: data to convert
        :return: correct data in format '2040-12-31 13:45'
        """
        replacement = ['Tomorrow ']
        start_date = wrong_data
        output_format = "YYYY-MM-DD HH:mm"
        current_date = arrow.now().format("YYYY-MM-DD")

        try:
            if wrong_data == '':
                return f"{current_date} 00:00"

            else:
                for r in replacement:
                    wrong_data = wrong_data.replace(r, '')

            if len(wrong_data) < 6:
                if str(wrong_data).find(':') != -1:
                    return f"{current_date} {wrong_data}"

            else:
                if str(wrong_data).startswith('Yesterday '):
                    wrong_data = wrong_data.replace('Yesterday ', str(arrow.now().shift(days=-1).format(output_format)))

                elif str(wrong_data[-4:]).isdigit() and str(wrong_data).find(':') != -1:
                    # Sun Mar 18 19:47 2018
                    wrong_data = arrow.get(wrong_data, "ddd MMM DD HH:mm YYYY").format(output_format)

                else:
                    # Mon Jan 28 09:12
                    wrong_data = str(arrow.get(wrong_data, "ddd MMM DD HH:mm")
                                     .format(output_format)).replace('0001', str(arrow.now().format("YYYY")))
        except Exception as e:
            print(f'PROBLEM with parsing: {wrong_data} => {e}')
            return "00.00.0000"

        correct_data = wrong_data

        if str(correct_data).startswith('0001-'):
            print(f'{start_date} => {correct_data}')
        return correct_data

    def clean_key(self, key):
        """
        Prepare channel name

        :param key: key from json data
        :return: key name without ' and " at the begging and end
        """

        cleaned = re.match(CLEANING_KEY_PATTER, key)
        return cleaned.group(1) if cleaned else key

    def create_df(self, news_source_file=False):
        """

        :param news_source_file: location of JSON file
        :return: Pandas DataFrames with articles
                -1 wrong source (is not file)
        """
        if not news_source_file:
            if CONCEPT_DEBUG:
                news_source_file: str = CSV_TEST_DATA
            else:
                news_source_file: str = CSV_BASE_SOURCE

        if not path.exists(news_source_file):
            self.update()

        if path.isfile(news_source_file):
            print(f"{news_source_file} : OK!")

            # To avoid json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

            with open(news_source_file, encoding='utf-8') as json_data:
                data = json.load(json_data, strict=False)

            articles = []
            self.keys = sorted(list(data.keys()))[:]  # Remove first key which is '' (empty result)

            for channel in tqdm(self.keys):
                for article in data[channel]:
                    body = article
                    body['channel'] = self.clean_key(channel)
                    body['published'] = self.format_awasu_date(article['published'])
                    articles.append(body)
        else:
            return -1

        df = pd.DataFrame(articles)
        df = df.rename(columns=self.df_column_names)
        print(df.head())
        return df

    def main_folders(self):
        """
        Get top level hierarchy folders for menu
        :return: list of folders
        """
        return self.top_folders

    def update(self):
        """
        Update DataFrame. It may take some times
        :return: None
        """
        report_run = f"AWASU_API_URL/reports/run?token=GYmh3B&format=json&name=ALL_CSV"
        print("Run report...")
        status = requests.get(report_run)
        if 'channelReports' in status:
            info = status['channelReports']
            if 'name' and 'status' in info:
                print(f"{info['name']} - {info['status']}")

        self.df = self.create_df()

    @staticmethod
    def load_settings(settings_dir=False, match_ext='txt'):
        """
        Load settings from files
        :param settings_dir:
        :return: dict with keys as names of loaded files converted to list
        """
        if not settings_dir:
            settings_dir = BASE_SETTINGS_DIR
        files = listdir(settings_dir)
        options = {}

        for file in files:
            if str(file).endswith(match_ext):
                with open(path.join(settings_dir, file), mode="r", encoding="utf8") as datafile:
                    options[str(file).split('.')[0]] = datafile.read().split('\n')

        return options

    def load_subfolders(self):
        """
        Load subfolder for Root folders
        :return: list of subfolders matched to key (dict)
        """
        print(f"{self.current_time}Loading subfolders...")
        folders_data = {}
        for main_folder in tqdm(self.top_folders, desc="Get Awasu Folder data", unit="API call"):
            folders_data[main_folder['position']] = self.get_channels_names(main_folder['position'])

        print(f"{self.current_time}Subfolder loaded!")
        return folders_data

    def search_agents_channels(self):
        search_agent_channels_names = []
        chs = list(set(self.df['Channel Name']))  # All channels names
        prefix = 'M >'

        for channel in chs:
            if channel.startswith(prefix):
                search_agent_channels_names.append(channel)

        return search_agent_channels_names

    def filter_df(self, **kwargs):
        """
        Select specified data from Data Frame
        :param kwargs:
            name - select by name
            position - select by folder GUID
            favorite - select by user favorite list
        :return: filtered DataFrame
        """

        options = kwargs.keys()

        if 'name' in options:
            selector: list = kwargs['name']

        elif 'position' in options:
            selector: list = self.subfolders[str(kwargs['position'])]

        elif 'favorite' in options:
            selector = self.settings[str(kwargs['favorite'])]

        elif 'searchagents' in options:
            selector = self.search_agents_channels()

        df = self.df.loc[self.df['Channel Name'].isin(selector)]
        print(f'DF Size: {len(df)} =>\n{df.head()}')
        return df

    def get_selected_arts(self):
        """
        Get selected articles
        :return: Pandas DF selected articles
        """
        return self.selected_arts

    def add_to_selected(self, added_article):
        """
        Add to selected articles Pandas DF
        :param added_article: article data to add (dict - key/val)
        :return: False if it is first article in select, in other case True
        """

        if self.selected_arts.empty:
            self.selected_arts.loc[0] = added_article
            return False

        print(self.selected_arts)
        print(added_article)

        self.selected_arts.loc[self.selected_arts.shape[0]] = added_article
        self.selected_arts = self.selected_arts.drop_duplicates(['url'])
        return True

    def remove_from_selected(self, article_index):
        """
        Delete article from selected list
        :param article_index: row index of article in DataFrame
        :return: None
        """
        self.selected_arts.drop(int(article_index), inplace=True)

    def filter_articles(self, mode, option=None):

        if mode == 'allnews':
            articles_data = self.get_news()
        elif mode == 'infolder':
            articles_data = self.filter_df(position=option)
        elif mode == 'favorite':
            articles_data = self.filter_df(favorite=option)
        elif mode == 'quick':
            articles_data = self.get_news().groupby('Channel Name').head(int(option)).reset_index(drop=True)
        elif mode == 'searchagents':
            articles_data = self.filter_df(searchagents='all')

        exist_data = False

        if len(articles_data) > 0:
            exist_data = True
        return Articles_data(exist=exist_data,
                             articles_data=articles_data,
                             indexes=articles_data.index.tolist(),
                             count=articles_data.count()
                             )
