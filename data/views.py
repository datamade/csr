from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, HttpResponse
from data.models import Image, Task, EventLog, WorkTimer, Constants
from django.forms.models import inlineformset_factory, modelform_factory
from data.decorators import timeout_logging, check_access
from data.forms import MenuItemForm
from django.db import models
from django import forms
from django.conf import settings
import data.user_patch
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User

# Create your views here.

@login_required(login_url="/login/")
def index(request):
    return HttpResponseRedirect(reverse('data:images'))

@login_required(login_url="/login/")
@check_access
def list_images(request):
    try:
        referer = request.META["HTTP_REFERER"]
    except KeyError:
        referer = "DNE"
    if "/login/" in referer:
        clickmodal = "yes"
    else:
        clickmodal = None
    images = request.user.get_tasks()
    context = {
        'images': images,
        'clickmodal': clickmodal,
    }
    return render(request, "data/images.html", context)


def my_login(request, *args, **kwargs):
    kwargs = {'template_name': "login.html",}
    response = auth_views.LoginView(request)
    if response.status_code == 302:
        user = User.objects.get(username=request.POST['username'])
        event = EventLog(user_id=user.id, name="login", frame=user.treatment.get_frame())
        event.save()
    return response

def my_logout(request, *args, **kwargs):
    description = request.GET.get('message', '')
    if not request.user.is_authenticated():
        return render(request, 'login.html', {'message': "logged out due to inactivity"})
    event = EventLog(user_id=request.user.id, name="logout", description=description, frame=request.user.treatment.get_frame())
    event.save()
    return auth_views.logout(request, next_page="/", extra_context={'message': 'logged out due to inactivity'})

def field_widget_callback(field):
    return forms.TextInput(attrs={'placeholder': field.name})

@timeout_logging
def task_entry(request, image_id):
    if not request.user.treatment.get_access()['access']:
        redirect('unauthorized')
    fields = [
        'month','year', 'street_nam',  'city', 'state', 'pic_quality', 'str_quality', 'pot_holes',
        'bui_quality', 'car_quality', 'litter', 'road_work', 'graffiti',  'for_sale',
        'shoes', 'people', 'broken_signs', 'trees',
    ]
    inactive = 0
    task, created = Task.objects.get_or_create(image_id=image_id, user_id=request.user.id)
    TaskForm = modelform_factory(Task, exclude=['id', 'image', 'user', 'finished', 'timestarted', 'timefinished',])
    # Evaluate which form the post came from.  If from timer, then repopulate with request.DATA
    # else save it per usual
    if request.method == "POST":
        taskform = TaskForm(request.POST, request.FILES, instance=task)
        if request.POST['action'] == "save":
            for f in fields:
                val = request.POST[f]
                if val != '':
                    if f != 'street_nam' and f != 'city' and f != 'state':
                        val = int(val)
                    setattr(task,f, val)
            task.save()
            taskform = TaskForm(instance=task)
        if request.POST['action'] == "submit":
            if taskform.is_valid():
                task.finished = 1
                task.save()
                return HttpResponseRedirect(reverse('data:images'))

        if request.POST['action'] == "log":
            inactive = 1

    else:
        taskform = TaskForm(instance=task)


    context = {
        'inactive': inactive,
        'task': task,
        'taskform': taskform,
        'DEBUG': settings.DEBUG,
    }
    return render(request, "data/task_entry.html", context)

@login_required(login_url="/login/")
def log_event(request, image_id):
    task = Task.objects.get(image_id=image_id, user_id=request.user.id)
    url = "/taskentry/{}".format(task_id)
    event = EventLog(task_id=task.id, name="timeout")
    event.save()
    return redirect(url)

@csrf_protect
def home_timer(request):
    time = round(float(request.POST['time']))
    token = request.POST['token']
    worktimer, created = WorkTimer.objects.get_or_create(user_id=request.user.id, page="home", value=int(time), token=token,access=int(request.user.treatment.get_access()['access']))
    response = HttpResponse()
    return response


def unauthorized(request):
    context = {
        'user':request.user,
    }
    return render(request, "data/unauthorized.html", context)

