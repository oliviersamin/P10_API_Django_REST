from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



class Projects(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=400)
    type = models.CharField(max_length=128)
    contributors = models.ManyToManyField(User, related_name="collaborators")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_author")

    def __str__(self):
        contributors = [contributor.pk for contributor in self.contributors.all()]
        return "id: {} - title: {} - author: {} - contributors: {}".format(self.pk, self.title, self.author.pk,
                                                                           contributors)


class Issues(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=400)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=128)
    # project_id = models.IntegerField('project id')
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    status = models.CharField(max_length=128)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='issue_author')
    assignee = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='issue_assignee')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "id: {} - title: {}".format(self.pk, self.title)


class Comments(models.Model):
    description = models.CharField(max_length=400)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comment_author")
    issue_id = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "id: {} - description: {}".format(self.pk, self.description)
