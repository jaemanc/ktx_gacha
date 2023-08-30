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
  "version": "2.3",
  "template": {
    "outputs": [
      {
        "textCard": {
          "text": "예매할거냠?",
          "buttons": [
            {
              "label": "예매",
              "action": "block",
              "blockId": "pgf3311er4tah52zdin4aiv0",
              "extra": {
                "key1": "value1",
                "key2": "value2"
              }
            }
          ]
        }
      }
    ]
  },
  "context": {},
  "data": {}
}

        # 변환된 JSON 객체 내용 확인

        logger.info(f' request data : {request.data}')

        return Response(data=return_msg, status=status.HTTP_200_OK)
