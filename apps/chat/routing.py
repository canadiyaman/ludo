from django.conf.urls import url

from apps.chat import consumers

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<key>[0-9A-Fa-f-]+)$', consumers.ChatConsumer),
]
