from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=16, null=True)
    email = models.EmailField(unique=True, null=True, validators=[validate_email])
    bio = models.TextField(max_length=128, null=True)
    avatar = models.ImageField(null=True, default="avatar.svg", upload_to="avatars/")
    balance = models.PositiveSmallIntegerField(default=300)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class Topic(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128, null=True, blank=True)
    students = models.ManyToManyField(User, related_name="students", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.name


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return f"{self.body[0:32]} ..."


class Conspect(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    description = models.CharField(max_length=128, null=True)
    file = models.FileField(upload_to="uploads/")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        if self.description:
            file_extension = self.file.name.split(".")[-1]
            return f"[.{file_extension}] {self.description}"
        return f"images/{self.file.name}"
