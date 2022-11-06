from django.urls import path, re_path

from .views import ChatViewSet

urlpatterns = [
    path('add_member/', ChatViewSet.as_view({'put': 'partial_update_add_user_to_chat'})),
    path('create/', ChatViewSet.as_view({'post': 'create'})),
    re_path('delete/(?P<pk>(\d)+)/', ChatViewSet.as_view({'delete': 'destroy'})),
    path('delete_member/', ChatViewSet.as_view({'delete': 'delete_member_from_chat'})),
    re_path('get/(?P<pk>(\d)+)/', ChatViewSet.as_view({'get': 'retrieve'})),
    path('get_all_chats/', ChatViewSet.as_view({'get': 'list_all_chats'})),
    re_path('get_users/(?P<user_pk>(\d)+)/', ChatViewSet.as_view({'get': 'list_user_chats'})),
    path('edit/', ChatViewSet.as_view({'put': 'update'})),
]
