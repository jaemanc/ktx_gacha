import logging
import traceback

import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger()
log_selenium = logging.getLogger('selenium')

custom_options = Options()
custom_options.add_argument("--disable-extensions")
custom_options.add_argument('--headless=new')
custom_options.add_argument('--no-sandbox')
custom_options.add_argument('--lang=ko-KR')
custom_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=custom_options)

driver.execute_script("window.open('');")

s = requests.session()

logger.info(f'driver session id :  {driver.session_id}')


def get_web_site_crawling(**kwargs):
    global driver

    # 로컬 환경 버전이 아닌 드라이버 버전에 맞는 객체를 설치하고 가져오도록 수정.
    # 단점은 크롬이 이미 설치되어야 한다는 점, 장점은 크롬이 업데이트 되면 자동으로 버전을 맞춰준다는 점.
    try:
        url = kwargs['url']
        # 웹사이트 URL 설정
        if url:
            driver.get(url)

        alert = driver.switch_to.alert
        alert.dismiss()

        return driver.get(driver.current_url)

    except Exception as err:
        log_selenium.info(f'{traceback.format_exc()}')
        log_selenium.info(f'{err}')

        # URL 요청 없을경우
        # 기존 driver의 정보를 그대로 리턴한다.
        return driver


def use_call_back_msg():
    return {"version": "3.2", "useCallback": True, "context": {}, "data": {}}


def train_list_and_callback_chatbot_response_message(train_list):
    return {
            "version": "2.0", # 2.0 아니면 메세지 안보임. 버그인지 의도인지 카카오에 문의 한 상태 2023 08 30
            "template": {
                "outputs": [
                    {
                        "textCard": {
                            "text": train_list,
                            "buttons": [
                                {
                                    "label": "표 예약하러 가기",
                                    "action": "block",
                                    "blockId": "64ec11f6e4f55f6afe216dcc"
                                }
                            ]
                        }
                    }
                ]
            }
            }

def login_msg_and_callback_chatbot_response_message(login_status_msg):
    return {
            "version": "2.0", # 2.0 아니면 메세지 안보임. 버그인지 의도인지 카카오에 문의 한 상태 2023 08 30
            "template": {
                "outputs": [
                    {
                        "textCard": {
                            "text": login_status_msg,
                            "buttons": [
                                {
                                    "label": "시간표 보러 가기",
                                    "action": "block",
                                    "blockId": "64ec10eae4f55f6afe216dc0"
                                },
                                {
                                    "label": "표 예약하러 가기",
                                    "action": "block",
                                    "blockId": "64ec11f6e4f55f6afe216dcc"
                                }
                            ]
                        }
                    }
                ]
            }
            }






