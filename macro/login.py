import logging
import traceback

from django.views import View
from selenium.webdriver.common.by import By
from macro.common import get_web_site_crawling
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

logger = logging.getLogger()


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

        except Exception as err:
            logger.debug(f'v1/login error: {traceback.format_exc()}')
            logger.debug(f'{err}')
            return Response(data=pages, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=pages, status=status.HTTP_200_OK)


def login(request):
    login_web_site_url = "https://www.letskorail.com/korail/com/login.do"
    login_page = get_web_site_crawling(url=login_web_site_url)
    req_membershipNum = request.data['membershipNum']
    req_password = request.data['password']
    membernumbs = login_page.find_element(By.ID, "txtMember")
    password = login_page.find_element(By.ID, "txtPwd")
    membernumbs.send_keys(req_membershipNum)
    password.send_keys(req_password)
    login_btn = login_page.find_element(By.XPATH,'//img[@src="/images/btn_login.gif"]')
    login_btn.click()

    return login_page
