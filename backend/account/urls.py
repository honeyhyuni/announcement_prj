from django.urls import path

from account import views

urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name='login')
]