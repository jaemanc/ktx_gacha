import logging
import http.client
import logging
import traceback

import requests
from rest_framework import status

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from rest_framework.views import exception_handler

from macro.common import get_web_site_crawling
import macro.common

logger = logging.getLogger()
custom_options = Options()

custom_options.add_argument('--headless=new')
custom_options.add_argument('--no-sandbox')
custom_options.add_argument('--lang=ko-KR')
driver = None

def webdriver_exception_handler():

    try:
        logger.info(f'##########################################')
        logger.info(f'Initialize the web driver due to an error.')
        logger.info(f'##########################################')

        # 연속성을 위해 전역으로 세팅
        global driver

        driver = webdriver.Chrome(options=custom_options)
        driver.get('https://www.letskorail.com/ebizprd/prdMain.do')

        # 에러 이후 드라이버가 종료되면 다른 작업들도 다막히기 때문에 수정.
        macro.common.driver = driver

    except Exception as err:
        logger.info(f' 서버 혹은 container를 재실행 해야 합니다!!! ')
        logger.info(f'{traceback.format_exc()}')
        logger.info(f'{err}')

