import logging
import traceback

from django.views import View
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from macro.common import get_web_site_crawling
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

from macro.utils.exception_handle import webdriver_exception_handler

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
            pages = login(request)

            logger.info(f" login success!! ")
            return Response(data=request.data, status=status.HTTP_200_OK)

        except Exception as err:
            logger.debug(f'v1/chatbot-login error: {traceback.format_exc()}')
            logger.debug(f'{err}')
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
    req_membershipNum = membershipNum
    req_password = password

    login_page = None

    try:
        login_web_site_url = "https://www.letskorail.com/ebizprd/prdMain.do"
        login_page = get_web_site_crawling(url=login_web_site_url)

        logger.info(f'driver session id :  {login_page.session_id}')
    except Exception as err:
        login_web_site_url = "https://www.letskorail.com"
        login_page = get_web_site_crawling(url=login_web_site_url)

        logger.info(f' retried.. go! {login_web_site_url}, driver session id :  {login_page.session_id}')
    finally:
        login_page.implicitly_wait(3)

        # 로그인 페이지 이동.
        try:
            go_to_login_page_button = login_page.find_elements(By.XPATH, '//img[@src="/images/gnb_login.gif"]')
            go_to_login_page_button[0].click()
        except Exception as err:
            go_to_login_page_button = login_page.find_elements(By.XPATH, '//img[@src="/images/gnb_home.gif"]')
            go_to_login_page_button[0].click()

        login_page.implicitly_wait(3)

        member_numbs = None
        password = None

        elements = login_page.find_elements(By.XPATH, '//img')

        # 모든 엘리먼트 로그로 출력
        for element in elements:
            logging.info(f" Element: {element.tag_name} - Text: {element.text} , {element.get_attribute('outerHTML')} ")


        try:
            member_numbs = login_page.find_element(By.ID, "txtMember")
            member_numbs.send_keys(req_membershipNum)

            password = login_page.find_element(By.ID, "txtPwd")
            password.send_keys(req_password)
        except Exception as err:
            if member_numbs:
                member_numbs = login_page.find_element(By.NAME, "txtMember")
                member_numbs.send_keys(req_membershipNum)
            if password:
                password = login_page.find_element(By.NAME, "txtPwd")
                password.send_keys(req_password)

        # elements = login_page.find_elements(By.XPATH, '//img')
        #
        # # 모든 엘리먼트 로그로 출력
        # for element in elements:
        #     logging.info(f" Element: {element.tag_name} - Text: {element.text} , {element.get_attribute('outerHTML')} ")

        try:
            login_btn = login_page.find_element(By.XPATH, '//img[@src="/images/btn_login.gif"]')
        except NoSuchElementException as err:
            login_btn = login_page.find_element(By.XPATH, 'a[href="javascript:Login(1);"]')
        except Exception as err2:
            login_btn = login_page.find_element(By.XPATH, 'li.btn_login')

        login_btn.click()

        # href 속성 값으로 엘리먼트 찾기

    return login_page




