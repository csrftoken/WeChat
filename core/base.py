#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/5/1

"""
    access_token 是公众号的全局唯一接口调用凭据, 公众号调用各接口时都需使用access_token

    故而单独隔离
"""

import time
import requests

from src.api import ACCESS_TOKEN_API
from config import settings


class WxBasic(object):

    """
    获取 `access_token` 基类
    """

    def __init__(self):
        self.__access_token = None
        self.__left_time = 0

    def __get_real_access_token(self, ):
        response = requests.get(
            url=ACCESS_TOKEN_API,
            params={
                "grant_type": "client_credential",
                "appid": settings.WeChatConfig.app_id,
                "secret": settings.WeChatConfig.secret
            }
        ).json()
        self.__access_token = response["access_token"]
        self.__left_time = response["expires_in"]

    def get_access_token(self):

        if self.__left_time < 10:
            self.__get_real_access_token()

        return self.__access_token

    def run(self):
        while True:
            if self.__left_time > 10:
                time.sleep(2)
                self.__left_time -= 2
            else:
                self.__get_real_access_token()
