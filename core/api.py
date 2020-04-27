from collections import namedtuple
from functools import partial
import json
from json import JSONDecodeError
from typing import List

import attr
import asks
import requests
from requests import Response
import trio

from core.data.presentation import print_colored
from core.settings.config import AWASU_API
from core.settings.config import TOKEN
from core.settings.slices import BEGINNING_OF_RESPONSE
from core.settings.slices import FIRST_FROM_LIST
"""
Awasu API call library

Use AwasuAPI to makes calls and ParamsBuilder to prepare list of api calls

Examples:

Preparing to calls
    pb = ParamsBuilder()
    pb.make(api_name="search/query", query="Donald Trump", max=100)
    pb.make(api_name="search/query", query="Europe", max=100)
    pb.make(api_name="search/query", query="USA", max=100)
    
    new_params = pb.prepared_params # Pass here to call_api()/acall_api()
    
Typical API declaration
    api = AwasuAPI()
    
Synchronous API call (blocking):
    print(api.call_awasu("buildInfo"))  

Async gathering data (non blocking):
    
    print_colored("PROCESSING", new_params)
    api.start_multicalls(new_params)  # Here put ParamsBuilder.prepared_params when you finish make items on list to call
    result = api.gathered_data
    print_colored("INFO", result)

"""



class AwasuExceptionInAPI(Exception):
    pass


AwasuCallParams = namedtuple('AwasuCallData', 'api_name params')


@attr.s(auto_attribs=True)
class AwasuAPI:

    awasu_server: str = attr.ib(default=AWASU_API)
    data: list = []
    params: dict = {}
    token: str = attr.ib(default=TOKEN)

    def prepare_params(self, call_params: dict) -> dict:
        """
        Prepare params to use in call

        :param call_params: params to use in call
        :return: extended params
        """

        call_params["format"] = "json"
        if TOKEN:
            call_params["token"] = TOKEN
            return call_params
        else:
            raise AwasuExceptionInAPI("No valid token provided. Setup 'TOKEN' in 'config.py'")

    @staticmethod
    def build_url(api_name):
        return f"{AWASU_API}/{api_name}"

    def call_awasu(self, api_name: str, **kwargs) -> json:
        """
        Call to Awasu API

        :param api_name: used API from Awasu, more see doc: https://awasu.com/help/
        :param kwargs: params of call
        :return: result of call in JSON
        """
        call_params = self.prepare_params(kwargs)
        post_data = call_params.pop("post_data", None)
        url = self.build_url(api_name)

        if post_data:
            used_method = "POST"
            resp: Response = requests.post(url, params=call_params, data=post_data)
        else:
            used_method = "GET"
            resp: Response = requests.get(url, params=call_params)

        print_colored("INFO", f"[{used_method}] Status:{resp.status_code} {url}")
        return json.loads(resp.text)

    def clear_response_data(self) -> None:
        """
        Clear data to avoid overide
        :return: none
        """
        self.data = []

    async def acall_awasu(self, api_name: str, show_info: bool =False, **kwargs) -> json:
        """
        Async call to Awasu API

        :param api_name: used API from Awasu, more see doc: https://awasu.com/help/
        :param kwargs: params of call
        :return: result of call in JSON
        """
        call_params = self.prepare_params(kwargs)
        post_data = call_params.pop("post_data", None)
        url = self.build_url(api_name)

        if post_data:
            used_method = "POST"
            resp: asks.request = await asks.post(url, params=call_params, data=post_data)
        else:
            used_method = "GET"
            resp: asks.request = await asks.get(url, params=call_params)

        if show_info:
            print_colored("INFO", f"[{used_method}] Status:{resp.status_code} {resp.reason_phrase} {resp.url}")

        try:
            json_data = json.loads(resp.content)
            self.data.append({list(json_data.keys())[FIRST_FROM_LIST]: json_data})
            return json_data
        except JSONDecodeError:
            # It's expected that primary format in API call will be json. If you change to HTML / XML it will be broke
            print_colored("ERROR", f"Expected JSON. Wrong data responded:\n{resp.content[BEGINNING_OF_RESPONSE]}")
            return -1

    def unpack_call_data(self, data: dict) -> AwasuCallParams:
        """
        Unpack data for seperate api_name from params. Use ParamsBuilder to prepare data
        :param data: builder data
        :return:
        """
        api_name: str = list(data.keys())[0]
        return AwasuCallParams(api_name=api_name, params=data[api_name])

    async def gather_data_from_calls(self, call_list: List[dict]) -> None:
        """
        Make async call to Awasu and get together results.

        Warning! Open socket limits on Windows makes tat if you get above 200 calls it will be start crash.
        Use splitting instead add pass API call list at once. Normally you do not have to makes that many of calls.

        :param call_list: list of dict with param to use in Awasu. Use ParamsBuilder to prepare
        :return: None
        """
        self.clear_response_data()
        print_colored("INFO", f"Start makes {len(call_list)} calls to Awasu...")

        async with trio.open_nursery() as nursery:
            for call in call_list:
                awasu_call_data: AwasuCallParams = self.unpack_call_data(call)
                nursery.start_soon(partial(self.acall_awasu, awasu_call_data.api_name, **awasu_call_data.params))

        print_colored("INFO", "Data gathering's finished")

    def start_multicalls(self, call_list: List[dict]):
        trio.run(self.gather_data_from_calls, call_list)

    @property
    def gathered_data(self):
        return self.data


@attr.s(auto_attribs=True)
class ParamsBuilder:
    params: list = attr.ib(default=[])

    def make(self, **kwargs):
        if 'api_name' not in kwargs:
            raise AwasuExceptionInAPI("You are not defined 'api_name' in make method. Calling to API is impossible!")

        print(kwargs)
        call_api_name = kwargs['api_name']
        del kwargs['api_name']
        data: dict = {call_api_name: kwargs}
        self.params.append(data)  # Convert format

    @property
    def prepared_params(self):
        return self.params