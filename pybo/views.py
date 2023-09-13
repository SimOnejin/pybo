from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question
from django.utils import timezone


# Create your views here.
def index(request):
    """

    pybo List Print
    """
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    """

    pybo List Print
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    """

    pybo Answer post
    """
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'),
                               create_date=timezone.now())
    return redirect('pybo:detail', question_id=question.id)







#
# def ocr_page(request):
#
#
#     # 인증 설정 (서비스 계정 키 JSON 파일 경로)
#     os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './graphic-jet-394909-3ac279e985b3.json'
#
#     # Vision API 클라이언트 초기화
#     client = vision_v1.ImageAnnotatorClient()
#
#     # 이미지 파일 경로
#     # image_path = './image/테스트단어.png' #250/20 10,30,400,150
#     # image_path = './image/테스트단어2.png'
#     image_path = './image/테스트4.png'
#
#     # 이미지 열기
#     with open(image_path, 'rb') as image_file:
#         content = image_file.read()
#
#     # 이미지 데이터로 Image 객체 생성
#     image = types.Image(content=content)
#
#     # 일본어만 추출
#     def extract_japanese(texts):
#         japanese_texts = []
#
#         # 일본어 문자를 포함하는 문자열을 찾기 위한 정규 표현식
#         pattern = re.compile(r'[\u3040-\u30FF\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]')
#
#         for text in texts:
#             if pattern.search(text.description):
#                 japanese_texts.append(text)
#
#         return japanese_texts
#
#     def remove_korean(texts):
#         non_korean_texts = []
#
#         # 한글 문자를 찾기 위한 정규 표현식
#         pattern = re.compile(r'[\uAC00-\uD7A3]')
#
#         for text in texts:
#             if not pattern.search(text.description):
#                 non_korean_texts.append(text)
#
#         return non_korean_texts
#
#     # 이미지에서 텍스트 추출
#     # image_context = vision_v1.ImageContext(language_hints=["ja"])
#     response = client.text_detection(image=image)
#     # texts = remove_korean(response.text_annotations)
#     texts = response.text_annotations
#
#     def get_center(vertex1, vertex2):
#         """두 꼭지점 간의 중심 좌표를 반환합니다."""
#         x_center = (vertex1.x + vertex2.x) // 2
#         y_center = (vertex1.y + vertex2.y) // 2
#         return x_center, y_center
#
#     def calculate_distance(point1, point2):
#         """두 점 간의 거리를 계산합니다."""
#         return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
#
#     def group_boxes(annotations, threshold_x=250, threshold_y=20):  # threshold_x 값(간격)을 조절해서 한단어로 묶기
#         """임계값 이내의 경계 상자들을 그룹화합니다."""
#         centers = [get_center(text.bounding_poly.vertices[0], text.bounding_poly.vertices[2]) for text in annotations]
#         groups = []
#         visited = set()
#
#         for i, center1 in enumerate(centers):
#             if i in visited:
#                 continue
#
#             group = [i]
#             for j, center2 in enumerate(centers):
#                 dx = abs(center1[0] - center2[0])  # x 좌표의 차이
#                 dy = abs(center1[1] - center2[1])  # y 좌표의 차이
#
#                 if i != j and j not in visited and dx < threshold_x and dy < threshold_y:
#                     group.append(j)
#                     visited.add(j)
#
#             groups.append(group)
#             visited.add(i)
#
#         return groups
#
#     context = []
#     def draw_grouped_boxes(image_path, annotations, groups, min_width=10, min_height=30, max_width=400, max_height=150):
#         """그룹화된 경계 상자들을 그립니다."""
#         im = Image.open(image_path)
#         draw = ImageDraw.Draw(im)
#
#         for group in groups:
#             min_x = min([annotations[i].bounding_poly.vertices[0].x for i in group])
#             min_y = min([annotations[i].bounding_poly.vertices[0].y for i in group])
#             max_x = max([annotations[i].bounding_poly.vertices[2].x for i in group])
#             max_y = max([annotations[i].bounding_poly.vertices[2].y for i in group])
#
#             width = max_x - min_x
#             height = max_y - min_y
#
#             if width >= min_width and height >= min_height and width <= max_width and height <= max_height:
#                 draw.rectangle([min_x, min_y, max_x, max_y], outline='red')
#
#                 # 해당 경계 상자 내의 텍스트를 추출하고 출력
#                 group_texts = [annotations[i].description for i in group]
#                 group_texts = ''.join(group_texts)
#                 print(group_texts)
#                 # print(extract_japanese(group_texts))
#                 global context
#                 context = {
#                     "group_texts": group_texts
#                 }
#         im.show()
#
#     groups = group_boxes(texts)
#     draw_grouped_boxes(image_path, texts, groups)
#     # request에 대해 main.html로 context데이터를 넘겨준다.
#     return render(request, 'pybo/ocr.html', context)