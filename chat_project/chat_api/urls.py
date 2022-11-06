from django.urls import path, re_path

from . import views
from .views import ChatViewSet


urlpatterns = [
    path('add_member/', ChatViewSet.as_view({'put': 'partial_update_add_user_to_chat'})),
    path('create/', views.create_chat),
    re_path('delete/(?P<pk>(\d)+)/', views.delete_chat),
    path('delete_member/', views.delete_member_from_chat),
    re_path('get/(?P<pk>(\d)+)/', views.get_chat),
    path('get_all_chats/', views.get_chats),
    re_path('get_users/(?P<user_pk>(\d)+)/', views.get_user_chats),
    path('edit/', views.edit_chat_information),
]
