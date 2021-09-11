from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Projects, Issues, Comments


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user



class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'contributors', 'author_user_id']
        extra_kwargs = {'id': {'read_only': True}}

