from django.urls import path
from . import views
from .views import base_views, question_views, answer_views, comment_views, vote_views

# 이미지를 업로드하자
from django.conf.urls.static import static
from django.conf import settings

app_name = 'pybo'

urlpatterns = [
    # base_views.py
    path('',
         base_views.index, name='index'),
    path('<int:question_id>/',
         base_views.detail, name='detail'),

    path('voca/create/',
         base_views.voca_create, name='voca_create'),
    path('voca/list/',
         base_views.voca_list, name='voca_list'),
    path('voca/detail/<int:voca_id>/',
         base_views.voca_detail, name='voca_detail'),
    path('ocr/<int:voca_id>/',
         base_views.ocrTest1, name='ocrTest1'),

    # question_views.py
    path('question/create/',
         question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/',
         question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/',
         question_views.question_delete, name='question_delete'),
    path('question/vote/<int:question_id>/', question_views.question_vote, name='question_vote'),

    # answer_views.py
    path('answer/create/<int:question_id>/',
         answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/',
         answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/',
         answer_views.answer_delete, name='answer_delete'),
    path('answer/vote/<int:answer_id>/', answer_views.answer_vote, name='answer_vote'),


    #path의 첫번째 인자""는 주소창에 보일주소, 두번째는 호출할 함수
    # path("ocr/", views.base_views.ocr_page, name='ocr_page'),
    # path('ocr/', views.base_views.upload_image, name='upload_image'),

    path('ocr/<int:question_id>/',
         base_views.ocrTest, name='ocrTest'),
    path('ocr_lists/', base_views.shuffle, name='shuffle'),
    path('trans/', base_views.translate, name='translate'),
    path('t', base_views.session_reset, name='session_reset'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
