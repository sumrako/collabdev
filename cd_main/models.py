from django.db import models


# Create your models here.
class User(models.Model):
    full_name = models.CharField(max_length=100, help_text="Enter your full name", blank=False)
    date_of_birth = models.DateField(help_text="Enter your birthday", blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    update_at = models.DateTimeField(auto_now=True, blank=False)
    soft_delete = models.BooleanField(default=False, blank=False)
    user_avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    skills = models.ManyToManyField(to='Skill', blank=True)

    def __str__(self):
        return self.full_name


class Skill(models.Model):
    title = models.CharField(max_length=100, blank=False)
    code = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=100, help_text="Enter project title", blank=False)
    description = models.CharField(max_length=5000, help_text="Enter project description", blank=False)
    skills = models.ManyToManyField(to='Skill', blank=True)
    project_type = models.ForeignKey(to='ProjectTypes', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    update_at = models.DateTimeField(auto_now=True, blank=False)
    soft_delete = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return self.title


class UserProjectRelation(models.Model):
    user_id = models.ManyToManyField(to=User, related_name='users')
    project_id = models.ManyToManyField(to=Project, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id}-{self.project_id}"


class ProjectTypes(models.Model):
    title = models.CharField(max_length=100, blank=False)
    code = models.PositiveIntegerField(blank=False)

    def __str__(self):
        return self.title
