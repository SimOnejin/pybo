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
from pybo.models import Voca
from pybo.models import VocaList

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

    random.shuffle(matched_pairs)

    # matchedPairs를 템플릿에 전달
    context = {'combined_list': matched_pairs, "content": content}

    # 템플릿 렌더링
    return render(request, 'pybo/voca_save_success.html', context)



@login_required(login_url='common:login')
def vocaTest(request):
    user_id = request.user
    voca = Voca
    print("출력0")
    vocaList = voca.objects.raw("SELECT voca_idx, voca_japan, voca_korea FROM {}_voca".format(user_id))
    for item in vocaList:
        print("출력1", item.voca_idx, item.voca_japan, item.voca_korea)
    # vocaList = [{'voca_japan' : 'あ', 'voca_korea' : '아'},
    #             {'voca_japan' : 'い', 'voca_korea' : '이'},
    #             {'voca_japan' : 'う', 'voca_korea' : '우'},
    #             {'voca_japan' : 'え', 'voca_korea' : '에'},
    #             {'voca_japan' : 'お', 'voca_korea' : '오'}]
    random.shuffle(vocaList)
    print("출력2")

    # 정답과 오답 자리를 섞기위한 리스트생성
    randomPosition = []
    for i in range(len(vocaList)):
        print("출력3"+ vocaList[i])
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

