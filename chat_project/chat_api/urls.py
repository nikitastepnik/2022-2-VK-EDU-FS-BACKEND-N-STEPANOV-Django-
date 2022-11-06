from django.urls import path, re_path

from . import views

urlpatterns = [
    path('add_member/', views.add_user_to_chat),
    path('create/', views.create_chat),
    re_path('delete/(?P<pk>(\d)+)/', views.delete_chat),
    path('delete_member/', views.delete_member_from_chat),
    re_path('get/(?P<pk>(\d)+)/', views.get_chat),
    path('get_all_chats/', views.get_chats),
    re_path('get_users/(?P<user_pk>(\d)+)/', views.get_user_chats),
    re_path('edit/(?P<pk>(\d)+)/', views.edit_chat_information),
]
