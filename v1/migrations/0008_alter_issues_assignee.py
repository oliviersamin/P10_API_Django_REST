# Generated by Django 3.2.7 on 2021-09-13 13:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('v1', '0007_rename_issue_id_comments_issue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issues',
            name='assignee',
            field=models.ForeignKey(default=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_author', to=settings.AUTH_USER_MODEL), on_delete=django.db.models.deletion.CASCADE, related_name='issue_assignee', to=settings.AUTH_USER_MODEL),
        ),
    ]
