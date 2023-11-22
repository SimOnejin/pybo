from django import forms
from pybo.models import Question, Answer, Comment, UserImage, Voca


class VocaForm(forms.ModelForm):
    class Meta:
        model = Voca  # 사용할 모델
        fields = ['subject', 'image']  # QuestionForm에서 사용할 Question 모델의 속성
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows':10}),
        # }
        labels = {
            'subject': '제목',
            'image': '사진',
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # 사용할 모델
        fields = ['subject', 'content', 'image']  # QuestionForm에서 사용할 Question 모델의 속성
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows':10}),
        # }
        labels = {
            'subject': '제목',
            'content': '내용',
            'image': '사진',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }


class UserImageForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ['image']