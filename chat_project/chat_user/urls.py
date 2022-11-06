from django.urls import re_path

from . import views
from .views import UserViewSet

urlpatterns = [
    re_path('get_info/(?P<pk>(\d)+)/$', UserViewSet.as_view({'get': 'retrieve'})
),
]
