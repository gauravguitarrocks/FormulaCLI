import sys
from typing import Union

from bs4 import BeautifulSoup
from requests import Response
from requests import get
from urllib3 import HTTPResponse


def get_response(url: str, b: bool = False) -> Union[str, HTTPResponse]:
    try:
        if b:
            response: Response = get(url, stream=True)
            return response.raw
        else:
            response = get(url)
            response.encoding = "utf-8"
            return response.text
    except Exception as e:
        print(e)
        sys.exit()


def parse(response: str) -> BeautifulSoup:
    return BeautifulSoup(response, 'html.parser')
