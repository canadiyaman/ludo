from django.conf.urls import url

from apps.chat.views import ChatView, RoomView, CreateRoomView

urlpatterns = (
    url(r'^$', ChatView.as_view(), name='home'),
    url(r'^rooms/(?P<key>[0-9A-Fa-f-]+)$', RoomView.as_view(), name='room'),
    url(r'^rooms/$', CreateRoomView.as_view(), name='create_room'),
)
