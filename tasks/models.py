from datetime import timedelta

from django.core.exceptions import ValidationError
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


class Team(models.Model):
    """Model used to represent a team, namely its name and members"""

    team_name = models.CharField(max_length=50,unique=True, blank=False, primary_key=True)
    team_members = models.ManyToManyField(User, related_name='teams', blank=False)
    team_admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def invite_member(self,user):
        """method to invite user to team"""
        self.team_members.add(user)

    def remove_member(self, user):
        """method to remove user from team"""
        self.team_members.remove(user)

    def __str__(self):
        return self.team_name


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
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=False)
    members = models.ManyToManyField(User, related_name='assigned_members', blank=False)

    def __str__(self):
        return self.name

    

class Notifications(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_receieved')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_sent', default=1)
    message = models.TextField(max_length=100, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp'] # Order by timestamp in descending order

    def __str__(self):
        return f'{self.sender} to {self.recipient}: {self.message}'

class TimeLogging(models.Model):
    """record how many time a user spent on a task"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField(default=timedelta())

    def clean(self):
        super().clean()

        """ Check if start_time is before end_time"""
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError({'start_time': 'Start time must be before end time.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        """ Calculate duration before saving"""
        if self.start_time and self.end_time:
            self.duration = self.end_time - self.start_time
            self.duration_minutes = self.duration.total_seconds() // 60
        super().save(*args, **kwargs)






