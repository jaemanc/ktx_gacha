from macro.trainreservation.chatbot_login import ChatBotLogin
from macro.trainreservation.chatbot_reservation import ChatBotReservation
from macro.trainreservation.chatbot_search_train import ChatBotSearchTrain
from macro.trainreservation.say_hello import Chatbot

from django.urls import path


urlpatterns = [
    path('v1/chat-test', Chatbot.as_view(({"post": "chatbot_test"}))),
    path('v1/chatbot-login', ChatBotLogin.as_view(({"post": "login_to_website"}))),
    path('v1/chatbot-train', ChatBotSearchTrain.as_view(({"post": "get_train"}))),
    path('v1/chatbot-train-reservation', ChatBotReservation.as_view(({"post": "train_reservation"})))
]
