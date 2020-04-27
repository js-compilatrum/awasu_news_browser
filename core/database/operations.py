"""
Main database interfaces for queries and Dabatase operations
"""
from collections import namedtuple
import attr
from itertools import chain
import sqlalchemy
from typing import Any
from typing import List

from sqlalchemy import desc, and_, asc

from core.database.base import session
from core.database.base import Article
from core.database.base import Channels
from core.database.base import DB_META
from core.database.results_manipulations import fill_with_headlines
from core.settings.slices import FIRST


@attr.s(auto_attribs=True)
class DatabaseOperation(object):
    """
    Main database operation interface to makes queries
    """
    session: sqlalchemy.orm.session.Session
    result: list = []

    def latest_n_articles_sort_by_channel(self, n_count: int) -> List[Any]:
        """
        
        :param n_count: number of latest articles 
        :return: Article list
        """
        self.result = self.session.query(Article).order_by(desc(Article.published)).\
            order_by(desc(Article.channel)).limit(n_count).all()
        self.session.commit()

        return self.result

    def from_channel(self, channel_name: str) -> List[Article]:
        """
        Get articles only from selected channel, latest articles on top
        :param channel_name: full channel name
        :return: Article lists
        """
        self.result = self.session.query(Article).filter(Article.channel == channel_name)\
            .order_by(desc(Article.published)).all()
        self.session.commit()
        return self.result

    def from_channels(self, channel_list: list) -> List[Article]:
        """
        Get articles from selected channel
        :param channel_list:
        :return:
        """

        self.result = self.session.query(Article).filter(Article.channel.in_(channel_list)).\
            order_by(and_(asc(Article.channel),
                          desc(Article.published))).all()
        session.commit()
        return self.result

    def channel_description(self, channel_name: str) -> List[Any]:
        self.result = self.session.query(Channels).filter(Channels.name == channel_name).first()
        session.commit()
        return self.result

    def channel_like(self, channel_name_part) -> List[Any]:
        """
        Get articles based on part of title

        :param channel_name_part: word of part of word from Channel name
        :return: Article list
        """
        self.result = self.session.query(Article).filter(Article.channel.like(channel_name_part)).all()
        self.session.commit()


    def from_folder_names(self, names: List[str]) -> List[Article]:
        channels = self.session.query(Channels.name).filter(Channels.channel_folders.ilike(names)).all()
        session.commit()
        return list(chain.from_iterable(
            [fill_with_headlines(self.from_channel(channel[FIRST])) for channel in channels])
        )

    @staticmethod
    def main_folders() -> List[str]:
        return [
            root_folder['channelFolder']['name']
            for root_folder in DB_META['folders']['channelFolders']
        ]


dbo = DatabaseOperation(session)
