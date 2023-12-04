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
    voca_list = VocaList()
    vocaList = voca_list.select(user_id=str(user_id), voca_class='f')
    random.shuffle(vocaList)

    for item in vocaList:
        print(item)

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
            answer_index = int(answers[j])
            answer_instance = vocaList[answer_index]
            answers[j] = answer_instance.voca_korea

        randAnswer.append(answers)

    # vocaList = 단어장, randomPosition = 정답 위치, randAnswer = 선택지
    datas = {"vocaList": vocaList,
             "randomPosition": randomPosition,
             "randAnswer": randAnswer}

    return render(request, 'pybo/voca_test.html', datas)


@login_required(login_url='common:login')
def vocaRead(request):
    user_id = request.user

    vocaList = VocaList.select(user_id)
    vocalist_class = set(item[3] for item in vocaList)

    print("vocaList: ", vocaList)
    print("vocalist_class: ", vocalist_class)

    if request.method == 'POST':
        global selected_voca_list
        selected_voca_class = request.POST.get('voca_class')  # 드롭다운에서 선택된 값 가져오기
        print("voca_class: ", selected_voca_class)
        selected_voca_list = VocaList.select_where(user_id, selected_voca_class)
        vocaList = VocaList.select(user_id)
        vocalist_class = set(item[3] for item in vocaList)
        # 선택된 voca_class에 해당하는 데이터를 가져오는 등의 작업을 수행할 수 있습니다.
        context = {"vocalist_class":vocalist_class, "selected_voca_list": selected_voca_list}
        return render(request, 'pybo/voca_read.html', context)


    context = {"vocaList" : vocaList, "vocalist_class":vocalist_class}
    return render(request, 'pybo/voca_read.html', context)


def vocaTest(request):
    # voca = Voca
    vocaList = selected_voca_list

    random.shuffle(vocaList)

    # 정답과 오답 자리를 섞기 위한 리스트 생성
    randomPosition = []
    for i in range(len(vocaList)):
        ranList = [0, 1, 2, 3]
        random.shuffle(ranList)
        randomPosition.append(ranList)

    # 정답과 함께 출력할 오답의 리스트 생성 - 0번 인덱스가 정답 1~3번 인덱스가 오답
    randAnswer = []
    for i in range(len(vocaList)):
        answers = []
        answers.append(i)
        for j in range(1, 4):
            while True:
                answer = random.randrange(len(vocaList))

                dupChk = True
                for k in range(0, j):
                    if answers[k] == answer:
                        dupChk = False
                        break

                if dupChk:
                    answers.append(answer)
                    break

        for j in range(4):
            answers[j] = set(item[2] for item in vocaList)

        randAnswer.append(answers)

    # vocaList = 단어장, randomPosition = 정답 위치, randAnswer = 선택지
    datas = {"vocaList": vocaList,
             "randomPosition": randomPosition,
             "randAnswer": randAnswer}

    return render(request, 'pybo/voca_test.html', datas)


@login_required(login_url='common:login')
def vocaTest2(request):
    user_id = request.user
    # vocaList_queryset = VocaList.select_where(user_id, "vv")  # Assuming VocaList.select returns a QuerySet
    # vocaList = list(vocaList_queryset)
    vocaList = selected_voca_list
    print(vocaList)

    random.shuffle(vocaList)

    # 정답과 오답 자리를 섞기 위한 리스트 생성
    randomPosition = []
    for i in range(len(vocaList)):
        ranList = [0, 1, 2, 3]
        random.shuffle(ranList)
        randomPosition.append(ranList)

    # 정답과 함께 출력할 오답의 리스트 생성 - 0번 인덱스가 정답 1~3번 인덱스가 오답
    randAnswer = []
    for i in range(len(vocaList)):
        answers = [i]
        # Assuming 'vv' is the second element in the tuple, change the index accordingly
        vv_value = vocaList[i][1] if len(vocaList[i]) > 1 else None
        vocaList_ids = list(vv_value) if vv_value else []

        # 랜덤하게 3개의 오답 선택
        # 확인할 필요 없이 random.sample을 호출할 수 있도록 길이를 체크
        if len(vocaList_ids) >= 3:
            other_answers = random.sample(vocaList_ids, 3)
        else:
            # 예외 처리 또는 적절한 대체 로직을 추가
            # 예를 들어, 모든 아이템을 선택하거나 다른 로직을 적용할 수 있음
            other_answers = vocaList_ids
            # 또는 raise ValueError("적절한 예외 처리")

        # 선택한 오답들을 answers에 추가
        for j in range(3):
            if j < len(other_answers):
                answers.append(other_answers[j])
            else:
                # j가 other_answers의 길이보다 크거나 같은 경우, 적절한 처리를 추가
                answers.append("Out of Range")

        # answers 리스트를 셔플
        random.shuffle(answers)

        # 각 오답의 실제 내용을 가져와서 randAnswer에 추가
        for j in range(4):
            if j < len(answers):
                if isinstance(answers[j], int):  # Out of Range가 숫자인 경우에만 데이터베이스 조회 시도
                    try:
                        answers[j] = VocaList.objects.get(id=answers[j]).voca_korea
                    except VocaList.DoesNotExist:
                        # 예외 처리: 해당 id에 대한 데이터가 없을 때
                        answers[j] = "Not Found"
            else:
                # j가 answers의 길이보다 크거나 같은 경우, 적절한 처리를 추가
                pass

        # 한 글자씩 나눠진 vv 값을 합쳐서 넣기
        # vocaList[i] = "".join(vocaList[i][1]) if len(vocaList[i]) > 1 else None

        randAnswer.append(answers)

    # vocaList = 단어장, randomPosition = 정답 위치, randAnswer = 선택지.
    datas = {"vocaList": vocaList,
             "randomPosition": randomPosition,
             "randAnswer": randAnswer}

    return render(request, 'pybo/voca_test.html', datas)


def shuffle(request):
    random.shuffle(selected_voca_list)
    context = {"selected_voca_list": selected_voca_list}
    return render(request, 'pybo/ocr_lists.html', context)