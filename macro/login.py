import logging
import traceback

from django.views import View
from selenium.webdriver.common.by import By
from macro.common import get_web_site_crawling
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

logger = logging.getLogger()
log_selenium = logging.getLogger('selenium')


class Login(viewsets.GenericViewSet, mixins.ListModelMixin, View):

    def login_to_website(self, request):
        """
        {
            "membershipNum": "비밀번호",
            "password": "패스워드"
        }
        """
        logger.debug(f'url : v1/login')
        logger.debug(f'method: POST')
        logger.debug(f'request_data: {request.data}')

        try:
            pages = login(request)

            logger.info(f" login success!! ")
            return Response(data=request.data, status=status.HTTP_200_OK)

        except Exception as err:
            logger.debug(f'v1/login error: {traceback.format_exc()}')
            logger.debug(f'{err}')

            log_selenium.debug(f' se v1/login error: {traceback.format_exc()}')
            log_selenium.debug(f' se {err}')
            return Response(data=request.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def login(request):

    # login_web_site_url = "https://www.letskorail.com"

    req_membershipNum = request.data['membershipNum']
    req_password = request.data['password']

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

        login_page.implicitly_wait(5)

        # 로그인 페이지 이동.
        try:
            go_to_login_page_button = login_page.find_elements(By.XPATH, '//img[@src="/images/gnb_login.gif"]')
            go_to_login_page_button[0].click()
        except Exception as err:
            go_to_login_page_button = login_page.find_elements(By.XPATH, '//img[@src="/images/gnb_home.gif"]')
            go_to_login_page_button[0].click()

        member_numbs = login_page.find_element(By.ID, "txtMember")
        member_numbs.send_keys(req_membershipNum)

        password = login_page.find_element(By.ID, "txtPwd")
        password.send_keys(req_password)
        login_btn = login_page.find_element(By.XPATH, '//img[@src="/images/btn_login.gif"]')
        login_btn.click()

    return login_page
