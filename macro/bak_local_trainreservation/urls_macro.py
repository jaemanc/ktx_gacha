from django.urls import path

from macro.bak_local_trainreservation.login import Login

urlpatterns = [
    path('v1/login', Login.as_view(({"post": "login_to_website"}))),
]

