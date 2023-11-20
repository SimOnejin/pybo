from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
import os
import random
from googletrans import Translator

from ..models import Question
from ..models import Article

from ..ocr import Nice
from ..forms import UserImageForm


def index(request):
    """
    pybo 목록 출력
    """
    try:
        request.session.modified = True  # 세션 삭제 가능하도록 등록
        del request.session['texts']  # 세션 삭제
    except:
        pass

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
    request.session['texts'] = []
    global texts, new_image_path
    question = get_object_or_404(Question, pk=question_id)
    # image_url = question.image.url
    image_path = os.path.join(settings.MEDIA_ROOT, question.image.name)
    if not os.path.isfile(image_path):
        # 파일이 존재하지 않을 때 처리할 로직
        pass
    else:
        # 파일이 존재하면 처리 계속하기
        request.session['texts'] = Nice(image_path)
        # texts = Nice(image_path)
        texts = request.session['texts']

    request.session['key'] = 'value'

    # 파일 경로와 확장자를 분리
    file_path, file_extension = os.path.splitext(question.image.name)
    # 문구 추가
    new_image_path = file_path + '_lined' + file_extension

    # texts = Nice(image_url)
    context = {'texts': texts, 'image':new_image_path}
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

def shuffle(request):
    # 리스트의 순서를 랜덤하게 섞음
    # random.shuffle(texts)
    random.shuffle(combined_list)
    shuffled_texts, shuffled_trans = zip(*combined_list)
    # 템플릿으로 데이터 전달
    # context = {'texts': shuffled_texts, 'trans': shuffled_trans}
    context = {'combined_list': combined_list}
    return render(request, 'pybo/ocr_lists.html', context)

def translate(request):
    # 예외 처리: texts가 없거나 비어있을 때 빈 리스트 반환
    texts = request.GET.getlist('texts', [])

    translator = Translator()
    global trans
    trans = []
    for i in texts:
        # request.session['result'] = translator.translate(i, dest='ko')
        # result = request.session['result']
        # result = translator.translate(i, dest='ko')
        # trans.append(result.text)
        translation_result = translator.translate(i, dest='ko')
        trans.append(translation_result.text)

    global combined_list
    combined_list = list(zip(texts, trans))
    context = {'combined_list': combined_list}
    # print(result.text)
    return render(request, 'pybo/trans.html', context)
