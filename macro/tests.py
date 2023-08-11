from django.test import TestCase
from selenium import webdriver
import logging

# Create your tests here.

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
