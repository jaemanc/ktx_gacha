import logging
import threading
import time
import traceback
from telnetlib import EC

from django.views import View
from selenium.webdriver.common.alert import Alert
from datetime import timedelta

from macro.trainreservation.models.reservation_model import ReservationModel
from macro.utils.buttons import Buttons, Seat
from macro.utils.email_sender import send_stmp, error_sender

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from macro.utils.common import get_crawling_driver
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from datetime import datetime

from macro.utils.exception_handle import webdriver_exception_handler
from selenium.webdriver.support import expected_conditions as EC

from macro.utils.pages import Pages, Stations

logger = logging.getLogger()

semaphore = threading.Semaphore(value=1)


class ChatBotReservation(viewsets.GenericViewSet, mixins.ListModelMixin, View):

    def train_reservation(self, request):
        logger.debug(f'url : v1/chatbot-train-reservation')
        logger.debug(f'method: POST')
        logger.debug(f'request_data: {request.data}')

        try:
            reservation_model = chatbot_reservation_model_setter(request)
            # validation
            if reservation_model is not None and is_valid_request(reservation_model=reservation_model):

                reserve_thread = threading.Thread(target=train_reserve, args=(reservation_model,))
                reserve_thread.start()
            else:
                return Response(data={"data":"BAD REQUEST!!"}, status=status.HTTP_400_BAD_REQUEST)

            logger.info("스레드를 기다려보자!")
            return Response(data={"msg":"SUCCESS"}, status=status.HTTP_200_OK)
        except Exception as err:
            logger.debug(f'v1/train-reservation error: {traceback.format_exc()}')
            logger.debug(f'train-reservation error:  {err}')
            error_sender(err)
            webdriver_exception_handler()
            return Response(data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




def is_valid_request(reservation_model):
    try:
        req_startingPoint = reservation_model.starting_point
        req_arrivalPoint = reservation_model.arrival_point
        req_date = reservation_model.date
        req_memberNum = reservation_model.member_num
        req_trainType = reservation_model.train_type
        req_contact = reservation_model.contact
        req_seatType = reservation_model.seat_type

        req_memberNum = int(req_memberNum)

        if req_memberNum <= 0:
            logger.info("member plz...!")
            return False

        if req_contact == "":
            logger.info("contact plz...!")
            return False

        # default 일반 좌석
        if req_seatType == "":
            req_seatType = "일반"

        # 현재는 ktx만 지원
        if req_trainType != 'ktx':
            logger.info("ktx plz...!")
            return False

        # 출발역 조회
        if not chk_station(target=req_startingPoint):
            logger.info(f"출발역을 다시 생각해보세요! : {req_startingPoint}")
            return False

        # 도착역 조회
        if not chk_station(target=req_arrivalPoint):
            logger.info(f"도착역을 다시 생각해보세요! : {req_arrivalPoint}")
            return False

        # 주어진 시간이 현재 시간보다 이전인지 확인
        requested_time = datetime.strptime(req_date, "%Y-%m-%d %H")
        current_time = datetime.now()

        if requested_time <= current_time:
            logger.error(f' requested_time : {requested_time}... why..? ')
            return False

        return True
    except Exception as err:
        logger.error(f'train-reservation error:  {err}')
        return False


def chatbot_reservation_model_setter(request):
    data = request.data

    try:
        origin_value = data["action"]["detailParams"]["ReservationEntity"]["origin"]
        parts = origin_value.split(" / ")

        reservation_model = ReservationModel()
        reservation_model.starting_point = parts[0].replace("예매 : ", "").strip()
        reservation_model.arrival_point = parts[1]
        reservation_model.date = parts[2]
        reservation_model.year = reservation_model.date[:4]
        reservation_model.month = reservation_model.date[5:7]
        reservation_model.day = reservation_model.date[8:10]
        reservation_model.hour = reservation_model.date[11:13]
        reservation_model.member_num = parts[3]
        reservation_model.train_type = parts[4]
        reservation_model.contact = parts[5]
        reservation_model.seat_type = parts[6]

        logger.info(f' train models : {reservation_model.__dict__}')
    except Exception as err:
        return None

    return reservation_model


def chk_station(target):
    # 가능한 역 목록
    if target in Stations.VALID_STATIONS:
        return True
    else:
        return False


def train_reserve(reservation_model):
    # 최대 30 분 동안 반복해서 서치
    start_time = time.time()
    end_time = start_time + 30 * 60 * 12

    # get driver - 목록 조회 페이지에서만 동작해야한다.
    reserve_driver = get_crawling_driver()

    url = reserve_driver.current_url
    logger.info(f' current url : {url}')

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

        try:
            # 페이지 새로 고침.
            page_search_refresh(reservation_model=reservation_model)

            for index in range(10):
                logger.info(
                    f"end_time : {end_time_formatted} index : {index} , reservation_model : {reservation_model.__dict__}")
                flag = reservation_loop(reservation_model=reservation_model, index=index)
        except Exception as err:
            logger.debug(f'{traceback.format_exc()}')
            logger.debug(f'{err}')

    logger.info(f' roop end... , {flag}')
    return flag

def page_search_refresh(reservation_model):
    try:
        train_search_url = Pages.KTX_MAIN_PAGE_INDEX
        train_search = get_crawling_driver(url=train_search_url)

        reservation_btn = train_search.find_element(By.XPATH, Buttons.IMG_SRC_LNB_MU01_01)
        reservation_btn.click()
    except Exception as err:
        train_search_url = Pages.KTX_SEARCH_PAGE
        train_search = get_crawling_driver(url=train_search_url)
        # 승차권 예매 페이지 이동 후 driver 초기화
    logger.info(f' 페이지 이동 : {train_search.current_url}')
    train_search.get(train_search.current_url)

    start_station = train_search.find_element(By.ID, Buttons.START)
    arrival_station = train_search.find_element(By.ID, Buttons.GET)

    month = train_search.find_element(By.ID, Buttons.S_MONTH)
    day = train_search.find_element(By.ID, Buttons.S_DAY)
    hour = train_search.find_element(By.ID, Buttons.S_HOUR)
    members = train_search.find_element(By.ID, Buttons.S_MEMBER)

    # 초기화
    start_station.clear()
    arrival_station.clear()

    # 사용자 요청 값으로 세팅
    start_station.send_keys(reservation_model.starting_point)
    arrival_station.send_keys(reservation_model.arrival_point)
    month.send_keys(reservation_model.month)
    day.send_keys(reservation_model.day)

    monthSelect = Select(month)
    monthSelect.select_by_value(reservation_model.month)

    daySelect = Select(day)
    daySelect.select_by_value(reservation_model.day)

    hourSelect = Select(hour)
    hourSelect.select_by_value(reservation_model.hour)

    # 사용자 요청 수 대로 선택
    memberSelect = Select(members)
    memberSelect.select_by_value(reservation_model.member_num)

        # 요청 차종 선택
    if reservation_model.train_type == "ktx":
        train_btn = train_search.find_element(By.ID, Buttons.SELECT_TRAIN_KTX)
        train_btn.click()

    # 조회 요청
    search_btn = train_search.find_element(By.XPATH, Buttons.IMG_SRC_BTN_ING_TICK)
    search_btn.click()

    # 조회 시, 아이프레임 알림 뜨는 경우 처리.
    try:
        iframe = WebDriverWait(train_search, 1).until(
            EC.presence_of_element_located(By.TAG_NAME, Buttons.IFRAME)
        )
        train_search.switch_to.frame(iframe)

        element = train_search.find_element(By.XPATH, Buttons.IFRAME_CLOSE)
        element.click()

        # iframe에서 빠져나옴
        train_search.switch_to.default_content()

    except Exception as err:
        logger.info(f'알림없음 계속 진행. ')

    train_search.implicitly_wait(3)
    reserve_driver = get_crawling_driver()
    logger.info(f' 대기 팝업 확인... ')
    WebDriverWait(reserve_driver, 60
                  ).until_not(EC.presence_of_element_located((By.ID, 'NetFunnel_Loading_Popup')))
    logger.info(f' 대기 팝업 종료 확인 예약 진행합니다! ')


def reservation_loop(reservation_model, index):

    reserve_driver = get_crawling_driver()

    # 조회 결과 테이블
    table = None
    trs = None
    tr = None
    try:
        table = reserve_driver.find_element(By.ID, Buttons.TABLE_RESULT)
        trs = table.find_elements(By.TAG_NAME, Buttons.TABLE_TR)

        # for tr in trs:
        tr = trs[index]
        count = 0
    except Exception as err:
        logger.info(f'loop exit!!! : {index}')
        return True

    try:
        td_objs = tr.find_elements(By.TAG_NAME, Buttons.TABLE_TD)

        for td in td_objs:
            count += 1

            # td object에는 여러가지 값들이 있어서 필요한 값이 있는 순번에만 검색하도록 수정.
            if count not in {3, 4, 5, 6}:
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
                element = td.find_element(By.TAG_NAME, Buttons.TAG_NAME_IMG)

                img_name = element.get_attribute(Buttons.ATTRIBUTE_NAME)
                btn_names_special = {f"btnRsv2_{i}" for i in range(10)}

                if img_name in btn_names_special:
                    if reservation_model.seat_type == Seat.SPECIAL_SEAT:
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
                                iframe = reserve_driver.find_element(By.TAG_NAME, Buttons.IFRAME)
                                reserve_driver.switch_to.frame(iframe)

                                element = reserve_driver.find_element(By.XPATH, Buttons.IFRAME_CLOSE_BTN_BLUE)

                                if element:
                                    element.click()

                                # iframe에서 빠져나옴
                                reserve_driver.switch_to.default_content()

                            except Exception as err:
                                logger.info(f'iframe not found... keep go! ')

                            while True:
                                try:
                                    # alert 창 확인 처리.
                                    alert = Alert(reserve_driver)
                                    alert.accept()
                                except:
                                    break

                            reservation_model.go = go
                            logger.info(f' 특실 예약합니다. {go} , {reservation_model.__dict__}')

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
                element = td.find_element(By.TAG_NAME, Buttons.TAG_NAME_IMG)

                img_name = element.get_attribute(Buttons.ATTRIBUTE_NAME)
                btn_names_special = {f"btnRsv1_{i}" for i in range(10)}

                if img_name in btn_names_special:

                    if reservation_model.seat_type == Seat.ECONOMY_SEAT:
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
                                iframe = reserve_driver.find_element(By.TAG_NAME, Buttons.IFRAME)
                                reserve_driver.switch_to.frame(iframe)

                                element = reserve_driver.find_element(By.XPATH, Buttons.IFRAME_CLOSE_BTN_BLUE)

                                if element:
                                    element.click()

                                # iframe에서 빠져나옴
                                reserve_driver.switch_to.default_content()

                            except Exception as err:
                                logger.info(f'iframe not found... keep go! ')

                            while True:
                                try:
                                    # alert 창 확인 처리.
                                    alert = Alert(reserve_driver)
                                    alert.accept()
                                except:
                                    break

                            # 선택한 출발 시간 세팅
                            reservation_model.go = go
                            logger.info(f'일반실 예약합니다. {go} , {reservation_model.__dict__}')

                            # 예매 정보 이메일로 통보
                            send_stmp(reservation_model=reservation_model)

                            # 장바구니에 담김
                            return True

            except Exception as err:
                logger.info(f'v1/train-reservation error 1: {traceback.format_exc()}')
                logger.info(f'{err}')
                logger.info("일반실 매진")

    except Exception as err:
        logger.error(f'v1/train-reservation error 2: {traceback.format_exc()}')
        logger.error(f'{err}')

    return False
