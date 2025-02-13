from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer
from rest_framework import permissions
from rest_framework.decorators import action

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


    @action(detail=False, methods=['GET'])
    def user_categories(self, request):
        """List user created categories"""
        user_categories = self.queryset.filter(user=request.user).order_by('name')
        serializer = self.get_serializer(user_categories, many = True)
        return Response(serializer.data)
    
class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def user_tasks(self, request):
        """List user created tasks"""
        user_tasks = self.queryset.filter(user = request.user).order_by('-created_at')
        serializer = self.get_serializer(user_tasks, many=True)
        return Response(serializer.data)