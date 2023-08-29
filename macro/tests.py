import os
import smtplib
from email.message import EmailMessage

from django.test import TestCase
from selenium import webdriver
import logging


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
logger = logging.getLogger()

class MySeleniumTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_example(self):
        self.driver.get("https://www.naver.com")
        logger.info(f' crawlling..? {self.driver.get("https://www.naver.com")}')
        logger.info(f' test? ', self.driver)

    def test_emailsend(self):

        # 1. SMTP 서버 연결
        smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)

        EMAIL_ADDR = os.environ['GMAIL_SENDER']
        EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

        # 2. SMTP 서버에 로그인
        smtp.login(EMAIL_ADDR, EMAIL_PASSWORD)

        # 3. MIME 형태의 이메일 메세지 작성
        message = EmailMessage()
        message.set_content('메일 테스트합니다.')
        message["Subject"] = "이메일 제목"
        message["From"] = EMAIL_ADDR  # 보내는 사람의 이메일 계정
        message["To"] = 'jaemanc93@gmail.com'

        # 4. 서버로 메일 보내기
        smtp.send_message(message)

        # 5. 메일을 보내면 서버와의 연결 끊기
        smtp.quit()

        return None
