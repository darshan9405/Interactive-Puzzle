from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm
from .models import submissions, CustomUser, question, session
import datetime
from django.utils import timezone


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("interactivepuzzle:index")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("interactivepuzzle:index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    return login_request(request)


def logout_request(request):
    if request.user.is_authenticated:
        logout(request)
    return login_request(request)


def instructions(request):
    if request.user.is_authenticated:
        return render(request, 'instructions.html')
    return login_request(request)


def fetchquestion(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(username=request.user)
        subs = submissions.objects.filter(
            user=request.user).filter(status=True)
        currQuestion = len(subs) + 1
        que = question.objects.filter(id=currQuestion)
        createSession = False
        for q in que:
            que = q
            createSession = True
            break
        user_session = session.objects.filter(user=request.user)
        if len(user_session) != 0:
            user_session = user_session.filter(question=que)
            found = False
            for u in user_session:
                user_session = u
                found = True
                break
            if not found:
                user_session = session()
                user_session.user = user
                user_session.question = que
                user_session.startTime = timezone.now()

                user_session.save()
            arr = q.clues.split('>')
            que.clues = arr
            return render(request, 'question.html', context={'question': que, 'session': user_session})
        if len(user_session) == 0 and createSession:
            # create a new session for the question
            user_session = session()
            user_session.question = que
            user_session.user = user
            user_session.startTime = timezone.now()
            user_session.save()

        arr = q.clues.split('>')
        que.clues = arr
        return render(request, 'question.html', context={'question': que, 'session': user_session})
    return login_request(request)


def submission_request(request, id):
    if request.GET:
        return fetchquestion(request)
    if request.user.is_authenticated:
        currQuestion = submissions.objects.filter(
            user=request.user).filter(status=True)
        currQuestionId = len(currQuestion) + 1
        if id != currQuestionId:
            return fetchquestion(request)
        else:
            data = request.POST.dict()
            answer = data.get("answer")
            user = CustomUser.objects.get(username=request.user)
            quesdata = question.objects.get(id=id)
            if quesdata.answer == answer:
                prevSession = session.objects.filter(
                    user=request.user).filter(question=quesdata)
                currSubmission = submissions()
                currSubmission.question = quesdata
                currSubmission.user = user
                currSubmission.status = True
                for s in prevSession:
                    currSubmission.timeStart = s.startTime
                    break
                currSubmission.timeEnd = timezone.now()
                currSubmission.score = 100
                currSubmission.save()
                for s in prevSession:
                    prevSession = s
                prevSession.endTime = timezone.now()
                prevSession.save()
                return fetchquestion(request)
            else:
                currSubmission = submissions()
                currSubmission.question = quesdata
                currSubmission.user = user
                currSubmission.status = False
                currSubmission.timeStart = timezone.now()
                currSubmission.timeEnd = timezone.now()
                currSubmission.score = 0
                currSubmission.save()
                return fetchquestion(request)
    return login_request(request)


def fetch_leaderboard(request):
    subs = submissions.objects.filter(status=True)
    users = CustomUser.objects.all()
    userData = {}
    for user in users:
        userData[user.username] = {'score': 0, 'time': 0}
    for sub in subs:
        userData[sub.user.username]['score'] = userData[sub.user.username]['score'] + sub.score
        timeTaken = sub.timeEnd - sub.timeStart
        userData[sub.user.username]['time'] = int(
            userData[sub.user.username]['time'] + (timeTaken.seconds)/60)
    sorted_data = sorted(
        userData.items(), key=lambda x: (-1*x[1]['score'], x[1]['time']))
    final_data = []
    for data in sorted_data:
        final_data.append([data[0], data[1]['score'], data[1]['time']])
    context = {'data': final_data}
    return render(request, 'leaderboard.html', context=context)


