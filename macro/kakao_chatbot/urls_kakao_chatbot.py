from macro.kakao_chatbot.say_hello import Chatbot

from django.urls import path


urlpatterns = [
    path('v1/chat-test', Chatbot.as_view(({"post": "chatbot_test"}))),
]
