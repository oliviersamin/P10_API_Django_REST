from django.contrib import admin
from django.contrib.auth.models import User
from .models import Projects, Comments, Issues

admin.site.register(Projects)
admin.site.register(Issues)
admin.site.register(Comments)
