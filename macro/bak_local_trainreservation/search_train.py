import logging
import threading
import traceback

from django.views import View
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from macro.utils.common import get_crawling_driver
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from macro.utils.exception_handle import webdriver_exception_handler
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger()


class Train(viewsets.GenericViewSet, mixins.ListModelMixin, View):

    # 목록 조회
    def get_train(self, request):
        logger.debug(f'url : v1/train')
        logger.debug(f'method: GET')
        logger.debug(f'request_data: {request.data}')

        try:
            # 오늘 날짜 이전 데이터 조회 방어
            if is_valid_date(request):

                get_train_thread = threading.Thread(target=get_train_list, args=(request,))
                get_train_thread.start()

                # row_data = get_train_list(request)
                return Response(data=" 조회 결과는 이메일로..? ", status=status.HTTP_200_OK)
            else:
                return Response(data=None, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            logger.debug(f'v1/train error: {traceback.format_exc()}')
            logger.debug(f'get train list error:  {err}')
            webdriver_exception_handler()
            return Response(data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def is_valid_date(request):
    req_date = request.query_params.get("date", "1993-07-17 01")
    # 주어진 날짜와 시간을 datetime 객체로 변환
    requested_time = datetime.strptime(req_date, "%Y-%m-%d %H")

    # 현재 시간 구하기
    current_time = datetime.now()

    # 주어진 시간이 현재 시간보다 이전인지 확인
    if requested_time <= current_time:
        logger.info(f' requested_time : {requested_time}... why..? ')
        return False
    else:
        return True


def get_train_list(request):
    req_startingPoint = request.query_params.get("startingPoint", "용산")
    req_arrivalPoint = request.query_params.get("arrivalPoint", "익산")
    req_date = request.query_params.get("date", "1993-07-17 01")

    req_year = req_date[:4]
    req_month = req_date[5:7]
    req_day = req_date[8:10]
    req_hour = req_date[11:13]  # 00~ 23 까지

    req_memberNum = request.query_params.get("memberNum", "1")
    req_trainType = request.query_params.get("trainType", "ktx")

    # 조회 로직 리팩토링
    try:
        train_search_url = "https://www.letskorail.com/index.jsp"
        train_search = get_crawling_driver(url=train_search_url)

        reservation_btn = train_search.find_element(By.XPATH, '//img[@src="/images/lnb_mu01_01.gif"]')
        reservation_btn.click()
    except Exception as err:
        train_search_url = "https://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do"
        train_search = get_crawling_driver(url=train_search_url)


    # 승차권 예매 페이지 이동 후 driver 초기화
    logger.info(f' 페이지 이동 : {train_search.current_url}')
    train_search.get(train_search.current_url)

    start_station = train_search.find_element(By.ID, "start")
    arrival_station = train_search.find_element(By.ID, "get")

    month = train_search.find_element(By.ID, "s_month")
    day = train_search.find_element(By.ID, "s_day")
    hour = train_search.find_element(By.ID, "s_hour")
    members = train_search.find_element(By.ID, "peop01")

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

    hourSelect = Select(hour)
    hourSelect.select_by_value(req_hour)

    # 사용자 요청 수 대로 선택
    memberSelect = Select(members)
    memberSelect.select_by_value(req_memberNum)

    logger.info(f' 요청 시간 : {req_year} / {req_month} / {req_day} / {req_hour}')

    # 요청 차종 선택
    if req_trainType == "ktx":
        train_btn = train_search.find_element(By.ID, "selGoTrainRa00")
        train_btn.click()

    # 조회 요청
    search_btn = train_search.find_element(By.XPATH, '//img[@src="/images/btn_inq_tick.gif"]')
    search_btn.click()

    # 조회 후에 가끔 아이프레임 페이지 뜨는 경우 있음 없는 경우를 위해 시간 단축 처리.
    try:
        iframe = WebDriverWait(train_search, 1).until(
            EC.presence_of_element_located(By.TAG_NAME, 'iframe')
        )
        train_search.switch_to.frame(iframe)

        element = train_search.find_element(By.XPATH, '//a[@class="plainmodal-close"]')
        element.click()

        # iframe에서 빠져나옴
        train_search.switch_to.default_content()

    except Exception as err:
        logger.info(f' 계속 진행. ')

    train_search.implicitly_wait(3)

    table = train_search.find_element(By.ID, "tableResult")

    trs = table.find_elements(By.TAG_NAME, "tr")

    row_data = []

    for tr in trs:
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
                    row_data.append({
                        "go": go,
                        "end": end,
                        "kind": "특실"
                    })

            except NoSuchElementException as err:
                logger.info("특실 매진")

            try:
                # 일반실
                element = td.find_element(By.TAG_NAME, "img")

                img_name = element.get_attribute("name")
                btn_names_special = {f"btnRsv1_{i}" for i in range(10)}

                if img_name in btn_names_special:
                    row_data.append({
                        "go": go,
                        "end": end,
                        "kind": "일반"
                    })

            except NoSuchElementException as err:
                logger.info("일반실 매진")

    logger.info(row_data)

    return row_data
