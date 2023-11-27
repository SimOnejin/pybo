# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm
from pybo.models import VocaList
from django.http import HttpResponse

from django.db import connection


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인

            print(request.POST.get("username"))
            print("test")

            vocaList = VocaList(user_id=request.POST.get("username"))
            vocaList.create()

            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})


def test(requst):
    # vocaTest = VocaList(user_id="test")
    cursor = connection.cursor()

    query = ("CREATE TABLE test_voca ("
             + "`voca_idx` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, "
             + "`voca_japan` varchar(20) NOT NULL, "
             + "`voca_korea` varchar(20), "
             + "`voca_class` varchar(100)"
             + ")")
    cursor.execute(query)

    # query = ("select * from pybo_voca")
    # cursor.execute(query)

    # vocaTest.create()
    return HttpResponse("test")