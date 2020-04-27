from collections import namedtuple
from collections import ChainMap
import json
from typing import NamedTuple

import arrow
from boltons.iterutils import get_path, research, remap
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from attrs_sqlalchemy import attrs_sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from tqdm import tqdm

from core.api import AwasuAPI
from core.api import ParamsBuilder
from core.data.manipulation import convert_name_to_pep
from core.data.manipulation import join_dicts
from core.data.presentation import print_colored
from core.settings.config import DEBUG
from core.settings.config import FILE_WTIH_DATA_TO_DATABASE

api = AwasuAPI()
pb = ParamsBuilder()
Base = declarative_base()
DB_META = {}  # Setting and nested structure for database outside articles

@attrs_sqlalchemy
class Article(Base):
    __tablename__ = 'articles'

    id: Column = Column(Integer, primary_key=True, autoincrement=True)
    channel: Column = Column(String, index=True)
    title: Column = Column(String, index=True)
    published: Column = Column(DateTime, index=True)
    url: Column = Column(String)
    state: Column = Column(String, index=True)


@attrs_sqlalchemy
class Channels(Base):
    __tablename__ = "channels"

    id: Column = Column(Integer, primary_key=True, autoincrement=True)
    type: Column = Column(String, index=True)
    name: Column = Column(String, index=True)
    description: Column = Column(String)
    feed_url: Column = Column(String)
    home_url: Column = Column(String)
    config_filename: Column = Column(String)
    last_feed_filename: Column = Column(String)
    auto_update_interval: Column = Column(Integer)
    last_update_timestamp: Column = Column(Integer)
    last_successful_update_timestamp: Column = Column(Integer)
    update_error_count: Column = Column(Integer)
    n_unread_items: Column = Column(Integer)
    new_items: Column = Column(Integer)
    channel_folders: Column(String) = Column(String)
    channel_folders_names: Column(String) = Column(String)
    channel_folders_ids: Column(String) = Column(String)


@attrs_sqlalchemy
class Selected(Base):
    __tablename__ = "selected"

    id: Column = Column(Integer, primary_key=True, autoincrement=True)
    article_id: Column(Integer, index=True)


def init_db() -> NamedTuple('DatabaseElements', [('engine', Engine), ('session_factory', sessionmaker)]):
    """
    Call it once to create database in memory

    :return: engine and session factory for SQL Alchemy
    """
    print_colored("PROCESSING", "Establish database connection")
    db_elements: namedtuple = namedtuple("DatabaseElements", ["engine", "session_factory"])

    connection_option = "sqlite:///:memory:"

    if DEBUG:
        engine = create_engine(connection_option, echo=True)
    else:
        engine = create_engine(connection_option, echo=False)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)  # once engine is available
    session = Session()
    Base.metadata.create_all(engine)  # After model
    print_colored("INFO", "Database created")
    return db_elements(engine=engine, session_factory=session)


def populate_db(session):
    print_colored("PROCESSING", f"Loading Awasu data from {FILE_WTIH_DATA_TO_DATABASE}")
    # CSV_BASE_SOURCE = r'D:\Pliki z danymi\Bieżące przedsięwzięcia\Awasu\Raporty\json\all_unread_channels.json'
    with open(FILE_WTIH_DATA_TO_DATABASE, encoding='utf-8') as json_data:
        data = json.load(json_data, strict=False)

    keys = sorted(list(data.keys()))[:]
    for channel in tqdm(keys, unit=" channels"):
        for article in data[channel]:
            body = article
            body['channel'] = channel
            body['published'] = arrow.get(body['published']).datetime
            session.add(Article(**body))
    session.commit()


def awasu_data_from_api_calls():
    pb.make(api_name="channels/folders/tree")
    pb.make(api_name="channels/list", verbose="1")
    params = pb.prepared_params
    api.start_multicalls(params)
    return api.gathered_data


def combine_data_from_api() -> dict:
    """
    Gather data from Awasu API calls and flat all JSON by join it together
    :return:
    """
    awasu_api_result = awasu_data_from_api_calls()
    return dict(ChainMap(*awasu_api_result))


def find_channels(folders: dict, folder_name: str) -> dict:
    """

    :param folders: Awasu directory tree from API
    :param folder_name: target folder name
    :return: channels
    """

    match = research(folders,
                     lambda dir_path, key, value: key == 'name' and value == folder_name)
    if match:
        root = get_path(folders, match[0][0][:-1])
        channel_folders = research(root, lambda dir_path, key, value: key == 'channelFolder')
        channels = [value for _, value in channel_folders]
        for channel in channels:
            del channel['channelFolders']
        return channels
    return {}


def create_channels_table(data):
    """
    Create SQLAlchemy DB table for channels

    :param data: Awasu Channels API information
    :return: None
    """
    database_fields = [field for field in list(Channels.__dict__.keys()) if not field.startswith('__')]

    for channel in data['channels']['channels']:
        channel_info = {
            convert_name_to_pep(key): channel[key]
            for key in channel.keys()
            if convert_name_to_pep(key) in database_fields
        }
        folders = channel['channelFolders']
        channel_info['channel_folders'] = ';'.join([folder['name'] for folder in folders])
        session.add(Channels(**channel_info))
    session.commit()


def fill_folders_db_meta(data: dict) -> dict:
    """
    Return sublevel of root folder from Awasu directory structure

    :param data:
    :return: sublevel root folders
    """
    return data['channelFolder']['channelFolder']


def fill_from_api() -> dict:
    """
    Combine JSONs from Awasu API and put in database

    :return: data from Awasu API
    """
    data = join_dicts(awasu_data_from_api_calls())
    create_channels_table(data)
    return data


DATABASE: NamedTuple('DatabaseElements', [('engine', Engine), ('session_factory', sessionmaker)]) = init_db()
engine: Engine = DATABASE.engine
session: sessionmaker = DATABASE.session_factory
populate_db(session)  # Put data to database here when import file in any view

api_data = fill_from_api()
DB_META['folders'] = fill_folders_db_meta(api_data)
DB_META['created'] = arrow.now().format('YYYY-MM-DD HH:mm:ss')

print_colored("INFO", "Data loaded!")