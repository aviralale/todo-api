from rest_framework import serializers
from .models import  Task, Category
import markdown

class TaskSerializer(serializers.ModelSerializer):
    description_html = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ['id', 'title', 'description','category','description_html','is_completed', 'completion_date', 'created_at', 'updated_at']

    def get_description_html(self, obj):
        return markdown.markdown(obj.description)
    
    def validate_category(self, value):
        """Ensure the category exists."""
        if not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Invalid category ID.")
        return value

    def create(self, validated_data):
        """
        Automatically associate the task with the authenticated user.
        """
        user = self.context['request'].user  # Get the authenticated user
        validated_data['user'] = user  # Set the user field
        return super().create(validated_data)
        

class CategorySerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True, source='task_set')
    class Meta:
        model = Category
        fields = ["id",'name','created_at', 'tasks']
        read_only_fields = ['user']