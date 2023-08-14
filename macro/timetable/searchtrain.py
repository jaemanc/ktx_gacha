import logging
import traceback

from django.views import View
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
            pages = get_train_list(request)
        except Exception as err:
            logger.debug(f'v1/train error: {traceback.format_exc()}')
            logging.debug(f'update_user_profile_info ERROR :: {err}')
            return Response(data=pages, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=pages, status=status.HTTP_200_OK)


def get_train_list(request):
    req_startingPoint = request.query_params.get("startingPoint", "용산")
    req_arrivalPoint = request.query_params.get("arrivalPoint", "익산")
    req_date = request.query_params.get("date", "1993-07-17")

    req_year = req_date[:4]
    req_month = req_date[5:7]  # 5번째부터 6번째까지는 월
    req_day = req_date[8:]  # 8번째부터 끝까지는 일

    req_memberNum = request.query_params.get("memberNum", "1")
    req_trainType = request.query_params.get("trainType", "ktx")

    train_search_url = "https://www.letskorail.com/index.jsp"
    train_search = get_web_site_crawling(url=train_search_url)

    reservation_btn = train_search.find_element(By.XPATH, '//img[@src="/images/lnb_mu01_01.gif"]')
    reservation_btn.click()

    # 승차권 예매 페이지 이동 후 driver 초기화
    logger.info(f' 페이지 이동 : {train_search.current_url}' )
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

    return train_search
