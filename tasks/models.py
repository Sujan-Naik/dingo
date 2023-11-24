from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar

class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )],
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)


    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        
        return self.gravatar(size=60)

class Task(models.Model):
    """Model used for tasks."""

    class Priority(models.IntegerChoices):
        """Priority level for the task"""
        BACKLOG = 1
        LOW = 2
        MEDIUM = 3
        HIGH = 4
        URGENT = 5

    name = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=5000, blank=False)
    deadline = models.DateTimeField(blank=False)
    priority = models.IntegerField(choices=Priority.choices, blank=False, default=Priority.MEDIUM)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Team(models.Model):
    """Model used to represent a team, namely its name and members"""

    team_name = models.CharField(max_length=50,unique=True, blank=False, primary_key=True)
    team_members = models.ManyToManyField(User, related_name='teams', blank=False)
    team_admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Notification(models.Model):

    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=100, blank=False)
    timestmap = models.DateTimeField(auto_now_add=True)

    




