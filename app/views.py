from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from app.serializers import MyTokenObtainPairSerializer
from .models import Users, ChatRooms, UsersInChatRooms, Messages
from .serializers import (
    UsersSerializer,
    ChatRoomsSerializer,
    UsersInChatRoomsSerializer,
    InChatRoomsSerializer,
    MessagesSerializer
)

from .usecases import (
    UserConnectionsLogic,
    UserAppendRoomsLogic,
    UserNotInrRoomsLogic,
    ChatRoomsLogic
)


class LoginViewSet(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin):

    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def chat_rooms(self, request, **kwargs):
        user = self.get_object()
        chat_rooms = UsersInChatRooms.objects.filter(
            user_id=user.id
        )
        chat_rooms_serializer = UsersInChatRoomsSerializer(
            chat_rooms, many=True
        )

        return Response(chat_rooms_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def users_connections(self, request, **kwargs):
        result_data = UserConnectionsLogic().user_connections()

        if not result_data:
            return Response(
                [],
                status=status.HTTP_200_OK
            )
        return Response(result_data, status=status.HTTP_200_OK)


class ChatRoomsViewSet(GenericViewSet, RetrieveModelMixin,
                       ListModelMixin, CreateModelMixin):
    queryset = ChatRooms.objects.all()
    serializer_class = ChatRoomsSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def users_rooms(self, request, **kwargs):
        rooms = self.get_object()
        users = UsersInChatRooms.objects.filter(chat_room_id=rooms.id)
        users_serializer = InChatRoomsSerializer(users, many=True)

        return Response(users_serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = ChatRoomsLogic().create_(
            data=serializer.data, user=self.request.user
        )
        if not data:
            return Response(
                {'detail': 'room not in database'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def append_user_room(self, request, **kwargs):
        rooms = self.get_object()
        data = request.data

        result_data = UserAppendRoomsLogic().create_(
            data=data, rooms=rooms
        )
        if not result_data:
            return Response(
                {'detail': 'user not in database'},
                status=status.HTTP_400_BAD_REQUEST
            )

        users_serializer = InChatRoomsSerializer(result_data, many=True)
        return Response(users_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def users_not_in_room(self, request, **kwargs):
        rooms = self.get_object()
        data = UserNotInrRoomsLogic().get_users(rooms=rooms)

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def get_messages(self, request, **kwargs):
        room = self.get_object()
        messages = Messages.objects.filter(chat_room_id=room)
        data = MessagesSerializer(messages, many=True)

        return Response(data.data, status=status.HTTP_200_OK)


class MessagesViewSet(GenericViewSet, CreateModelMixin):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=self.request.user)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
