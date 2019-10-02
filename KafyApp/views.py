from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import QuestionForm, SubmitForm
import socket
import json
from .models import UserInfo, Question, Submit


# Create your views here.
def SignUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def submit_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        submit_form = SubmitForm(request.POST)
        if request.POST.get('type') == 'question' and question_form.is_valid():
            cd = question_form.cleaned_data
            q_history = []
            for question in UserInfo.get(request.user).questions.all():
                q_history.extend([question.a, question.b, question.c, question.answer])
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', 8000))
            sock.send(json.dumps({
                'username': request.user.username,
                'type': 'question',
                'q_history': q_history,
                'question': [cd['a'], cd['b'], cd['c']]
            }).encode('utf-8'))
            response_data = sock.recv(1024)
            sock.close()
            response_data = response_data.split()
            Question.objects.create(user_info=UserInfo.get(request.user), a=question_form.a, b=question_form.b, c=question_form.c, answer=response_data[0], remained=response_data[1])
        if request.POST.get('type') == 'submit' and submit_form.is_valid():
            cd = submit_form.cleaned_data
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', 8000))
            sock.send(json.dumps({
                'username': request.user.username,
                'type': 'submit',
                'permu': list(map(lambda x: int(x.strip()), cd['value'].split(',')))
            }).encode('utf-8'))
            response_data = sock.recv(1024)
            sock.close()
            response_data = response_data.split()
            Question.objects.create(user_info=UserInfo.get(request.user), a=question_form.a, b=question_form.b, c=question_form.c, answer=response_data[0], remained=response_data[1])
    else:
        question_form = QuestionForm()
        submit_form = SubmitForm()
    return render(request, 'question.html', {'question_form': question_form,
                                            'submit_form':submit_form})
