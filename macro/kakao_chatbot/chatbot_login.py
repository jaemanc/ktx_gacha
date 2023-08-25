import logging
import traceback

from django.views import View
from selenium.webdriver.common.by import By
from macro.common import get_web_site_crawling
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

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
        # 로그인 페이지 이동.
        go_to_login_page_button = login_page.find_element(By.XPATH, '//img[@src="/images/gnb_login.gif"]')
        go_to_login_page_button.click()

        member_numbs = login_page.find_element(By.ID, "txtMember")
        member_numbs.send_keys(req_membershipNum)

        password = login_page.find_element(By.ID, "txtPwd")
        password.send_keys(req_password)
        login_btn = login_page.find_element(By.XPATH, '//img[@src="/images/btn_login.gif"]')
        login_btn.click()

    return login_page




