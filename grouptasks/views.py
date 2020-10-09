from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.contrib.auth.models import User

from grouptasks.serializers import (
    UserSerializer,
    MyGroupSerializer,
    GroupSerializer,
    GroupSummarySerializer,
    TaskSerializer,
    MyTasksSerializer,
    CreateTaskSerializer,
    MembershipSerializer,
)
from grouptasks.models import Group, Task, Membership
from grouptasks.custompermissions import (
    IsSuperUser,
    IsTheUser,
    IsInTaskGroup, 
    IsGroupMember,
    IsPersonEnteringGroup,
    IsTaskInCharge,
    IsPersonInTheGroup,
)

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'users' : reverse(UserList.name, request=request),
            'tasks' : reverse(TaskCreate.name, request=request),
        })

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'
    permission_classes = (
        permissions.IsAuthenticated,
        IsSuperUser,
    )

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'
    permission_classes = (
        permissions.IsAuthenticated,
        IsTheUser,
    )

class MyGroups(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = MyGroupSerializer
    name = 'group-list'
    permission_classes = (
        permissions.IsAuthenticated,
        IsTheUser,
    )

class Groups(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSummarySerializer
    name = 'group-create'
    permission_classes = (
        permissions.IsAuthenticated,
    )

class GroupDetail(generics.RetrieveDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    name = 'group-detail'
    permission_classes = (
        permissions.IsAuthenticated,
        IsGroupMember,
    )

class TaskCreate(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = CreateTaskSerializer
    name = 'task-create'
    permission_classes = (
        IsInTaskGroup,
    )

class MyTasks(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = MyTasksSerializer
    name = 'task_list'
    permission_classes = (
        IsTaskInCharge,
    )

class MembershipsList(generics.ListCreateAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    name = 'memberships'
    filter_fields = ('user', 'group')
    # permission_classes = (
    #     IsPersonEnteringGroup,
    # )

class MembershipDetail(generics.RetrieveDestroyAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    name = 'membership-detail'
    # permission_classes = (
    #     IsPersonInTheGroup,
    # )

    def destroy(self, request, *args, **kwargs):
        member_to_delete = self.get_object().user
        all_person_in_charges = []
        for task in self.get_object().group.group_tasks.all():
            all_person_in_charges.append(task.in_charge)
     
        if member_to_delete in all_person_in_charges:
            return Response({'detail': 'Person in charge still have to do' }, status=status.HTTP_400_BAD_REQUEST)        
        else:
            return super(MembershipDetail,self).destroy(request, *args, **kwargs)

# Create your views here.
