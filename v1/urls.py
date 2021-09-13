from django.urls import include, path
from . import views

app_name = 'v1'


urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    path('projects/', views.ProjectList.as_view()),
    path('projects/<int:project_id>', views.ProjectDetail.as_view()),
    path('projects/<int:project_id>/users', views.ProjectContributors.as_view()),
    path('projects/<int:project_id>/users/<int:user_id>', views.DeleteContributor.as_view()),
    path('projects/<int:project_id>/issues', views.IssuesList.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>', views.IssueDetails.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments', views.CommentsList.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>', views.CommentDetails.as_view()),
]
