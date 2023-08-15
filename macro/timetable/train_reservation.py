import logging
import time
import traceback

from django.views import View
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from macro.common import get_web_site_crawling
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

from macro.timetable.models.reservation_model import ReservationModel

logger = logging.getLogger()

class TrainReservation(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    def train_reservation(self, request):
        logger.debug(f'url : v1/train-reservattion')
        logger.debug(f'method: POST')
        logger.debug(f'request_data: {request.data}')

        try:
            #validation
            if is_valid_request(request):

                reservation_model = reservation_model_setter(request)
                train_reserve(train_model=reservation_model)
            else:
                return Response(data=None, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            logger.debug(f'v1/train-reservation error: {traceback.format_exc()}')
            logger.debug(f'train-reservation error:  {err}')
            return Response(data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=None, status=status.HTTP_200_OK)


def is_valid_request(request):
    try:
        req_startingPoint = request.data['startingPoint']
        req_arrivalPoint = request.data["arrivalPoint"]
        req_date = request.data["date"]
        req_memberNum = request.data["memberNum"]
        req_trainType = request.data["trainType"]
        req_contact_to_be_notified = request.data["contact"]

        if req_memberNum <=0:
            return False

        if req_contact_to_be_notified == "":
            return False

        # 현재는 ktx만 지원
        if req_trainType != 'ktx':
            return False
        #Todo
        # 시작역에 없는 역이 입력됐을 경우 역이 많다..
        #   return False
        #Todo
        # 도착역에 없는 역이 입력됐을 경우 역이 많다..
        #  return False
        #Todo
        # 현재 시간 보다 이전의 요청 날짜가 들어 올 경우.
        # return False

        return True
    except Exception as err:
        logger.debug(f'train-reservation error:  {err}')
        logger.info(f'request value not appropriate / REQ VAL : {request.data}')
        return False

def reservation_model_setter(request):

    reservation_model = ReservationModel()
    reservation_model.starting_point = request.data['startingPoint']
    reservation_model.arrival_point = request.data["arrivalPoint"]
    reservation_model.date = request.data["date"]
    reservation_model.year = reservation_model.date[:4]
    reservation_model.month = reservation_model.date[5:7]
    reservation_model.day = reservation_model.date[8:]
    reservation_model.member_num = request.data["memberNum"]
    reservation_model.train_type = request.data["trainType"]
    reservation_model.contact = request.data["contact"]

    logger.info(f' train models : {reservation_model.__dict__}')
    return reservation_model

def train_reserve(train_model):

    # 최대 30 분 동안 반복해서 서치
    start_time = time.time()
    end_time = start_time + 30 * 60

    # while time.time() < end_time:
    #
    #     time.sleep(5)

    logger.info(" 시간 지났음다 ㅜㅜ 다시 요청 해주세요. ")

    return None

