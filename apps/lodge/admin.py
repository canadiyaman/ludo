from django.contrib import admin

from apps.lodge.models import Content


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    class Media:
        js = ("js/main.js",)
