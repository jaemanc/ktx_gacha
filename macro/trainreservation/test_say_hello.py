import json
import logging

from django.views import View
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

logger = logging.getLogger()


class Chatbot(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    def chatbot_test(self, request):
        logger.info(f" return msg test!!! ")

        return_msg = {
                        "version": "2.0",
                        "template": {
                            "outputs": [
                                {
                                    "textCard": {
                                        "text": "후.. 🙂 찾았슴다.\n ",
                                        "buttons": [
                                            {
                                                "label": "예매",
                                                "action": "block",
                                                "blockId": "64ec11f6e4f55f6afe216dcc"
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    }

        # simple_test_data = {
        #                         "version": "2.0",
        #                         "template": {
        #                             "outputs": [
        #                                 {
        #                                     "simpleText": {
        #                                         "text": "간단한 텍스트 요소입니다."
        #                                     }
        #                                 }
        #                             ]
        #                         }
        #                     }


        # 변환된 JSON 객체 내용 확인

        # logger.info(f' request data : {request.data}')
        logger.info(f'{return_msg}')

        return Response(data=return_msg, status=status.HTTP_200_OK)
