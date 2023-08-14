from django.urls import path

from macro.login import Login

urlpatterns = [
    path('v1/login', Login.as_view(({"post": "login_to_website"}))),
]

