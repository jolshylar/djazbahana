from typing import Any, Dict, Optional

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .forms import (ClassroomForm, ConspectForm, CustomUserCreationForm,
                    UserForm)
from .models import Classroom, Conspect, Message, Topic, User


class HomeView(ListView):
    template_name: str = 'base/home.html'
    model = Classroom
    context_object_name: Optional[str] = 'classrooms'
    paginate_by: int = 3

    def get_queryset(self):
        q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
        user = User.objects.filter(username__icontains=q).first()
        return Classroom.objects.filter(
            Q(host=user) |
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q) 
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''

        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()[0:5]
        context['classroom_count'] = Classroom.objects.count()
        context['classroom_messages'] = Message.objects.filter(
            Q(classroom__topic__name__icontains=q)
        )[0:5]
        return context


def read_markdown(filename: str):
    with open(settings.BASE_DIR / f"static/markdown/{filename}.md", "r") as f:
        context = {'markdown_content': f.read()}
    return context


class AboutPageView(TemplateView):
    template_name: str = 'base/about.html'

    def get_context_data(self) -> Dict[str, Any]:
        return read_markdown('about')


class DonatePageView(TemplateView):
    template_name: str = 'base/donate.html'

    def get_context_data(self) -> Dict[str, Any]:
        return read_markdown('donate')


class RegisterPageView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        context = {'form': form}
        return render(request, 'base/login_register.html', context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # Login after registration
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')


class LoginPageView(View):
    def get(self, request):
        page = 'login'
        if request.user.is_authenticated:
            return redirect('home')

        return render(request, 'base/login_register.html', {'page': page})

    def post(self, request):
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


class LogoutRedirectView(RedirectView):
    pattern_name: Optional[str] = 'home'

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


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


class UserProfileDetailView(DetailView):
    model = User
    template_name: str = 'base/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        user = User.objects.filter(username__icontains=self.kwargs.get('username')).first()
        classrooms = user.classroom_set.all()

        paginator = Paginator(classrooms, 3)
        number = self.request.GET.get('page')
        page_obj = paginator.get_page(number)

        context = super().get_context_data(**kwargs)
        context['user'] = user
        context['page_obj'] = page_obj
        context['classroom_messages'] = user.message_set.all()
        context['topics'] = Topic.objects.all()
        return context


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
            return redirect('classroom', pk=classroom.id)
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
def confirm_payment(request, pk):
    user = request.user
    conspect = Conspect.objects.get(id=pk)

    def open_conspect(conspect):
        return FileResponse(open(f'{settings.BASE_DIR}/static/{conspect}', "rb"))

    if user == conspect.author:
        return open_conspect(conspect)

    if request.method == 'POST':
        user.balance -= 100
        conspect.author.balance += 100
        user.save()
        conspect.author.save()
        messages.info(request, 'Purchase has been successfully done.')
        return open_conspect(conspect)

    context = {'state': 'confirm', 'obj': conspect}
    return render(request, 'base/confirm.html', context)


@login_required(login_url='login')
def delete_classroom(request, pk):
    classroom = Classroom.objects.get(id=pk)

    if request.user != classroom.host:
        return FileResponse(open(settings.MEDIA_ROOT / 'errors/403.jpg', 'rb'))

    if request.method == 'POST':
        classroom.delete()
        return redirect('home')
    
    context = {'state': 'confirm', 'obj': classroom}
    return render(request, 'base/confirm.html', context)


@login_required(login_url='login')
def delete_conspect(request, pk):
    conspect = Conspect.objects.get(id=pk)

    if request.user != conspect.author:
        return FileResponse(open(settings.MEDIA_ROOT / 'errors/403.jpg', 'rb'))

    if request.method == 'POST':
        conspect.delete()
        return redirect('classroom', conspect.classroom.id)

    context = {'state': 'confirm', 'obj': conspect}
    return render(request, 'base/confirm.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.author:
        return FileResponse(open(settings.MEDIA_ROOT / 'errors/403.jpg', 'rb'))

    if request.method == 'POST':
        message.delete()
        return redirect('classroom', message.classroom.id)

    context = {'state': 'confirm', 'obj': message}
    return render(request, 'base/confirm.html', context)


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


class TopicsPageView(TemplateView):
    template_name: str = 'base/topics.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        q = self.request.GET.get('q') or ''
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.filter(name__icontains=q)
        return context


class ActivitiesPageView(TemplateView):
    template_name: str = 'base/activities.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['classroom_messages'] = Message.objects.all()
        return context
