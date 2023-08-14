from django.urls import path

from macro.login import Login
from macro.timetable.searchtrain import Train

urlpatterns = [
    path('v1/trains', Train.as_view(({"get": "get_train"}))),
]

