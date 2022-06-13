from django.urls import path
from basic_app.views import register, logout, login

app_name = "basic_app"

urlpatterns = [
    path("register/", register, name="register"),
    path("logout/", logout, name="logout"),
    path("login/", login, name="login"),

]