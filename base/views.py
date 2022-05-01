from django.http import HttpResponse, FileResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings

from .forms import ConspectForm, CustomUserCreationForm, UserForm, ClassroomForm
from .models import Classroom, Conspect, User, Message, Topic


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    classrooms = Classroom.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    classroom_count = classrooms.count()
    classroom_messages = Message.objects.filter(Q(classroom__topic__name__icontains=q))[0:5]

    context = {
        'classrooms': classrooms,
        'topics': topics,
        'classroom_count': classroom_count,
        'classroom_messages': classroom_messages,
    }
    return render(request, 'base/home.html', context)


def read_markdown(filename):
    with open(settings.BASE_DIR / f"static/markdown/{filename}.md", "r") as f:
        context = {'markdown_content': f.read()}
    return context


def about_page(request):
    context = read_markdown('about')
    return render(request, 'base/about.html', context)


def donate_page(request):
    context = read_markdown('donate')
    return render(request, 'base/donate.html', context)


def register_page(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # Login right after registration
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    
    context = {'form': form}
    return render(request, 'base/login_register.html', context)



def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email or password entered wrong')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def classroom(request, pk):
    author = request.user
    classroom = Classroom.objects.get(id=pk)
    classroom_messages = classroom.message_set.all()
    classroom_conspects = classroom.conspect_set.all()
    students = classroom.students.all()

    if request.method == 'POST':
        Message.objects.create(
            author=author,
            classroom=classroom,
            body=request.POST.get('body'),
        )
        classroom.students.add(author)
        return redirect('classroom', pk=classroom.id)

    context = {
        'classroom': classroom,
        'classroom_messages': classroom_messages,
        'classroom_conspects': classroom_conspects,
        'students': students,
    }
    return render(request, 'base/classroom.html', context)


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    classrooms = user.classroom_set.all()
    classroom_messages = user.message_set.all()[0:2]
    topics = Topic.objects.all()
    context = {
        'user': user,
        'classrooms': classrooms,
        'classroom_messages': classroom_messages,
        'topics': topics,
    }
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def create_classroom(request):
    form = ClassroomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Classroom.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    
    context = {'form': form, 'topics': topics}
    return render(request, 'base/classroom_form.html', context)


@login_required(login_url='login')
def create_conspect(request, pk):
    if request.method == 'POST':
        form = ConspectForm(request.POST, request.FILES)
        if form.is_valid():
            classroom = Classroom.objects.get(id=pk)
            instance = Conspect(
                author=request.user,
                classroom=classroom,
                file=request.FILES['file'],
            )
            instance.save()
            return redirect('classroom', classroom.id)
    else:
        form = ConspectForm()
    context = {'form': form}
    return render(request, 'base/conspect_form.html', context)


@login_required(login_url='login')
def update_classroom(request, pk):
    classroom = Classroom.objects.get(id=pk)
    form = ClassroomForm(instance=classroom)
    topics = Topic.objects.all()

    if request.user != classroom.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        classroom.name = request.POST.get('name')
        classroom.topic = topic
        classroom.description = request.POST.get('description')
        classroom.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'classroom': classroom}
    return render(request, 'base/classroom_form.html', context)


@login_required(login_url='login')
def delete_classroom(request, pk):
    classroom = Classroom.objects.get(id=pk)

    if request.user != classroom.host:
        return FileResponse(open(settings.MEDIA_ROOT / 'errors/403.jpg', 'rb'))

    if request.method == 'POST':
        classroom.delete()
        return redirect('home')
    
    context = {'obj': classroom}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def delete_conspect(request, pk):
    conspect = Conspect.objects.get(id=pk)

    if request.user != conspect.author:
        return FileResponse(open(settings.MEDIA_ROOT / 'errors/403.jpg', 'rb'))

    if request.method == 'POST':
        conspect.delete()
        return redirect('classroom', conspect.classroom.id)

    context = {'obj': conspect}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.author:
        return FileResponse(open(settings.MEDIA_ROOT / 'errors/403.jpg', 'rb'))

    if request.method == 'POST':
        message.delete()
        # TODO: think whether to redirect to a parent message or home
        return redirect('home')

    context = {'obj': message}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/update_user.html', context)


def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)


def activity_page(request):
    classroom_messages = Message.objects.all()
    context = {'classroom_messages': classroom_messages}
    return render(request, 'base/activity.html', context)
