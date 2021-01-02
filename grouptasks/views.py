from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import views

from django.contrib.auth.models import User
from django.db import IntegrityError

from grouptasks.serializers import (
    UserSerializer,
    UserModelSerializer,
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
    IsTaskInCharge,
    IsPersonInTheGroup,
)

# Need to add sorting mechanism
class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'users' : reverse(UserList.name, request=request),
            'tasks' : reverse(TaskCreate.name, request=request),
        })

class UserList(views.APIView):
    name = 'user-list'

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        user_serializer = UserSerializer(
            queryset, 
            many=True,
            context={ 
                'request': request 
            }
        )
        return Response(user_serializer.data)

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']

        if ((not username) or (not password)):
            raise ValidationError(detail="Username and password can't be empty")


        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,            
            )
            user.save()
        except IntegrityError:
            return Response(
                ["Username is taken"],
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_serializer = UserSerializer(
            user,
            context={ 
                'request': request 
            }
        )
        return Response(
            user_serializer.data, 
            status=status.HTTP_201_CREATED
        )

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'
    permission_classes = (
        permissions.IsAuthenticated,
        IsTheUser,
    )

class UserfromUsername(generics.RetrieveAPIView):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-from-username'
    permission_classes = (
        permissions.IsAuthenticated,
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
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group_instance = self.perform_create(serializer)
        group_instance.members.set([request.user])
        group_instance.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        return instance

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
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
        permissions.IsAuthenticated,
        IsInTaskGroup,
    )

class MyTasks(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = MyTasksSerializer
    name = 'task-list'
    permission_classes = (
        permissions.IsAuthenticated,
        IsTaskInCharge,
    )

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    name = 'task-detail'
    permission_classes = (
        permissions.IsAuthenticated,
        IsInTaskGroup,
    )

class AddRemoveMembership(generics.GenericAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsPersonInTheGroup,
    )
    serializer_class = MembershipSerializer
    name = 'membership-detail'
    
    def get_object(self):
        membership = Membership.objects.get(user=self.kwargs['user_pk'], group=self.kwargs['group_pk'])
        self.check_object_permissions(self.request, membership)
        return membership

    def put(self, request, *args, **kwargs):
        new_member = self.get_serializer(data={
            'user': kwargs['user_pk'],
            'group': kwargs['group_pk']
            })
        new_member.is_valid(raise_exception=True)
        new_member.save()
        return Response(data=new_member.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        membership_to_delete = self.get_object()

        all_person_in_charges = [task.in_charge for task in membership_to_delete.group.group_tasks.all()]

        if membership_to_delete.user in all_person_in_charges:
            return Response({'detail': 'This user is still in charge of some tasks' }, status=status.HTTP_400_BAD_REQUEST)
        
        if (membership_to_delete.group.members.all().count() == 1):
            return Response({'detail': 'This user is the last member of the group. Please delete the group instead!'}, status=status.HTTP_400_BAD_REQUEST)

        membership_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
