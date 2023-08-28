from macro.timetable.train_reservation import TrainReservation

from django.urls import path

from macro.timetable.search_train import Train

urlpatterns = [
    path('v1/trains', Train.as_view(({"get": "get_train"}))),
    path('v1/train-reservation', TrainReservation.as_view({"post":"train_reservation"})),
]
