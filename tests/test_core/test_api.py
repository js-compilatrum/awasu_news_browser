import json
import unittest
import pytest

from core.api import AwasuAPI
from core.api import AwasuExceptionInAPI
from core.settings.config import AWASU_API
# AWASU_API: str = "http://localhost:2604"  # nb: get this from config.py
# MAX_API_CONNECTION: int = 10
# TOKEN: str = "GYmh3B"
# BEGINING_OF_RESPONSE = slice(0, 100)
#
# class AwasuExceptionInAPI(Exception):
#     pass
#
#
# AwasuCallParams = namedtuple('AwasuCallData', 'api_name params')


def test_api_invalid_token():
    TOKEN = ""
    api = AwasuAPI()
    api.prepare_params({'wrong_data': 'is_here'})
    pytest.raises(AwasuExceptionInAPI) == True


def test_api_build_url():
    api = AwasuAPI()
    assert api.build_url('channel/list') == f"{AWASU_API}/channel/list"


def test_call_awasu_sync(capsys):
    build_info = """{'buildInfo': {'version'"""
    api = AwasuAPI()
    result = api.call_awasu('buildInfo')
    captured = capsys.readouterr()

    assert str(result).startswith(build_info)
    assert isinstance(result, dict)
    assert f"[GET] Status:200" in captured.out, "Printing to console"


def test_clear_response_data():
    api = AwasuAPI()
    api.data = ['something']
    api.clear_response_data()
    assert api.data == [], "Clear what get from Awasu"