from django.urls import path, re_path

from . import views
from .views import MessageViewSet

urlpatterns = [
    path('create/', MessageViewSet.as_view({'post': 'create'})),
    path('delete/', MessageViewSet.as_view({'delete': 'destroy'})),
    path('edit/', MessageViewSet.as_view({'put': 'partial_update'}),
    re_path('get/(?P<pk>(\d)+)/$', views.get_message),
    path('get_list_for_user_chat/', views.get_messages_filter_user_chat),
    path('get_list_for_chat/', views.get_messages_filter_chat),
    re_path('mark_as_viewed/(?P<pk>(\d)+)/$', views.mark_message_as_viewed),
]
