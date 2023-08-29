import logging
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from macro.common import get_web_site_crawling
import macro.common

logger = logging.getLogger()
custom_options = macro.common.custom_options
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

