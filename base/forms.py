from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models import User, Classroom, Conspect


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']


class ClassroomForm(ModelForm):
    class Meta:
        model = Classroom
        fields = '__all__'
        exclude = ['host', 'students']


class ConspectForm(ModelForm):
    class Meta:
        model = Conspect
        fields = ['file']
