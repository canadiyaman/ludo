from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.conf.urls import url

from apps.chat.consumers import ChatConsumer
from apps.lodge.consumers import LodgeConsumer, Lodge2Consumer
websocket_urlpatterns = [
    url(r'^ws/chat/(?P<key>[0-9A-Fa-f-]+)$', ChatConsumer),
    url(r'^ws/lodge/(?P<group_name>[\w-]+)$', LodgeConsumer),
    url(r'^ws/lodge2/(?P<group_name>[\w-]+)$', Lodge2Consumer),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
