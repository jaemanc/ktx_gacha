from django.urls import path

from macro import login

urlpatterns = [
    path('v1/login', login.login_web_site)
]

