from django.urls import path
from grouptasks.views import (
    ApiRoot,
    UserList,
    UserDetail,
    GroupList,
    GroupDetail,
    TaskCreate,
    TaskDetail,
    MembershipCreate,
    MembershipDetail,
)

urlpatterns = [
    path('', ApiRoot.as_view(), name=ApiRoot.name),
    path('users/', UserList.as_view(), name=UserList.name),
    path('users/<int:pk>/', UserDetail.as_view(), name=UserDetail.name),
    path('groups/', GroupList.as_view(), name=GroupList.name),
    path('groups/<int:pk>/', GroupDetail.as_view(), name=GroupDetail.name),
    path('tasks/create', TaskCreate.as_view(), name=TaskCreate.name),
    path('tasks/<int:pk>/', TaskDetail.as_view(), name=TaskDetail.name),
    path('memberships/create/', MembershipCreate.as_view(), name=MembershipCreate.name),
    path('memberships/<int:pk>/', MembershipDetail.as_view(), name=MembershipDetail.name),
]
