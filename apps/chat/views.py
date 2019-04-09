from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, TemplateView

from apps.chat.models import Room
from apps.chat.forms import RoomForm


class ChatView(View):
    def get(self, request):
        rooms = Room.objects.all()
        return render(request, 'pages/chat.html', {"rooms": rooms})


class RoomView(TemplateView):
    queryset = Room.objects.all()
    template_name = 'pages/room.html'
    lookup_field = 'key'

    def get(self, request, key=None, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['room'] = self.queryset.get(key=key)
        return self.render_to_response(context)


class CreateRoomView(CreateView):

    def post(self, request, *args, **kwargs):
        response = dict()
        data = request.POST.copy()
        data['created_by'] = request.user.id
        form = RoomForm(data=data)
        if form.is_valid():
            room = form.save()
            response['success'] = True
            response['room_url'] = room.get_absolute_url()
            return JsonResponse(response)

        response['success'] = False
        response['errors'] = form.errors
        return JsonResponse(response)
