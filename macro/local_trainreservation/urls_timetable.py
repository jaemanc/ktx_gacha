from macro.local_trainreservation.train_reservation import TrainReservation

from django.urls import path

from macro.local_trainreservation.search_train import Train
from macro.utils.email_sender import EmailSender

urlpatterns = [
    path('v1/trains', Train.as_view(({"get": "get_train"}))),
    path('v1/train-reservation', TrainReservation.as_view({"post":"train_reservation"})),
    path('v1/email', EmailSender.as_view({"post": "email_sender"})),

]
