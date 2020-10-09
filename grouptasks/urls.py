from django.urls import path
from grouptasks.views import (
    ApiRoot,
    UserList,
    UserDetail,
    MyGroups,
    GroupDetail,
    TaskCreate,
    MyTasks,
    MembershipsList,
    MembershipDetail,
)

urlpatterns = [
    path('', ApiRoot.as_view(), name=ApiRoot.name),
    path('users', UserList.as_view(), name=UserList.name),
    path('users/<int:pk>', UserDetail.as_view(), name=UserDetail.name),
    path('users/<int:pk>/groups', MyGroups.as_view, name=MyGroups.name),
    path('users/<int:pk>/tasks', MyTasks.as_view(), name=MyTasks.name),
    path('groups/<int:pk>', GroupDetail.as_view(), name=GroupDetail.name),
    path('tasks', TaskCreate.as_view(), name=TaskCreate.name),
    path('memberships/', MembershipsList.as_view(), name=MembershipsList.name),
    path('memberships/<int:pk>/', MembershipDetail.as_view(), name=MembershipDetail.name),
]
