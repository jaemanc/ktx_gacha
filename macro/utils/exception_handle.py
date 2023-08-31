import logging
import traceback

from selenium import webdriver

from macro.utils.common import get_web_site_crawling
import macro.utils.common

logger = logging.getLogger()
custom_options = macro.utils.common.custom_options
driver = None

def webdriver_exception_handler():

    try:
        logger.error(f'##########################################')
        logger.error(f'Initialize the web driver due to an error.')
        logger.error(f'##########################################')

        # 연속성을 위해 전역으로 세팅
        global driver

        if driver is not None:
            driver.quit()

        driver = webdriver.Chrome(options=custom_options)
        driver.get('https://www.letskorail.com/ebizprd/prdMain.do')

        # 에러 이후 드라이버가 종료되면 다른 작업들도 다막히기 때문에 수정.
        macro.utils.common.driver = driver

    except Exception as err:
        logger.fatal(f'docker process ERROR ')
        logger.fatal(f'{traceback.format_exc()}')
        logger.fatal(f'{err}')

