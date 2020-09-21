from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import ChatRooms, UsersInChatRooms, Messages, Users


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username']


class ChatRoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRooms
        fields = '__all__'


class UsersInChatRoomsSerializer(serializers.ModelSerializer):
    chat_room_id = ChatRoomsSerializer()

    class Meta:
        model = UsersInChatRooms
        fields = ['chat_room_id']


class InChatRoomsSerializer(serializers.ModelSerializer):
    user = UsersSerializer()

    class Meta:
        model = UsersInChatRooms
        fields = ['user']


class MessagesSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)

    class Meta:
        model = Messages
        fields = ['id', 'message', 'date_create', 'user', 'chat_room_id']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serialize Token
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = {'user_id': self.user.id, 'user_name': self.user.username}

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token
