from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from ..models import Question
from ..models import Article

from ..ocr import Nice

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

def ocr_page(request):
    texts = Nice("/Users/sim-onejin/Coding/python/projects/mysite/pybo/테스트4.png")
    context = {'texts': texts}
    return render(request, 'pybo/ocr.html', context)

def create(request):
    if request.method == 'POST':
        form = Article(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()