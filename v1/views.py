from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, ProjectListSerializer, ProjectDetailSerializer, ProjectContributorSerializer
from .models import Projects
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import CharField, Value
from itertools import chain
from rest_framework import status


class Signup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectList(APIView):
    """
    List all the projects related to the user
    * the user must be logged in to access these informations
    * only the projects related to the user are accessible through the GET method
    * the POST method allows the user to create a new project, he will be the author.
    """

    def get(self, request):
        projects1 = Projects.objects.filter(author=request.user)
        projects2 = Projects.objects.filter(contributors=request.user)
        projects1 = projects1.annotate(content_type=Value('author', CharField()))
        projects2 = projects2.annotate(content_type=Value('contributor', CharField()))
        projects = set(sorted(chain(projects1, projects2), key=lambda project: project.title))
        projects = list(projects)
        serializer = ProjectListSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):
    """
    Displays the details regarding the project with the corresponding id
    * the user must be logged in to access these informations
    * only the projects related to the user are accessible through the GET method

    """

    def get(self, request, project_id):
        project = Projects.objects.get(id=project_id)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    def put(self, request, project_id):
        project = Projects.objects.get(id=project_id)
        serializer = ProjectDetailSerializer(project, data=request.data)
        if (serializer.is_valid()) & (project.author.pk == request.user.pk):
            serializer.save()
            return Response(serializer.data)
        elif (serializer.is_valid()) & (project.author.pk != request.user.pk):
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id):
        project = Projects.objects.get(id=project_id)
        if project.author.pk == request.user.pk:
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class ProjectContributors(APIView):
    """
    à remplir
    """
    def get(self, request, project_id):
        project = Projects.objects.get(id=project_id)
        serializer = ProjectContributorSerializer(project)
        return Response(serializer.data)

    def post(self, request, project_id):
        project = Projects.objects.get(id=project_id)
        serializer = ProjectContributorSerializer(project, data=request.data)
        if (serializer.is_valid()) & (project.author.pk == request.user.pk):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif (serializer.is_valid()) & (project.author.pk != request.user.pk):
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteContributor(APIView):
    """
    à remplir
    """

    def delete(self, request, project_id, user_id):
        project = Projects.objects.get(id=project_id)
        contributors = [contributor.pk for contributor in project.contributors.all()]
        print('#############  user delete ######################')
        print(contributors, type(contributors))
        for index, id in enumerate(contributors):
            if (id == user_id) & (project.author.pk == request.user.pk):
                contributors.pop(index)
                print("CONTRIBUTORS = ", contributors)
                project.contributors.set(contributors)
                project.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class UserView(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

