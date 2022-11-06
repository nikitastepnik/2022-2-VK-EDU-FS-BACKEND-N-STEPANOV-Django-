from django.urls import path, re_path

from .views import MessageViewSet

urlpatterns = [
    path('create/', MessageViewSet.as_view({'post': 'create'})),
    path('delete/', MessageViewSet.as_view({'delete': 'destroy'})),
    path('edit/', MessageViewSet.as_view({'put': 'partial_update'})),
    re_path('get/(?P<pk>(\d)+)/$', MessageViewSet.as_view({'get': 'retrieve_without_filters'})),
    path('get_list_for_user_chat/', MessageViewSet.as_view({'get': 'retrieve_filter_user_and_chat'})),
    path('get_list_for_chat/', MessageViewSet.as_view({'get': 'retrieve_filter_chat'})),
    re_path('mark_as_viewed/', MessageViewSet.as_view({'put': 'partial_update_status'})),
]
