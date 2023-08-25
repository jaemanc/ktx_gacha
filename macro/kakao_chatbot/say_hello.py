import json
import logging
import traceback

from django.views import View
from selenium.webdriver.common.by import By
from macro.common import get_web_site_crawling
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

logger = logging.getLogger()


class Chatbot(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    def chatbot_test(self, request):
        logger.info(f" return msg test!!! ")

        return_msg = '{"version":"2.0","template":{"outputs":[{"simpleText":{"text":"hello I\'m Ryan"}}]}}'

        json_obj = json.loads(return_msg)

        version = json_obj['version']
        text = json_obj['template']['outputs'][0]['simpleText']['text']

        # 변환된 JSON 객체 내용 확인
        print("Version:", version)
        print("Text:", text)

        logger.info(f' request data : {request.data}')

        return Response(data=json_obj, status=status.HTTP_200_OK)
