import logging
import threading
import traceback

import requests
from django.views import View
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from macro.utils.buttons import Buttons
from macro.utils.common import get_crawling_driver, use_call_back_msg, login_msg_and_callback_chatbot_response_message
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

from macro.utils.email_sender import error_sender
from macro.utils.exception_handle import webdriver_exception_handler
from macro.utils.pages import Pages

logger = logging.getLogger()
log_selenium = logging.getLogger('selenium')


class ChatBotLogin(viewsets.GenericViewSet, mixins.ListModelMixin, View):

    def login_to_website(self, request):
        """
        {
            "membershipNum": "비밀번호",
            "password": "패스워드"
        }
        """
        logger.debug(f'url : v1/chatbot-login')
        logger.debug(f'method: POST')
        logger.debug(f'request_data: {request.data}')

        try:
            # 챗봇 콜백 정책으로 인해 응답 우선 비동기 처리.
            login_thread = threading.Thread(target=login, args=(request,))
            login_thread.start()
            # login(request)

            return Response(data=use_call_back_msg(), status=status.HTTP_200_OK)

        except Exception as err:
            logger.debug(f'v1/chatbot-login error: {traceback.format_exc()}')
            logger.debug(f'{err}')

            # 에러 사항 이메일로 전송
            error_sender(err)
            webdriver_exception_handler()

            return Response(data=request.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def login(request):

    # login_web_site_url = "https://www.letskorail.com"
    data = request.data
    bot_id = data['bot']['id']
    intent_id = data['intent']['id']

    loginentity_origin = data['action']['detailParams']['loginEntityParams']['origin']
    values = loginentity_origin.split('/')
    membershipNum = values[0].strip()
    password = values[1].strip()

    logger.info(f'bot_id : {bot_id}')
    logger.info(f'intent_id : {intent_id}')
    logger.info(f'loginentity_origin : {loginentity_origin} , membershipNum : {membershipNum} , password : {password}')

    login_page = None

    try:
        login_page = get_crawling_driver(url=Pages.KTX_MAIN_PAGE_DO)
        logger.info(f'driver session id: {login_page.session_id}')
    except Exception as err:
        login_page = get_crawling_driver(url=Pages.KTX_MAIN_PAGE)
        logger.info(f'retried.. go! {login_page.current_url}, driver session id: {login_page.session_id}')

    finally:
        login_page.implicitly_wait(3)

        # 로그인 페이지 이동.
        try:
            go_to_login_page_button = login_page.find_element(By.XPATH, Buttons.IMG_SRC_GNB_LOGIN)
        except NoSuchElementException:
            go_to_login_page_button = login_page.find_element(By.XPATH, Buttons.IMG_SRC_GNB_HOME)

        go_to_login_page_button.click()

        login_page.implicitly_wait(3)

        member_numbs_element = login_page.find_element(By.ID, Buttons.TXT_MEMBER)
        member_numbs_element.send_keys(membershipNum)

        password_element = login_page.find_element(By.ID, Buttons.TXT_PWD)
        password_element.send_keys(password)

        try:
            login_btn = login_page.find_element(By.XPATH, Buttons.IMG_SRC_BTN_LOGIN)
        except NoSuchElementException:
            try:
                login_btn = login_page.find_element(By.XPATH, Buttons.HREF_LOGIN_BTN)
            except NoSuchElementException:
                login_btn = login_page.find_element(By.XPATH, Buttons.LI_BTN_LOGIN)

        login_btn.click()

        response = login_msg_and_callback_chatbot_response_message(login_status_msg='로그인 했습니다!')

        # callback msg send
        callback_response = requests.post(request.data["userRequest"]["callbackUrl"], json=response, headers={"Content-Type": "application/json"})

        logger.info(f" login success!! callback : {callback_response}")

    return login_page




