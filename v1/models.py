from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

PROJECT_TYPES = [('back-end', 'back-end'), ('front-end', 'front-end'), ('ios', 'ios'), ('android', 'android')]
ISSUE_TAGS = [('bug', 'bug'), ('amélioration', 'amélioration'), ('tâche', 'tâche')]
ISSUE_STATUS = [('à faire', 'à faire'), ('en cours', 'en cours'), ('terminé', 'terminé')]
ISSUE_PRIORITIES = [('faible', 'faible'), ('moyenne', 'moyenne'), ('élevée', 'élevée')]

class Projects(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=400)
    type = models.CharField(choices=PROJECT_TYPES, max_length=128)
    contributors = models.ManyToManyField('auth.User', related_name="collaborators")
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="project_author")
    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_author")

    def __str__(self):
        contributors = [contributor.pk for contributor in self.contributors.all()]
        return "id: {} - title: {} - author: {} - contributors: {}".format(self.pk, self.title, self.author.pk,
                                                                           contributors)


class Issues(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=400)
    tag = models.CharField(choices=ISSUE_TAGS, max_length=128)
    priority = models.CharField(choices=ISSUE_PRIORITIES, max_length=128)
    # project_id = models.IntegerField('project id')
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    status = models.CharField(choices=ISSUE_STATUS, default='à faire', max_length=128)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='issue_author')
    assignee = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='issue_assignee')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "id: {} - title: {}".format(self.pk, self.title)


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=400)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comment_author")
    issue = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "id: {} - description: {}".format(self.pk, self.description)
