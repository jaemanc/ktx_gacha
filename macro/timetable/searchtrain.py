import logging
import traceback

from django.views import View
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from macro.common import get_web_site_crawling
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from datetime import datetime

logger = logging.getLogger()


class Train(viewsets.GenericViewSet, mixins.ListModelMixin, View):

    # 목록 조회
    def get_train(self, request):
        logger.debug(f'url : v1/train')
        logger.debug(f'method: GET')
        logger.debug(f'request_data: {request.data}')

        try:
            row_data = get_train_list(request)

        except Exception as err:
            logger.debug(f'v1/train error: {traceback.format_exc()}')
            logger.debug(f'get train list error:  {err}')
            return Response(data=row_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=row_data, status=status.HTTP_200_OK)


def get_train_list(request):
    req_startingPoint = request.query_params.get("startingPoint", "용산")
    req_arrivalPoint = request.query_params.get("arrivalPoint", "익산")
    req_date = request.query_params.get("date", "1993-07-17")

    req_year = req_date[:4]
    req_month = req_date[5:7]
    req_day = req_date[8:]

    req_memberNum = request.query_params.get("memberNum", "1")
    req_trainType = request.query_params.get("trainType", "ktx")

    train_search_url = "https://www.letskorail.com/index.jsp"
    train_search = get_web_site_crawling(url=train_search_url)

    reservation_btn = train_search.find_element(By.XPATH, '//img[@src="/images/lnb_mu01_01.gif"]')
    reservation_btn.click()

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
    hour.send_keys(0)

    # 사용자 요청 수 대로 선택
    memberSelect = Select(members)
    memberSelect.select_by_value(req_memberNum)

    # 요청 차종 선택
    if req_trainType == "ktx":
        train_btn = train_search.find_element(By.ID, "selGoTrainRa00")
        train_btn.click()

    # 조회 요청
    search_btn = train_search.find_element(By.XPATH, '//img[@src="/images/btn_inq_tick.gif"]')
    search_btn.click()

    train_search.implicitly_wait(3)

    # 조회 결과 테이블 정보 파싱
    # train_search.get(train_search.current_url)
    # logger.info(f' 페이지 이동 : {train_search.current_url}' )
    table = train_search.find_element(By.ID, "tableResult")

    trs = table.find_elements(By.TAG_NAME, "tr")

    row_data = []

    for tr in trs:
        count = 0
        td_objs = tr.find_elements(By.TAG_NAME, "td")

        for td in td_objs:
            count += 1
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
                if count == 5:
                    a_tag = td.find_element(By.TAG_NAME, "a")
                    if a_tag:
                        img_tag = a_tag.find_element(By.TAG_NAME, "img")
                        # btnRsv2_2 값이면 예매 가능
                        if img_tag:
                            btn_name = img_tag.get_attribute('name')
                            if btn_name.__eq__("btnRsv2_0") or btn_name.__eq__("btnRsv2_1")\
                                    or btn_name.__eq__("btnRsv2_2") or btn_name.__eq__("btnRsv2_3")\
                                    or btn_name.__eq__("btnRsv2_4") or btn_name.__eq__("btnRsv2_5")\
                                    or btn_name.__eq__("btnRsv2_6") or btn_name.__eq__("btnRsv2_7")\
                                    or btn_name.__eq__("btnRsv2_8") or btn_name.__eq__("btnRsv2_9"):
                                row_data.append({
                                    "go": go,
                                    "end": end,
                                    "kind": "특실"
                                })
            except NoSuchElementException as err:
                logger.info("특실 매진")

            try:
                # 일반실
                if count == 6:
                    a_tag = td.find_element(By.TAG_NAME, "a")
                    if a_tag:
                        img_tag = a_tag.find_element(By.TAG_NAME, "img")
                        # btnRsv1_0 값이면 예매 가능
                        if img_tag:
                            btn_name = img_tag.get_attribute('name')
                            if btn_name.__eq__("btnRsv1_0") or btn_name.__eq__("btnRsv1_1") \
                                    or btn_name.__eq__("btnRsv1_2") or btn_name.__eq__("btnRsv1_3") \
                                    or btn_name.__eq__("btnRsv1_4") or btn_name.__eq__("btnRsv1_5") \
                                    or btn_name.__eq__("btnRsv1_6") or btn_name.__eq__("btnRsv1_7") \
                                    or btn_name.__eq__("btnRsv1_8") or btn_name.__eq__("btnRsv1_9"):
                                row_data.append({
                                    "go": go,
                                    "end": end,
                                    "kind": "일반실"
                                })


            except NoSuchElementException as err:
                logger.info("일반실 매진")

    logger.info(row_data)

    return row_data
