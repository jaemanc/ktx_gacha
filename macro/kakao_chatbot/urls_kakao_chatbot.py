from macro.kakao_chatbot.chatbot_login import ChatBotLogin
from macro.kakao_chatbot.say_hello import Chatbot

from django.urls import path


urlpatterns = [
    path('v1/chat-test', Chatbot.as_view(({"post": "chatbot_test"}))),
    path('v1/chatbot-login', ChatBotLogin.as_view(({"post": "login_to_website"}))),

]
