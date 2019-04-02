"""ludo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from apps.chat.views import ChatView, RoomView
from views import CreateRoomView

urlpatterns = [
    url(r'^$', ChatView.as_view(), name='chat'),
    url(r'^rooms/(?P<key>[0-9A-Fa-f-]+)$', RoomView.as_view(), name='room'),
    url(r'^rooms/', CreateRoomView.as_view(), name='create_room'),
    path('admin/', admin.site.urls),
]
