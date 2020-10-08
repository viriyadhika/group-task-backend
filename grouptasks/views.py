from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.contrib.auth.models import User

from grouptasks.serializers import (
    UserSerializer, 
    GroupSerializer,
    TaskSerializer,
    TaskListofAUserSerializer,
    CreateTaskSerializer,
    MembershipSerializer,
)
from grouptasks.models import Group, Task, Membership
from grouptasks.custompermissions import (
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
            'groups' : reverse(GroupList.name, request=request),
        })

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'
    filter_fields = ('username',)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'

class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    name = 'group-list'

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

class TaskListofAUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = TaskListofAUserSerializer
    name = 'task_list'
    permission_classes = (
        IsTaskInCharge,
    )

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    name = 'task-detail'
    permission_classes = (
        IsInTaskGroup,
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
