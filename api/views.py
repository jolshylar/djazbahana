from rest_framework import permissions, viewsets

from base.models import Classroom, Topic, User

from .serializers import ClassroomSerializer, TopicSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class TopicViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to see all topics application has.
    """

    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = []


class ClassroomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to see all classrooms application has.
    """

    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]
