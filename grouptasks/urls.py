from django.urls import path
from grouptasks.views import (
    ApiRoot,
    UserList,
    UserDetail,
    UserfromUsername,
    MyGroups,
    GroupDetail,
    TaskCreate,
    TaskDetail,
    MyTasks,
    AddRemoveMembership,
)

urlpatterns = [
    path('', ApiRoot.as_view(), name=ApiRoot.name),
    path('users', UserList.as_view(), name=UserList.name),
    path('users/<int:pk>', UserDetail.as_view(), name=UserDetail.name),
    path('users/<str:username>', UserfromUsername.as_view(), name=UserfromUsername.name),
    path('users/<int:pk>/groups', MyGroups.as_view(), name=MyGroups.name),
    path('users/<int:pk>/tasks', MyTasks.as_view(), name=MyTasks.name),
    path('groups/<int:pk>', GroupDetail.as_view(), name=GroupDetail.name),
    path('groups/<int:group_pk>/users/<int:user_pk>', AddRemoveMembership.as_view(), name=AddRemoveMembership.name),
    path('tasks', TaskCreate.as_view(), name=TaskCreate.name),
    path('tasks/<int:pk>', TaskDetail.as_view(), name=TaskDetail.name),
]
