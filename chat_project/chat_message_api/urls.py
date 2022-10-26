from django.urls import path, re_path

from . import views

urlpatterns = [
    path('create/', views.post_create_message),
    re_path('delete/(?P<pk>(\d)+)/$', views.delete_message),
    path('edit_content/', views.edit_message_content),
    re_path('get/(?P<pk>(\d)+)/$', views.get_message),
    path('get_list_for_user_chat/', views.get_message_list_user_chat),
]
