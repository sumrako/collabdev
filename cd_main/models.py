from django.db import models
from django.contrib.auth.models import AbstractUser


class Project(models.Model):
    title = models.CharField(max_length=127, help_text="Enter project title", blank=False)
    description = models.TextField(max_length=8192, help_text="Enter project description", blank=False)
    skills = models.ManyToManyField(to='Skill', blank=True)
    project_type = models.ForeignKey(to='ProjectTypes', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    soft_delete = models.BooleanField(default=False, blank=False)
    status = models.ForeignKey(to='Status', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    birth_date = models.DateField(help_text="Enter your birthday", blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    user_avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    skills = models.ManyToManyField(to='Skill', blank=True)
    projects = models.ManyToManyField(Project, through='UserProjectRelation')

    def __str__(self):
        return self.username


class Skill(models.Model):
    title = models.CharField(max_length=127, blank=False)
    code = models.CharField(max_length=127, blank=False)

    def __str__(self):
        return self.title


class UserProjectRelation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class ProjectTypes(models.Model):
    title = models.CharField(max_length=127, blank=False)
    code = models.CharField(max_length=127, blank=False)

    def __str__(self):
        return self.title


class Status(models.Model):
    title = models.CharField(max_length=127, blank=False)
    code = models.CharField(max_length=127, blank=False)

    def __str__(self):
        return self.title
