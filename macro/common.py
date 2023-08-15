import logging

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger()

# 연속성을 위해 전역으로 세팅
customService = Service(ChromeDriverManager().install())
customOptions = Options()
driver = webdriver.Chrome(service=customService, options=customOptions)


def get_web_site_crawling(**kwargs):

    # 로컬 환경 버전이 아닌 드라이버 버전에 맞는 객체를 설치하고 가져오도록 수정.
    # 단점은 크롬이 이미 설치되어야 한다는 점, 장점은 크롬이 업데이트 되면 자동으로 버전을 맞춰준다는 점.
    # driver_path = '../chromedriver_mac_arm64/chromedriver'
    try:
        url = kwargs['url']
        # 웹사이트 URL 설정
        website_url = url  # 대상 웹사이트 URL
        driver.get(website_url)
        return driver

    except Exception as err:
        # URL 요청 없을경우
        # 기존 driver의 정보를 그대로 리턴한다.
        return driver
