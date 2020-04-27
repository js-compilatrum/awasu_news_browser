from core.database.base import session
from core.database.operations import DatabaseOperation

dbo = DatabaseOperation(session)


def test_get_latest_n_articles():
    assert len(dbo.latest_n_articles_sort_by_channel(100)) > 0

def test_get_articles_from_channel():
    assert len(dbo.from_channel('BBC')) > 0


def test_get_articles_from_channel_name_like():
    assert len(dbo.channel_like()) > 0


def test_channel_list():
    assert len(dbo.list_of_channels) > 0


def test_get_articles_from_channel_in_folder():
    folder_names = ['folder1', 'folder2']
    assert len(dbo.channels_in_folder(folder_names)) > 0


def get_articles_from_search_agents():
    assert len(dbo.from_search_agensts()) > 0


def get_articles_from_my_categories():
    categories = ['Movies', 'PC']
    assert len(dbo.from_my_categories(categories)) > 0


def get_last_watched_channels():
    assert len(dbo.last_watched_channels) > 0


def get_articles_from_suggested_channels():
    assert len(dbo.articles_from_suggested_channels) > 0

