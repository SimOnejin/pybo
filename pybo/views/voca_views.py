from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
import os
import random
from googletrans import Translator
import json


from django.contrib.auth.decorators import login_required
from django.utils import timezone
from pybo.forms import VocaForm
from pybo.models import VocaList
from pybo.models import Voca

from django.utils.encoding import force_str

from ..models import Question
from ..models import Article

from ..ocr import Nice
from ..forms import UserImageForm



@login_required(login_url='common:login')
def voca_save(request):
    # URL 매개변수에서 matchedPairs 가져오기
    content = request.GET.get('content', '')
    matched_pairs_json = request.GET.get('matchedPairs', '[]')

    # JSON 형식의 문자열을 파이썬 리스트로 변환
    matched_pairs = json.loads(matched_pairs_json)

    user_id = request.user

    # print(user_id)

    #리스트 저장
    for pair in matched_pairs:
        print(pair["text"])
        print(pair["translate"])
        print(str(user_id))
        vocaList = VocaList(
            user_id=str(user_id),
            voca_japan=pair["text"],
            voca_korea=pair["translate"],
            voca_class=content
        )
        vocaList.save()

    # 템플릿 렌더링
    return render(request, 'pybo/voca_save_success.html')


@login_required(login_url='common:login')
def vocaTest1(request):
    user_id = request.user
    voca = VocaList()
    vocaList = voca.select()
    random.shuffle(vocaList)


    # 정답과 오답 자리를 섞기위한 리스트생성
    randomPosition = []
    for i in range(len(vocaList)):
        ranList = [0,1,2,3]
        random.shuffle(ranList)
        randomPosition.append(ranList)


    # 정답과 함께 출력할 오답의 리스트 생성 - 0번 인덱스가 정답 1~3번 인덱스가 오답
    randAnswer = []
    for i in range(len(vocaList)):
        answers = []
        answers.append(i)
        for j in range(1, 4):
            while (True):
                answer = random.randrange(len(vocaList))

                dupChk = True
                for k in range(0, j):
                    if (answers[k] == answer):
                        dupChk = False
                        break

                if (dupChk):
                    answers.append(answer)
                    break

        for j in range(4):
            answers[j] = vocaList[answers[j]]["voca_korea"]

        randAnswer.append(answers)

    # vocaList = 단어장, randomPosition = 정답 위치, randAnswer = 선택지
    datas = {"vocaList": vocaList,
             "randomPosition": randomPosition,
             "randAnswer": randAnswer}

    return render(request, 'pybo/voca_test.html', datas)







@login_required(login_url='common:login')
def vocaTest(request):
    user_id = request.user
    voca = VocaList()
    vocaList = voca.objects.raw("select * from " + str(user_id) + "_voca")
    # vocaList = [{'voca_japan': 'あ', 'voca_korea': '아'},
    #             {'voca_japan': 'い', 'voca_korea': '이'},
    #             {'voca_japan': 'う', 'voca_korea': '우'},
    #             {'voca_japan': 'え', 'voca_korea': '에'},
    #             {'voca_japan': 'お', 'voca_korea': '오'}]

    random.shuffle(vocaList)


    # 정답과 오답 자리를 섞기위한 리스트생성
    randomPosition = []
    for i in range(len(vocaList)):
        ranList = [0,1,2,3]
        random.shuffle(ranList)
        randomPosition.append(ranList)


    # 정답과 함께 출력할 오답의 리스트 생성 - 0번 인덱스가 정답 1~3번 인덱스가 오답
    randAnswer = []
    for i in range(len(vocaList)):
        answers = []
        answers.append(i)
        for j in range(1, 4):
            while (True):
                answer = random.randrange(len(vocaList))

                dupChk = True
                for k in range(0, j):
                    if (answers[k] == answer):
                        dupChk = False
                        break

                if (dupChk):
                    answers.append(answer)
                    break

        for j in range(4):
            answers[j] = vocaList[answers[j]]["voca_korea"]

        randAnswer.append(answers)

    # vocaList = 단어장, randomPosition = 정답 위치, randAnswer = 선택지
    datas = {"vocaList": vocaList,
             "randomPosition": randomPosition,
             "randAnswer": randAnswer}

    return render(request, 'pybo/voca_test.html', datas)

