from django.contrib import admin
from app.models import Users, ChatRooms, UsersInChatRooms, Messages


admin.site.register(Users)
admin.site.register(ChatRooms)
admin.site.register(UsersInChatRooms)
admin.site.register(Messages)
