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

from ..models import Question
from ..models import Article

from ..ocr import Nice
from ..forms import UserImageForm


def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    sort_by = request.GET.get('sort_by', 'recent')  # 정렬기준

    # 정렬
    if sort_by == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif sort_by == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'sort_by': sort_by}  # <------ so 추가
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def voca_list(request):
    voca_list = Voca.objects.order_by('-create_date')
    context = {'voca_list': voca_list}
    return render(request, 'pybo/voca_list.html', context)
def voca_detail(request, voca_id):
    """
    pybo 내용 출력
    """
    voca = get_object_or_404(Voca, pk=voca_id)
    context = {'voca': voca}
    return render(request, 'pybo/voca_detail.html', context)

# def ocr_page(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     image_url = question.image.url
#     texts = Nice(image_url)
#     context = {'texts': texts, 'question': question}
#     return render(request, 'pybo/ocr.html', context)
    # return redirect('pybo:detail', question_id=question.id)

# def ocr_page(request):
#     texts = Nice("../mysite/pybo/테스트4.png")
#     context = {'texts': texts}
#     return render(request, 'pybo/ocr.html', context)

def ocrTest(request, question_id):
    # request.session['texts'] = []
    global texts, new_image_path
    texts = []
    question = get_object_or_404(Question, pk=question_id)
    # image_url = question.image.url
    image_path = os.path.join(settings.MEDIA_ROOT, question.image.name)
    if not os.path.isfile(image_path):
        # 파일이 존재하지 않을 때 처리할 로직
        pass
    else:
        # 파일이 존재하면 처리 계속하기
        # request.session['texts'] = Nice(image_path)
        texts = Nice(image_path)
        # texts = request.session['texts']
        # texts = request.session.get('texts', None)

    request.session['key'] = 'value'

    # 파일 경로와 확장자를 분리
    file_path, file_extension = os.path.splitext(question.image.name)
    # 문구 추가
    new_image_path = file_path + '_lined' + file_extension

    translator = Translator()
    trans = []
    for i in texts:
        # request.session['result'] = translator.translate(i, dest='ko')
        # result = request.session['result']
        # result = request.session.get('result', None)

        result = translator.translate(i, dest='ko')
        trans.append(result.text)

    global combined_list

    combined_list = list(zip(texts, trans))

    # texts = Nice(image_url)
    context = {'texts':texts, 'combined_list': combined_list, 'image':new_image_path}
    return render(request, 'pybo/ocr.html', context)


def ocrTest1(request, voca_id):
    # request.session['texts'] = []
    global texts, new_image_path
    texts = []
    voca = get_object_or_404(Voca, pk=voca_id)
    # image_url = question.image.url
    image_path = os.path.join(settings.MEDIA_ROOT, voca.image.name)
    if not os.path.isfile(image_path):
        # 파일이 존재하지 않을 때 처리할 로직
        pass
    else:
        # 파일이 존재하면 처리 계속하기
        # request.session['texts'] = Nice(image_path)
        texts = Nice(image_path)
        # texts = request.session['texts']
        # texts = request.session.get('texts', None)

    request.session['key'] = 'value'

    # 파일 경로와 확장자를 분리
    file_path, file_extension = os.path.splitext(voca.image.name)
    # 문구 추가
    new_image_path = file_path + '_lined' + file_extension

    translator = Translator()
    trans = []
    for i in texts:
        # request.session['result'] = translator.translate(i, dest='ko')
        # result = request.session['result']
        # result = request.session.get('result', None)

        result = translator.translate(i, dest='ko')
        trans.append(result.text)

    global combined_list

    combined_list = list(zip(texts, trans))

    # texts = Nice(image_url)
    context = {'texts':texts, 'combined_list': combined_list, 'image':new_image_path}
    return render(request, 'pybo/ocr.html', context)

def create(request):
    if request.method == 'POST':
        form = Article(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()

def upload_image(request):
    if request.method == 'POST':
        form = UserImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # 여기에서 성공 메시지를 추가하거나 다른 처리를 할 수 있습니다.
    else:
        form = UserImageForm()
    return render(request, 'pybo/ocr.html', {'form': form})

@login_required(login_url='common:login')
def shuffle(request):

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
        vocaList = VocaList(
            user_id=user_id,
            voca_japan=pair["text"],
            voca_korea=pair["translate"],
            voca_class=content
        )
        vocaList.save()

    random.shuffle(matched_pairs)

    # matchedPairs를 템플릿에 전달
    context = {'combined_list': matched_pairs, "content": content}

    # 템플릿 렌더링
    return render(request, 'pybo/ocr_lists.html', context)
def shuffle1(request):
    # 리스트의 순서를 랜덤하게 섞음
    # random.shuffle(texts)
    request.session.clear()
    texts = []
    random.shuffle(combined_list)
    shuffled_texts, shuffled_trans = zip(*combined_list)
    # 템플릿으로 데이터 전달
    # context = {'texts': shuffled_texts, 'trans': shuffled_trans}
    context = {'combined_list': combined_list, 'texts': texts}
    return render(request, 'pybo/ocr_lists.html', context)

def translate(request):
    # del request.session['combined_list']
    translator = Translator()
    global trans
    trans = []
    for i in texts:
        # request.session['result'] = translator.translate(i, dest='ko')
        # result = request.session['result']
        # result = request.session.get('result', None)

        result = translator.translate(i, dest='ko')
        trans.append(result.text)

    global combined_list

    combined_list = list(zip(texts, trans))
    context = {'combined_list': combined_list}
    # print(result.text)
    return render(request, 'pybo/trans.html', context)

def session_reset(request):
    request.session.clear()
    return render(request, 'pybo/question_list.html')


@login_required(login_url='common:login')
def voca_create(request):
    if request.method == 'POST':
        form = VocaForm(request.POST)
        if form.is_valid():
            voca = form.save(commit=False)
            voca.author = request.user  # author 속성에 로그인 계정 저장jj.
            voca.create_date = timezone.now()
            voca.image = request.FILES.get('image',None) #request의 FILES의 image 속성 가져온다
            voca.save()
            return redirect('pybo:voca_list')
    else:
        form = VocaForm()
    context = {'form': form}
    return render(request, 'pybo/voca_scan.html', context)



@login_required(login_url='common:login')
def vocaTest(request):
    # voca = Voca
    # vocaList = voca.objects.raw("select * from " + request.user + "_voca")
    vocaList = [{'voca_japan' : 'あ', 'voca_korea' : '아'},
                {'voca_japan' : 'い', 'voca_korea' : '이'},
                {'voca_japan' : 'う', 'voca_korea' : '우'},
                {'voca_japan' : 'え', 'voca_korea' : '에'},
                {'voca_japan' : 'お', 'voca_korea' : '오'}]
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

def  inputId(request):
    return render(request, 'pybo/voca_test_id.html')