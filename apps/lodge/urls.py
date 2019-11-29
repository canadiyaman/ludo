from django.conf.urls import url

from apps.lodge.views import LodgeView, SpecialLodge

urlpatterns = (
    url(r'^$', LodgeView.as_view(), name='home'),
    url(r'lodge/(?P<group_name>[\w-]+)$', SpecialLodge.as_view(), name='special_lodge')
)
