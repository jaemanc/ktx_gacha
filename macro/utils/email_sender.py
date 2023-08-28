import logging
import os
from email.message import EmailMessage

from django.views import View
from rest_framework import viewsets, mixins

import smtplib
from email.mime.text import MIMEText

logger = logging.getLogger()

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
class EmailSender(viewsets.GenericViewSet, mixins.ListModelMixin, View):

    # 로컬 테스트용 API
    def email_sender(self, request):

        send_stmp(reservation_model=request.data)

        logger.info(f' request data : {request.data}')


        return None

def send_stmp(reservation_model):
    # 1. SMTP 서버 연결
    smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)

    EMAIL_ADDR = os.environ['GMAIL_SENDER']
    EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

    # 2. SMTP 서버에 로그인
    smtp.login(EMAIL_ADDR, EMAIL_PASSWORD)

    # 3. MIME 형태의 이메일 메세지 작성
    message = EmailMessage()

    msg_content = (
        '\n'
        'ktx-gacha 성공! \n \n'
        '############################\n'
        '출발 : {} \n'
        '도착 : {} \n'
        '일시 : {}-{}-{}/{} \n'
        '열차 : {} / {} \n'
        '인원 : {} \n'
        '############################\n'
    ).format(
        reservation_model.starting_point,
        reservation_model.arrival_point,
        reservation_model.year, reservation_model.month, reservation_model.day, reservation_model.go,
        reservation_model.train_type, reservation_model.seat_type,
        reservation_model.member_num
    )

    message.set_content(msg_content)
    message["Subject"] = "예매 내역을 확인해주세요!"
    message["From"] = EMAIL_ADDR  # 보내는 사람의 이메일 계정
    message["To"] = reservation_model.contact

    # 4. 서버로 메일 보내기
    smtp.send_message(message)

    # 5. 메일을 보내면 서버와의 연결 끊기
    smtp.quit()
