from django.urls import path

from company import views

urlpatterns =[
    path("", views.CompanyListAPIView.as_view(), name='test'),
]