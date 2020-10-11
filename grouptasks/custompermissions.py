from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsTheUser(BasePermission):
    def has_object_permission(self, request, view, user):
        return request.user == user

class IsInTaskGroup(BasePermission):
    def has_object_permission(self, request, view, task):
        return request.user in task.group.members.all()

class IsGroupMember(BasePermission):
    def has_object_permission(self, request, view, group):
        return request.user in group.members.all()

class IsTaskInCharge(BasePermission):
    def has_object_permission(self, request, view, user):
        return request.user == user

class IsPersonInTheGroup(BasePermission):
    def has_object_permission(self, request, view, membership):
        return request.user in membership.group.members.all()