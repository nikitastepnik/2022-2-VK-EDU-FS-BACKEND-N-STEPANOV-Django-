from django.urls import path, re_path

from . import views

urlpatterns = [
    path('create/', views.post_create_chat),
    re_path('delete/(?P<pk>(\d)+)/$', views.delete_chat),
    re_path('get/(?P<pk>(\d)+)/$', views.get_chat),
    path('get_all_chats/', views.get_chats),
    re_path('get_for_user/(?P<user_pk>(\d)+)/$', views.get_user_chats),
    path('edit_topic/', views.edit_chat_topic),
]
