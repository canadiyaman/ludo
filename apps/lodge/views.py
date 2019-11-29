from django.contrib.auth.models import Group
from django.shortcuts import render
from django.views import View


class LodgeView(View):
    def get(self, request):
        groups = Group.objects.all()
        return render(request, 'pages/lodge_home.html', {"groups": groups})


class SpecialLodge(View):
    def get(self, request, group_name):
        group = Group.objects.get(name=group_name)
        return render(request, 'pages/special_lodge.html', {"group": group})
