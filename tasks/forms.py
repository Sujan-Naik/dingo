"""Forms for the tasks app."""
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import User, Task, Team, TimeLogging


class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user


class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class NewPasswordMixin(forms.Form):
    """Form mixing for new_password and password_confirmation fields."""

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
        )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Form mixing for new_password and password_confirmation fields."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""

        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(username=self.user.username, password=password)
        else:
            user = None
        if user is None:
            self.add_error('password', "Password is invalid")

    def save(self):
        """Save the user's new password."""

        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user


class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def save(self):
        """Create a new user."""

        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('new_password'),
        )
        return user


class CreateTaskForm(forms.ModelForm):
    """Form enabling registered users to create tasks."""
    class Meta:
        """Form options."""
        model = Task
        fields = ['name', 'description', 'deadline', 'team', 'members', 'priority']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            })
        }

    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    priority = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}), choices=Task.Priority.choices, initial=Task.Priority.MEDIUM)

    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check form-check-inline"})
    )

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""

        super().__init__(**kwargs)
        self.user = user
        self.fields['team'] = forms.ModelChoiceField(widget=forms.Select(attrs={"class": "form-control"}),
                                      queryset=Team.objects.filter(team_members__in=[self.user]))
        '''self.fields['members'] = forms.ModelMultipleChoiceField(
            queryset=Team.objects.filter(team_members__in=[self.user]).values('team_name'),
            widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check form-check-inline"}))'''
    def clean(self):
        """Clean the deadline datatime data and generate messages for any errors."""

        super().clean()
        deadline_datetime = self.cleaned_data.get('deadline')
        """Sends error if deadline time has already passed"""
        if deadline_datetime <= timezone.now():
            self.add_error('deadline', "Deadline is invalid")
        if self.user is None:
            self.add_error(None, "You must be logged in first!")

        team = self.cleaned_data.get('team')
        members = self.cleaned_data.get('members')
        if members is None:
            self.add_error('members', "Select at least one team member!")
        else:
            for member in members:
                if not team in member.teams.all():
                    self.add_error('members', "Members must be in the specified team!")
                    break

    def save(self):
        """Create a new task."""
        super().save(commit=False)
        task_name = self.cleaned_data.get("name")
        task_description = self.cleaned_data.get("description")
        task_deadline = self.cleaned_data.get("deadline")
        task_team = self.cleaned_data.get("team")
        task_priority = self.cleaned_data.get("priority")
        task = Task(name=task_name, description=task_description, deadline=task_deadline, priority=task_priority,
                    author=self.user, team=task_team)
        task.save()
        task.members.set(self.cleaned_data.get('members'))
        return task


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', 'team_members']

    team_name = forms.CharField(
        required=True
    )

    team_members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        to_field_name='username',
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()

        team_members = cleaned_data.get('team_members')
        if not team_members:
            raise ValidationError('A team must have at least 1 member.')

        team_name = cleaned_data['team_name']

        if Team.objects.filter(team_name=team_name).exclude(pk=self.instance.pk).exists():
            raise ValidationError('A team with this name already exists.')

        if not team_name:
            raise ValidationError('A team name cannot be empty')

        if self.user is None:
            self.add_error(None, "You must be logged in first!")

        return cleaned_data

    def save(self, commit=True):
        team = super().save(commit=False)
        team.team_admin = self.user
        team.team_name = self.cleaned_data.get('team_name')
        team.save()
        team.team_members.set(self.cleaned_data.get('team_members'))

        return team

class InviteMemberForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name']
        widgets = {
        }


class ModifyTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline', 'priority']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'class':'form-control', 'type':'datetime-local'})
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_deadline(self):
        deadline_datetime = self.cleaned_data.get('deadline')

        if deadline_datetime < timezone.now():
            raise forms.ValidationError("Deadline is Invalid")
        
        return deadline_datetime
    
    def save(self, commit=True):
        task = super().save(commit=False)
        if commit:
            task.save()

        return task



class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeLogging
        fields = ['start_time', 'end_time']

    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        help_text='Format: YYYY-MM-DDTHH:MM'
    )

    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        help_text='Format: YYYY-MM-DDTHH:MM'
    )


