from collections import ChainMap
from collections import defaultdict
from pathlib import Path
from typing import List

import arrow
from boltons.iterutils import get_path
from boltons.iterutils import research
from boltons.iterutils import remap

from core.settings.config import FILE_WTIH_DATA_TO_DATABASE
from core.settings.config import DEBUG
from core.settings.slices import LAST
from core.settings.slices import FIRST


def get_all_channels(root_path: dict) -> dict:
    """
    Get all channels in flattened structure
    :param root_path: top folder
    :return: in format 'Worldwide' : '5D93371C-6FCA-44B5-A880-3619DAD5C8FD', flattened
    """

    channels = defaultdict(dict)

    def visit(path_in_structure, key, value):
        if path_in_structure[LAST] == 'channelFolder' and key in ('name', 'id'):
            channels[path_in_structure].update({key: value})
        return False

    remap(root_path, visit=visit, reraise_visit=False)
    return {i['name']: i['id'] for i in channels.values()}


def find_channels(directory_tree_structure: dict, target: str) -> dict:
    """
    Find channels in Awasu Directory Tree

    :param directory_tree_structure: API Awasu directory tree
    :param target: folder to fine
    :return: dict with result of False if None
    """

    researched = research(directory_tree_structure,
                          lambda path_in_structure,
                                 key,
                                 value: key == 'name' and value == target)

    try:
        root = get_path(directory_tree_structure,
                        researched[FIRST][FIRST][:LAST])  # Parent path if exist or IndexError
    except IndexError:
        return False
    return get_all_channels(root)


def join_dicts(list_of_dicts: List[dict]) -> dict:
    """ Merge n numbers of dicts """
    return dict(ChainMap(*list_of_dicts))


def convert_name_to_pep(variable_name: str) -> str:
    """
    Replace thisTypeNames with PEP compatible this_typ_names

    :param variable_name:
    :return:
    """
    renamed = ""
    for letter in variable_name:
        if letter.isupper():
            letter = f"_{letter.lower()}"
        renamed += letter
    return renamed


def data_info() -> dict:
    """ General information about data source """

    created: str = arrow.get(Path(FILE_WTIH_DATA_TO_DATABASE).stat().st_ctime).format("YYYY.MM.DD HH:mm:ss")

    return {'sources': 2000,
            'articles': 400000,
            'created_data': created,
            'is_debug': DEBUG,
            }


def dict_of_channels_to_str(channels: List[dict]) -> dict:
    """
    Convert list of dict with channels to seperate names and ids namedtuple

    :param channels: list of dict with channels
    :return: namedtuple with names and ids
    """

    names = []
    ids = []

    for channel in channels:
        names.append(channel['name'])
        ids.append(channel['id'])

    return {'names': names, 'ids': ids}


def timestamp_to_normal_date(timestamp):
    return arrow.get(timestamp).format("YYYY.MM.DD HH:mm")