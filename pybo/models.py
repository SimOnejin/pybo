from django.contrib.auth.models import User
from django.db import models


from django.db import connection
# Create your models here.
# from django.utils.crypto import get_random_string




class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')  # 추천인 추가
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)

    def __str__(self):
        return self.subject

class Voca(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='author_voca')
    subject = models.CharField(max_length=200)
    create_date = models.DateTimeField()
    image = models.ImageField(upload_to='user_voca/', null=True, blank=True)

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)


class UserImage(models.Model):
    image = models.ImageField(upload_to='user_images/')
class Post(models.Model):
    postname = models.CharField(max_length=50)
    # 게시글 Post에 이미지 추가
    mainphoto = models.ImageField(blank=True, null=True)
    contents = models.TextField()

    # postname이 Post object 대신 나오기
    def __str__(self):
        return self.postname

class ImageModel(models.Model):
        image = models.TextField()

#사용자로부터 이미지 받기 10/30
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





class VocaList:
    voca_idx = ""

    def __init__(self, user_id="", voca_japan="", voca_korea="", voca_class=""):
        self.user_id = user_id
        self.voca_japan = voca_japan
        self.voca_korea = voca_korea
        self.voca_class = voca_class

    def create(self):
        cursor = connection.cursor()
        query = (
                "CREATE TABLE " + self.user_id + "_voca ("
                + "voca_idx SERIAL NOT NULL PRIMARY KEY, "
                + "voca_japan VARCHAR(20) NOT NULL, "
                + "voca_korea VARCHAR(20), "
                + "voca_class VARCHAR(100)"
                + ")"
        )
        cursor.execute(query)

    def save(self):
        query = ("INSERT INTO `" + self.user_id + "_voca` "
                 + "(voca_japan, voca_korea, voca_class) values ("
                 + "'" + self.voca_japan + "', "
                 + "'" + self.voca_korea + "', "
                 + "'" + self.voca_class + "'"
                 + ")")
        cursor.execute(query)

    class objects:
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                data_list = []

                datas = func(self, *args, **kwargs)
                for i in datas:
                    d = dict()
                    d["voca_idx"] = i[0]
                    d["voca_japan"] = i[1]
                    d["voca_korea"] = i[2]
                    d["voca_class"] = i[3]
                    data_list.append(d)

                return data_list
            return wrapper

        @decorator
        def raw(query):
            cursor.execute(query)
            return cursor.fetchall()









class Friends:
    friends_idx = ""

    def __init__(self, user_id="", friends_code="", friends_id="", friends_status="", friends_create_date=""):
        self.user_id = user_id
        self.friends_code = friends_code
        self.friends_id = friends_id
        self.friends_status = friends_status
        self.friends_create_date = friends_create_date

    def create(self):
        query = ("CREATE TABLE " + self.user_id + "_friends` ("
                 + "`friends_idx` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, "
                 + "`friends_code` varchar(10) NOT NULL UNIQUE, "
                 + "`friends_id` varchar(50) NOT NULL UNIQUE, "
                 + "`friends_status` varchar(10), "
                 + "`friends_create_date` datetime(6) NOT NULL"
                 + ")")
        cursor.execute(query)

    def save(self):
        query = ("INSERT INTO `" + self.user_id + "_voca` "
                 + "(friends_code, friends_id, friends_status, friends_create_date) values ("
                 + "'" + self.friends_code + "', "
                 + "'" + self.friends_id + "', "
                 + "'" + self.friends_status + "', "
                 + "'" + self.friends_create_date + "'"
                 + ")")
        cursor.execute(query)

    class objects:
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                data_list = []

                datas = func(self, *args, **kwargs)
                for i in datas:
                    d = dict()
                    d["friends_idx"] = i[0]
                    d["friends_code"] = i[1]
                    d["friends_id"] = i[2]
                    d["friends_status"] = i[3]
                    d["friends_create_date"] = i[4]
                    data_list.append(d)

                return data_list
            return wrapper

        @decorator
        def raw(query):
            cursor.execute(query)
            return cursor.fetchall()

    def drop(self):
        query = ("DROP TABLE `" + self.user_id + "_friends`")
        cursor.execute(query)

