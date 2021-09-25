from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from . import serializers
from .models import Projects, Issues, Comments
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import CharField, Value
from itertools import chain
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class BlacklistRefreshView(APIView):
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success")


class Signup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class ProjectList(APIView):
    """
    List all the projects related to the user
    * the user must be logged in to access these informations
    * only the projects related to the user are accessible through the GET method
    * the POST method allows the user to create a new project, he will be the author.
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        users = list(User.objects.all())
        # print("############## PRINT #####################")
        # print(users)
        # print(request, request.user, request.auth)
        if request.user in users:
            projects1 = Projects.objects.filter(author=request.user)
            projects2 = Projects.objects.filter(contributors=request.user)
            projects1 = projects1.annotate(content_type=Value('author', CharField()))
            projects2 = projects2.annotate(content_type=Value('contributor', CharField()))
            projects = set(sorted(chain(projects1, projects2), key=lambda project: project.id))
            projects = list(projects)
            serializer = serializers.ProjectListSerializer(projects, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        serializer = serializers.ProjectDetailSerializer(data=request.data)
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
    permission_classes = (IsAuthenticated,)
    def get(self, request, project_id):
        project = Projects.objects.get(id=project_id)
        contributors = [contributor.pk for contributor in project.contributors.all()]
        if (project.author.pk == request.user.pk) or (request.user.pk in contributors):
            serializer = serializers.ProjectDetailSerializer(project)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request, project_id):
        project = Projects.objects.get(id=project_id)
        serializer = serializers.ProjectDetailSerializer(project, data=request.data)
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
    permission_classes = (IsAuthenticated,)
    def get(self, request, project_id):
        project = Projects.objects.get(id=project_id)
        contributors = [contributor.pk for contributor in project.contributors.all()]
        if (project.author.pk == request.user.pk) or (request.user.pk in contributors):
            serializer = serializers.ProjectContributorSerializer(project)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request, project_id):
        users = list(User.objects.all())
        project = Projects.objects.get(id=project_id)
        serializer = serializers.ProjectContributorSerializer(project, data=request.data)
        print("############## REQUEST.DATA ###############")
        print(request.data)
        # print(users)
        # ids=[]
        # for user in users:
        #     if user.email in request.data['contributors']:
        #         print("################  YOUPI ######################")
        #         ids.append(user.pk)
        #         print(ids)

        if (project.author.pk == request.user.pk) & (serializer.is_valid()):
            print(serializer.validated_data)
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
    permission_classes = (IsAuthenticated,)
    def delete(self, request, project_id, user_id):
        project = Projects.objects.get(id=project_id)
        contributors = [contributor.pk for contributor in project.contributors.all()]
        for index, value in enumerate(contributors):
            if (value == user_id) & (project.author.pk == request.user.pk):
                contributors.pop(index)
                print("CONTRIBUTORS = ", contributors)
                project.contributors.set(contributors)
                project.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class IssuesList(APIView):
    """
    A FAIRE
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, project_id):
        project = Projects.objects.get(id=project_id)
        contributors = [contributor.pk for contributor in project.contributors.all()]
        if (project.author.pk == request.user.pk) or (request.user.pk in contributors):
            issues = sorted(list(Issues.objects.filter(project_id=project_id)), key=lambda issue: issue.created_time)
            issues.reverse()
            if issues == []:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                serializer = serializers.IssuesListSerializer(issues, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request, project_id):
        project = Projects.objects.get(id=project_id)
        contributors = [contributor.pk for contributor in project.contributors.all()]
        if (project.author.pk == request.user.pk) or (request.user.pk in contributors):
            serializer = serializers.CreateIssueSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save(project_id=project, author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_403_FORBIDDEN)


class IssueDetails(APIView):
    """
    A FAIRE
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, project_id, issue_id):
        project = Projects.objects.get(id=project_id)
        contributors = [contributor.pk for contributor in project.contributors.all()]
        if (project.author.pk == request.user.pk) or (request.user.pk in contributors):
            issue = Issues.objects.get(id=issue_id)
            serializer = serializers.CreateIssueSerializer(issue)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request, project_id, issue_id):
        issue = Issues.objects.get(id=issue_id)
        serializer = serializers.CreateIssueSerializer(issue, data=request.data)
        if (serializer.is_valid()) & (issue.author.pk == request.user.pk):
            serializer.save()
            return Response(serializer.data)
        elif (serializer.is_valid()) & (issue.author.pk != request.user.pk):
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, issue_id):
        issue = Issues.objects.get(id=issue_id)
        if issue.author.pk == request.user.pk:
            issue.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class CommentsList(APIView):
    """
    A FAIRE
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, project_id, issue_id):
        project = Projects.objects.get(id=project_id)
        contributors = [contributor.pk for contributor in project.contributors.all()]
        if (project.author.pk == request.user.pk) or (request.user.pk in contributors):
            issue = Issues.objects.get(id=issue_id)
            comments = sorted(list(Comments.objects.filter(issue_id=issue.id)),
                              key=lambda comment: comment.created_time)
            comments.reverse()
            if comments:
                serializer = serializers.CommentsListSerializer(comments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request, project_id, issue_id):
        project = Projects.objects.get(id=project_id)
        contributors = [contributor.pk for contributor in project.contributors.all()]
        if (project.author.pk == request.user.pk) or (request.user.pk in contributors):
            issue = Issues.objects.get(id=issue_id)
            serializer = serializers.CommentDetailsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(issue=issue, author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)


class CommentDetails(APIView):
    """
    A FAIRE
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, project_id, issue_id, comment_id):
        project = Projects.objects.get(id=project_id)
        contributors = [contributor.pk for contributor in project.contributors.all()]
        if (project.author.pk == request.user.pk) or (request.user.pk in contributors):
            comment = Comments.objects.get(id=comment_id)
            serializer = serializers.CommentDetailsSerializer(comment)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)


    def put(self, request, project_id, issue_id, comment_id):
        comment = Comments.objects.get(id=comment_id)
        serializer = serializers.CommentDetailsSerializer(comment, data=request.data)
        if (serializer.is_valid()) & (comment.author.pk == request.user.pk):
            serializer.save()
            return Response(serializer.data)
        elif (serializer.is_valid()) & (comment.author.pk != request.user.pk):
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, project_id, issue_id, comment_id):
        comment = Comments.objects.get(id=comment_id)
        if comment.author.pk == request.user.pk:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class UserView(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]
