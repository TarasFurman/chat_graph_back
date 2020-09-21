from app.models import ChatRooms, UsersInChatRooms, Users
from app.serializers import UsersSerializer


class UserConnectionsLogic:

    def _users_conections(self, data, result=None):
        len_data = len(data)
        result_data = {}
        if result:
            result_data = result

        for index, key in enumerate(data):
            n = 0

            while n < len_data:
                res = [key]
                if index == n:
                    n += 1
                    continue

                res.append(data[n])
                res.sort()

                full_data = ''.join(str(x) for x in res)
                if full_data not in result_data.keys():
                    result_data[full_data] = {'source': res[0], 'target': res[1]}

                n += 1
        # '110': {'a': 1, 'b': 10}, '23': {'a': 2, 'b': 3},
        return result_data

    def _filter_res(self, data):
        filter_res = []
        for key, item in data.items():
            filter_res.append(item)

        return filter_res

    def user_connections(self):
        result = None
        chats = list(ChatRooms.objects.all().values_list("id", flat=True))

        for chat_id in chats:
            users_in_chat = list(
                UsersInChatRooms.objects.filter(
                    chat_room_id__id=chat_id
                ).values_list('user__id', flat=True)
            )
            result = self._users_conections(users_in_chat, result=result)

        if not result:
            return result

        filtered = self._filter_res(result)
        return filtered


class UserAppendRoomsLogic:

    def create_(self, data, rooms):
        try:
            user = Users.objects.get(id=data.get('id'))
        except Users.DoesNotExist:
            return None

        UsersInChatRooms.objects.get_or_create(user=user, chat_room_id=rooms)

        # return all users in chat room
        users = UsersInChatRooms.objects.filter(chat_room_id=rooms.id)

        return users


class UserNotInrRoomsLogic:

    def get_users(self, rooms):
        all_users = Users.objects.all().values_list("id", flat=True).difference(
            UsersInChatRooms.objects.filter(
                chat_room_id=rooms.id
            ).values_list('user__id', flat=True)
        )

        users = Users.objects.filter(id__in=list(all_users))
        users_serializer = UsersSerializer(users, many=True)

        return users_serializer.data


class ChatRoomsLogic:

    def create_(self, data, user):
        try:
            chat = ChatRooms.objects.get(name=data.get('name'))
        except ChatRooms.DoesNotExist:
            return None
        UsersInChatRooms.objects.get_or_create(
            user=user,
            chat_room_id=chat
        )
        return data
