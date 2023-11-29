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




