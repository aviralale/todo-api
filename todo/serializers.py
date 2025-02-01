from rest_framework import serializers
from .models import  Task, Category
import markdown

class TaskSerializer(serializers.ModelSerializer):
    description_html = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ['id', 'title', 'description','description_html', 'completion_date', 'created_at', 'updated_at']

    def get_description_html(self, obj):
        return markdown.markdown(obj.description)
        

class CategorySerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True, source='task_set')
    class Meta:
        model = Category
        fields = ['name','created_at', 'tasks']

        read_only_fields = ['user']