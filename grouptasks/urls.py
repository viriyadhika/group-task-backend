from django.urls import path
from grouptasks.views import (
    UserList,
    UserDetail,
    GroupList,
    GroupDetail,
)

urlpatterns = [
    path('users/', UserList.as_view(), name='users'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('groups/', GroupList.as_view(), name='groups'),
    path('groups/<int:pk>/', GroupDetail.as_view(), name='group-detail'),
]
