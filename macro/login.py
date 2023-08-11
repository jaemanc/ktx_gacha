import logging

from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from macro.common import get_web_site_crawling
from rest_framework import status, viewsets, mixins
from rest_framework.utils import json

logger = logging.getLogger()


class Login(viewsets.GenericViewSet, mixins.ListModelMixin, View):

    @api_view(['POST'])
    @csrf_exempt
    def login_to_website(self, request):
        logger.debug(f'url : v1/login')
        logger.debug(f'method: POST')
        logger.debug(f'request_data: {request.data}')

        try:
            pages = login_web_site(request)
        except:
            return Exception

        return pages


def login_web_site(request):
    login_web_site_url = "https://www.letskorail.com/korail/com/login.do"
    login_page = get_web_site_crawling(url=login_web_site_url)
    logger.debug(f' test {login_page}')

    return login_page
