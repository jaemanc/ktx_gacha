from macro.timetable.train_reservation import TrainReservation

from django.urls import path

from macro.login import Login
from macro.timetable.searchtrain import Train

urlpatterns = [
    path('v1/trains', Train.as_view(({"get": "get_train"}))),
    path('v1/train-reservattion', TrainReservation.as_view({"post":"train_reservation"})),
]
