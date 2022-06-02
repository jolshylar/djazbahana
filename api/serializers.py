from rest_framework import serializers

from base.models import Classroom, Topic, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "bio", "avatar"]


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topic
        fields = ["name"]


class ClassroomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Classroom
        fields = ["name", "description", "created", "updated"]
