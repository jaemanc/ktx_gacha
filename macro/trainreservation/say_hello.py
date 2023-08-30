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
                                        "text": "챗봇 관리자센터에 오신 것을 환영합니다 🙂\n\n챗봇 관리자센터로 챗봇을 제작해 보세요. \n카카오톡 채널과 연결하여, 이용자에게 챗봇 서비스를 제공할 수 있습니다.",
                                        "buttons": [
                                            {
                                                "label": "예매",
                                                "action": "block",
                                                "blockId": "pgf3311er4tah52zdin4aiv0"
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
