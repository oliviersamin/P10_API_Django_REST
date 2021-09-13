from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Projects, Issues, Comments


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
        fields = ['id', 'title']  # , 'description', 'type', 'contributors', 'author']
        extra_kwargs = {'id': {'read_only': True}}


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'contributors', 'author']
        extra_kwargs = {'id': {'read_only': True},
                        'contributors': {'read_only': True},
                        'author': {'read_only': True}}


class ProjectContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['contributors']


class IssuesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = ['id', 'title']
        extra_kwargs = {'id': {'read_only': True}}


class CreateIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = ['id', 'title', 'description', 'tag', 'priority', 'project_id',
                  'status', 'assignee', 'author', 'created_time']

        extra_kwargs = {'id': {'read_only': True},
                        'project_id': {'read_only': True},
                        'author': {'read_only': True},
                        'created_time': {'read_only': True},
                        }


class CommentsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'description']

        extra_kwargs = {'id': {'read_only': True},
                        }


class CommentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'description', 'issue_id', 'author', 'created_time']

        extra_kwargs = {'id': {'read_only': True},
                        'issue_id': {'read_only': True},
                        'author': {'read_only': True},
                        'created_time': {'read_only': True},
                        }
