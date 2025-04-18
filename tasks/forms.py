"""Forms for the tasks app."""
import pytz
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


class CreateTaskForm1(forms.ModelForm):
    """First page of a form that creates a task"""

    class Meta:
        """Form options."""
        model = Task
        fields = ['name', 'description', 'deadline', 'team', 'priority']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            })
        }

    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    priority = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}), choices=Task.Priority.choices,
                                 initial=Task.Priority.MEDIUM)

    def __init__(self, user=None, **kwargs):
        """Construct a new form instance with a user instance."""

        super().__init__(**kwargs)
        self.user = user
        """Makes the team field only show the user's teams as options"""
        self.fields['team'] = forms.ModelChoiceField(widget=forms.Select(attrs={"class": "form-control"}),
                                                     queryset=Team.objects.filter(team_members__in=[self.user]))

    def clean(self):
        """Clean the deadline datatime data and generate messages for any errors."""

        super().clean()
        deadline_datetime = self.cleaned_data.get('deadline')

        """Checks if the deadline date is invalid"""
        if deadline_datetime is None:
            self.add_error('deadline', "Deadline is invalid")
        elif deadline_datetime <= timezone.now():
            """Sends an error if deadline time has already passed"""
            self.add_error('deadline', "Deadline is invalid")

        if self.user is None:
            self.add_error(None, "You must be logged in first!")


class CreateTaskForm2(forms.ModelForm):
    """Second page of a form that creates a task"""

    class Meta:
        """Form options."""
        model = Task
        fields = ['members']

    def __init__(self, user=None, team=None, **kwargs):
        """Construct new form instance with a user instance."""

        super().__init__(**kwargs)
        self.user = user
        self.team = team

        if self.team is not None:
            self.fields['members'] = forms.ModelMultipleChoiceField(
                queryset=team.team_members.all(),
                widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check form-check-inline"}))
        else:
            self.fields['members'] = forms.ModelMultipleChoiceField(
                queryset=User.objects.none(),
                widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check form-check-inline"}))

        self.fields['members'].label = "Assign Members"

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        if self.user is None:
            self.add_error(None, "You must be logged in first!")

        if self.team is None:
            self.add_error(None, "You must be select a team in the previous page first!")

        """Ensures at least one team member is selected"""
        members = self.cleaned_data.get('members')
        if members is None:
            self.add_error('members', "Select at least one team member!")
        else:
            """Checks if all members chosen are in the selected team"""
            for member in members:
                if not self.team in member.teams.all():
                    self.add_error('members', "Members must be in the specified team!")
                    break


class TeamCreateForm(forms.ModelForm):
    """Creates teams and initialises members"""
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
        """Ensures teams have at least one member, a unique non-null name and the user is logged in"""
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
        """Saves team name and members to database"""
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


class TaskSortForm(forms.Form):
    """Form to allow for sorting + filtering of the task list"""
    sorting_choices = [
        ("deadline", "Deadline"),
        ("name", "Name"),
        ("priority", "Priority"),
        ("author__username", "Author Username")
    ]
    filter_choices = [
        ("name", "Name"),
        ("description", "Description"),
        ("author__username", "Author Username")
    ]

    sort_by = forms.ChoiceField(choices=sorting_choices)
    asc_or_desc = forms.BooleanField(required=False)
    filter_by = forms.ChoiceField(choices=filter_choices)
    filter_string = forms.CharField(required=False)


class ModifyTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline', 'priority']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_deadline(self):
        deadline_datetime = self.cleaned_data.get('deadline')

        if deadline_datetime < timezone.now():
            raise forms.ValidationError("Deadline is Invalid")

        return deadline_datetime

    def save(self, commit=True):
        task = super().save(commit=True)
        return task


class ModifyTaskMembersForm(forms.ModelForm):
    add_members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    remove_members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super(ModifyTaskMembersForm, self).__init__(*args, **kwargs)

        # Dynamically set the queryset for add_members and remove_members based on the team
        if self.instance and self.instance.team:
            team_members = self.instance.team.team_members.all()
            assigned_members = self.instance.members.all()

            # Set the queryset for add_members to team members not assigned to the task
            self.fields['add_members'].queryset = team_members.exclude(id__in=assigned_members)

            # Set the queryset for remove_members to members assigned to the task
            self.fields['remove_members'].queryset = assigned_members

    class Meta:
        model = Task
        fields = ['add_members', 'remove_members']

class ReadAllNotificationsForm(forms.Form):
    # This form can be empty since we just need it to trigger the form submission
    pass

class TimeEntryForm(forms.ModelForm):
    """Form to let users enter time"""
    class Meta:
        model = TimeLogging
        fields = ['start_time', 'end_time']

    """set the form of start time and end time"""
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

class TimezoneForm(forms.Form):
    """Allows the user to select their timezone"""
    timezone = forms.ChoiceField(choices=[(x, x) for x in pytz.common_timezones], label=False)
