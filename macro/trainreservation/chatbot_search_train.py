import logging
import threading
import traceback
import requests

from django.views import View
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from macro.utils.buttons import Buttons, Seat
from macro.utils.common import get_crawling_driver, use_call_back_msg, \
    train_list_and_callback_chatbot_response_message
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from datetime import datetime

from macro.utils.email_sender import error_sender
from macro.utils.exception_handle import webdriver_exception_handler
from selenium.webdriver.support import expected_conditions as EC

from macro.utils.pages import Pages

logger = logging.getLogger()

class ChatBotSearchTrain(viewsets.GenericViewSet, mixins.ListModelMixin, View):

    def get_train(self, request):
        logger.debug(f'url : v1/chatbot-train')
        logger.debug(f'method: POST')
        logger.debug(f'request_data: {request.data}')

        try:
            # 오늘 날짜 이전 데이터 조회 유효성 검사
            if is_valid_date_chatbot(request):

                # 챗봇 콜백 정책으로 인해 응답 우선 비동기 처리.
                get_train_thread = threading.Thread(target=get_train_list_chatbot, args=(request,))
                get_train_thread.start()

                return Response(data=use_call_back_msg(), status=status.HTTP_200_OK)
            else:
                return Response(data=None, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            logger.debug(f'v1/chatbot-train error: {traceback.format_exc()}')
            logger.debug(f'get train list error:  {err}')
            error_sender(err)
            webdriver_exception_handler()
            return Response(data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def is_valid_date_chatbot(request):
    try:
        data = request.data
        origin_value = data["action"]["detailParams"]["TrainListEntity"]["origin"]
        parts = origin_value.split(" / ")

        date_time = parts[2]  # 일시

        logger.info(date_time)

        req_date = date_time
        # 주어진 날짜와 시간을 datetime 객체로 변환
        requested_time = datetime.strptime(req_date, "%Y-%m-%d %H")

        # 현재 시간 구하기
        current_time = datetime.now()

        # 주어진 시간이 현재 시간보다 이전인지 확인
        if requested_time <= current_time:
            logger.info(f' requested_time : {requested_time} 오늘 날짜 이전 요청은 불가능합니다!')
            return False
        else:
            return True
    except Exception as err:
        return False


def get_train_list_chatbot(request):
    data = request.data
    TrainListEntity = data["action"]["detailParams"]["TrainListEntity"]["origin"]


    """
        starting_point : 용산
        arrival_point : 익산
        date_time : 2023-08-25 01
        member_num : 1
        train_type : ktx
    """
    parts = TrainListEntity.split(" / ")

    starting_point = parts[0].replace("조회 : ","").strip()  # 출발역
    arrival_point = parts[1]  # 도착역
    date_time = parts[2]  # 일시
    member_num = parts[3]  # 인원 수
    train_type = parts[4]  # 열차 종류

    logger.info(f' TrainListEntity : {TrainListEntity} ')

    req_startingPoint = starting_point
    req_arrivalPoint = arrival_point
    req_date = date_time

    req_year = req_date[:4]
    req_month = req_date[5:7]
    req_day = req_date[8:10]
    req_hour = req_date[11:13] # 00~ 23 까지

    req_memberNum = member_num
    req_trainType = train_type

    # 조회 로직 리팩토링
    try:
        train_search_url = Pages.KTX_MAIN_PAGE_INDEX
        train_search = get_crawling_driver(url=train_search_url)

        reservation_btn = train_search.find_element(By.XPATH, Buttons.IMG_SRC_LNB_MU01_01 )
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
    start_station.send_keys(req_startingPoint)
    arrival_station.send_keys(req_arrivalPoint)
    month.send_keys(req_month)
    day.send_keys(req_day)

    monthSelect = Select(month)
    monthSelect.select_by_value(req_month)

    daySelect = Select(day)
    daySelect.select_by_value(req_day)

    hourSelect = Select(hour)
    hourSelect.select_by_value(req_hour)

    # 사용자 요청 수 대로 선택
    memberSelect = Select(members)
    memberSelect.select_by_value(req_memberNum)

    logger.info(f' 요청 시간 : {req_year} / {req_month} / {req_day} / {req_hour}')

    # 요청 차종 선택
    if req_trainType == Buttons.SELECT_TRAIN_KTX:
        train_btn = train_search.find_element(By.ID, Buttons.SELECT_TRAIN_KTX)
        train_btn.click()

    # 조회 요청
    search_btn = train_search.find_element(By.XPATH, Buttons.IMG_SRC_BTN_ING_TICK)
    search_btn.click()

    # 조회 후에 가끔 아이프레임 페이지 뜨는 경우 있음 없는 경우를 위해 시간 단축 처리.
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
        logger.info(f' 계속 진행. ')

    train_search.implicitly_wait(3)

    table = train_search.find_element(By.ID, Buttons.TABLE_RESULT)

    trs = table.find_elements(By.TAG_NAME, Buttons.TABLE_TR)

    row_data = []

    for tr in trs:
        count = 0
        td_objs = tr.find_elements(By.TAG_NAME, Buttons.TABLE_TD)

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
                element = td.find_element(By.TAG_NAME, Buttons.TAG_NAME_IMG)

                img_name = element.get_attribute(Buttons.ATTRIBUTE_NAME)
                btn_names_special = {f"btnRsv2_{i}" for i in range(10)}

                if img_name in btn_names_special:
                    row_data.append({
                        "go": go,
                        "end": end,
                        "kind": Seat.SPECIAL_SEAT
                    })

            except NoSuchElementException as err:
                logger.info("특실 매진")

            try:
                # 일반실
                element = td.find_element(By.TAG_NAME, Buttons.TAG_NAME_IMG)

                img_name = element.get_attribute(Buttons.ATTRIBUTE_NAME)
                btn_names_special = {f"btnRsv1_{i}" for i in range(10)}

                if img_name in btn_names_special:
                    row_data.append({
                        "go": go,
                        "end": end,
                        "kind": Seat.ECONOMY_SEAT
                    })

            except NoSuchElementException as err:
                logger.info("일반실 매진")

    train_list = ""
    if row_data:
        for entry in row_data:
            train_list += (
                '--------------------\n'
                '출발: {}\n도착: {}\n출발 시간: {}\n도착 시간: {}\n열차 타입: {}\n\n'
                .format(
                    entry['go'].split()[0], entry['end'].split()[0],
                    entry['go'].split()[1], entry['end'].split()[1],
                    entry['kind']
                )
            )

    response = train_list_and_callback_chatbot_response_message(train_list=train_list)
    logger.info(response)

    # 조회 사항 콜백 하단부 예약 버튼 포함
    callback_response = requests.post(request.data["userRequest"]["callbackUrl"], json=response, headers={"Content-Type": "application/json"})

    logger.info(callback_response.__dict__)
    return response
