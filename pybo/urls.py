from django.contrib import admin
from django.urls import path

from pybo import views

app_name = 'pybo'

urlpatterns = [
    path("", views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    # path("ocr.html/", views.ocr_page, name='ocr'),
]