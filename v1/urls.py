from django.urls import include, path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.BlacklistRefreshView.as_view(), name="logout"),
]
