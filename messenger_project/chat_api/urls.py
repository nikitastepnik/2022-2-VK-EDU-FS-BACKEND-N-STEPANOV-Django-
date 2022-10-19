from django.urls import path

from . import views

urlpatterns = [
    path('/create/chat', views.create_chat),
    path('/list/chats', views.list_of_chats),
    path('/page/chat', views.page_chat),
]
