from django.urls import include, path
from .views import ProjectList, Signup, ProjectDetail, ProjectContributors, DeleteContributor
from rest_framework import routers


app_name = 'v1'

# router = routers.DefaultRouter()
# router.register(r'projects', ProjectView)

urlpatterns = [
    path('projects/', ProjectList.as_view(), name='projects-list'),
    path('projects/<int:project_id>', ProjectDetail.as_view(), name='projects-list'),
    path('projects/<int:project_id>/users', ProjectContributors.as_view(), name='projects-list'),
    path('projects/<int:project_id>/users/<int:user_id>', DeleteContributor.as_view(), name='projects-list'),
    path('signup/', Signup.as_view(), name='signup'),
    # path('', views.redirection),
    # path('projects/', ),
]
