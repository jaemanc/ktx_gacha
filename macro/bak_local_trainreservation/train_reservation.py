import logging
import threading
import time
import traceback

from django.views import View
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from macro.utils.common import get_web_site_crawling
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

from macro.trainreservation.models.reservation_model import ReservationModel
from macro.utils.email_sender import send_stmp
from macro.utils.exception_handle import webdriver_exception_handler

logger = logging.getLogger()

semaphore = threading.Semaphore(value=1)


class TrainReservation(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    def train_reservation(self, request):
        logger.debug(f'url : v1/train-reservation')
        logger.debug(f'method: POST')
        logger.debug(f'request_data: {request.data}')

        try:
            # validation
            if is_valid_request(request):

                reservation_model = reservation_model_setter(request)
                train_reserve(reservation_model=reservation_model)
            else:
                return Response(data=None, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            logger.debug(f'v1/train-reservation error: {traceback.format_exc()}')
            logger.debug(f'train-reservation error:  {err}')
            webdriver_exception_handler()
            return Response(data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data='예약 완료!', status=status.HTTP_200_OK)


def is_valid_request(request):
    try:
        req_startingPoint = request.data['startingPoint']
        req_arrivalPoint = request.data["arrivalPoint"]
        req_date = request.data["date"]
        req_memberNum = request.data["memberNum"]
        req_trainType = request.data["trainType"]
        req_contact = request.data["contact"]
        req_seatType = request.data["seatType"]

        req_memberNum = int(req_memberNum)

        if req_memberNum <= 0:
            return False

        if req_contact == "":
            return False

        # default 일반 좌석
        if req_seatType == "":
            req_seatType = "일반"

        # 현재는 ktx만 지원
        if req_trainType != 'ktx':
            return False
        # Todo
        # 시작역에 없는 역이 입력됐을 경우 역이 많다..
        #   return False
        # Todo
        # 도착역에 없는 역이 입력됐을 경우 역이 많다..
        #  return False
        # Todo
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
    reservation_model.day = reservation_model.date[8:10]
    reservation_model.hour = reservation_model.date[11:13]
    reservation_model.member_num = request.data["memberNum"]
    reservation_model.train_type = request.data["trainType"]
    reservation_model.contact = request.data["contact"]
    reservation_model.seat_type = request.data["seatType"]

    logger.info(f' train models : {reservation_model.__dict__}')
    return reservation_model


def train_reserve(reservation_model):
    # 최대 30 분 동안 반복해서 서치
    start_time = time.time()
    end_time = start_time + 30 * 60

    # get driver - 목록 조회 페이지에서만 동작해야한다.
    reserve_driver = get_web_site_crawling()

    current_time = datetime.now()

    current_hour = current_time.hour
    current_minute = current_time.minute

    now_time = f"{current_hour:02d}:{current_minute:02d}"

    # end_time 시간과 분 계산
    end_datetime = datetime.fromtimestamp(end_time)
    end_hour = end_datetime.hour
    end_minute = end_datetime.minute
    end_time_formatted = f"{end_hour:02d}:{end_minute:02d}"

    logger.info(f" now_time : {now_time}")

    flag = False
    index = 0
    while time.time() < end_time and not flag:

        for index in range(10):
            logger.info(
                f"end_time : {end_time_formatted} index : {index} , reservation_model : {reservation_model.__dict__}")
            flag = reservation_loop(reservation_model=reservation_model, index=index)

    return flag


def reservation_loop(reservation_model, index):

    reserve_driver = get_web_site_crawling()
    try:
        # 조회 결과 테이블
        table = reserve_driver.find_element(By.ID, "tableResult")

        trs = table.find_elements(By.TAG_NAME, "tr")

        # for tr in trs:
        tr = trs[index]
        count = 0

        td_objs = tr.find_elements(By.TAG_NAME, "td")

        for td in td_objs:
            count += 1

            # td object에는 여러가지 값들이 있어서 필요한 값이 있는 순번에만 검색하도록 수정.
            if count in {1, 2, 7, 8, 9, 10, 11, 12, 13, 14}:
                continue

            if count == 3:
                go = td.text
                go = go.replace("\n", " ")
                continue

            if count == 4:
                end = td.text
                end = end.replace("\n", " ")
                continue

            try:
                # 특실
                element = td.find_element(By.TAG_NAME, "img")

                img_name = element.get_attribute("name")
                btn_names_special = {f"btnRsv2_{i}" for i in range(10)}

                if img_name in btn_names_special:
                    if reservation_model.seat_type == "특실":
                        # 출발 시간이 20 분 넘게 남았는가?
                        go = go[4:8]
                        hour, minute = map(int, go.split(":"))
                        going = datetime(int(reservation_model.year), int(reservation_model.month),
                                         int(reservation_model.day), int(hour), int(minute))
                        current_time = datetime.now()

                        if (going - current_time) >= timedelta(minutes=20):
                            element.click()  # 예약하기

                            # 안내 메시지 처리.
                            try:
                                iframe = reserve_driver.find_element(By.TAG_NAME, 'iframe')
                                reserve_driver.switch_to.frame(iframe)

                                element = reserve_driver.find_element(By.XPATH, '//a[@class="btn_blue_ang"]')

                                if element:
                                    element.click()

                                # iframe에서 빠져나옴
                                reserve_driver.switch_to.default_content()

                            except Exception as err:
                                logger.info(f' 계속 진행. ')

                            while True:
                                try:
                                    # alert 창 확인 처리.
                                    alert = Alert(reserve_driver)
                                    alert.accept()
                                except:
                                    break

                            reservation_model.go = go
                            logger.info(f' 특실 예약합니다. {go} , {reservation_model}')

                            # 예매 정보 이메일로 통보
                            send_stmp(reservation_model=reservation_model)

                            # 장바구니에 담았으면?
                            return True

            except Exception as err:
                logger.info(f'v1/train-reservation error 0 : {traceback.format_exc()}')
                logger.info(f'{err}')
                logger.info("특실 매진")

            try:
                # 일반실 예약하기 클릭
                element = td.find_element(By.TAG_NAME, "img")

                img_name = element.get_attribute("name")
                btn_names_special = {f"btnRsv1_{i}" for i in range(10)}

                if img_name in btn_names_special:

                    if reservation_model.seat_type == "일반":
                        # 출발 시간이 20 분 넘게 남았는가?
                        go = go[4:8]
                        hour, minute = map(int, go.split(":"))
                        going = datetime(int(reservation_model.year), int(reservation_model.month),
                                         int(reservation_model.day), int(hour), int(minute))

                        current_time = datetime.now()

                        if (going - current_time) >= timedelta(minutes=20):
                            element.click()  # 예약하기

                            # 안내 메시지 처리.
                            try:
                                iframe = reserve_driver.find_element(By.TAG_NAME,'iframe')
                                reserve_driver.switch_to.frame(iframe)

                                element = reserve_driver.find_element(By.XPATH, '//a[@class="btn_blue_ang"]')

                                if element:
                                    element.click()

                                # iframe에서 빠져나옴
                                reserve_driver.switch_to.default_content()

                            except Exception as err:
                                logger.info(f' 계속 진행. ')

                            while True:
                                try:
                                    # alert 창 확인 처리.
                                    alert = Alert(reserve_driver)
                                    alert.accept()
                                except:
                                    break

                            # 선택한 출발 시간 세팅
                            reservation_model.go = go
                            logger.info(f' 일반실 예약합니다. {go} , {reservation_model}')

                            # 예매 정보 이메일로 통보
                            send_stmp(reservation_model=reservation_model)

                            # 장바구니에 담았으면?
                            return True

            except Exception as err:
                logger.info(f'v1/train-reservation error 1: {traceback.format_exc()}')
                logger.info(f'{err}')
                logger.info("일반실 매진")

    except Exception as err:
        logger.debug(f'v1/train-reservation error 2: {traceback.format_exc()}')
        logger.debug(f'{err}')

    return False

