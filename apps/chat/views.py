from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from apps.chat.models import Room
from apps.chat.forms import RoomForm


class ChatView(View):
    def get(self, request):
        return render(request, 'pages/chat.html', {})


class RoomView(View):
    model = Room

    def get(self, request, key=None):
        room = Room.objects.get(key=key)
        return render(request, 'pages/room.html', {"room": room})

    def post(self, request, key=None):
        response = dict()

        form = RoomForm(data=request.POST)
        if form.is_valid():
            room = form.save()
            response['success'] = True
            response['link'] = room.create_url()
            return HttpResponse(room.serialize())

        response['success'] = False
        response['errors'] = form.errors
        return HttpResponse()
