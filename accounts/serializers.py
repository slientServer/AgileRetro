# from accounts.models import User
from rest_framework import serializers
from .models import User

class UsersSerializer(serializers.ModelSerializer):
    topics_count = serializers.DecimalField(max_digits=1000, decimal_places=0)
    posts_count = serializers.DecimalField(max_digits=1000, decimal_places=0)
    class Meta:
        model = User
        fields = ('username', 'topics_count', 'posts_count')