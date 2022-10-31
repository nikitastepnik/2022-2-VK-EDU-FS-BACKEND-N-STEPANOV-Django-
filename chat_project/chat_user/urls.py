from django.urls import re_path

from . import views

urlpatterns = [
    re_path('get_info/(?P<pk>(\d)+)/$', views.get_user_info),
]
