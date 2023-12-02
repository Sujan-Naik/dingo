from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from tasks.forms import LogInForm, PasswordForm, UserForm, SignUpForm, CreateTaskForm, TeamCreateForm, InviteMemberForm, TaskSortForm
from tasks.helpers import login_prohibited
from .models import Task, Team, User


@login_required
def dashboard(request):
    """Display the current user's dashboard."""

    current_user = request.user
    return render(request, 'dashboard.html', {'user': current_user})


@login_prohibited
def home(request):
    """Display the application's start/home screen."""

    return render(request, 'home.html')

class TaskListView(LoginRequiredMixin, ListView):
    """View the task list"""
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        """Filter tasks based on the logged-in user"""
        sort_by = self.request.GET.get("s", "deadline") # default sort is by deadline
        filter_by = self.request.GET.get("fp", "name") + "__icontains" # default filter is by name
        filter_string = self.request.GET.get("fs", "")
        return Task.objects.filter(**{"author":self.request.user, filter_by:filter_string}).order_by(sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskSortForm()
        return context

    def post(self, request, *args, **kwargs):
        """Deal with sorting + filtering"""
        sort = request.POST.get('asc_or_desc', "") + request.POST.get('sort_by')
        filter_property = request.POST.get('filter_by')
        filter_string = request.POST.get('filter_string')
        return HttpResponseRedirect(reverse('task_list') + f"?s={sort}&fp={filter_property}&fs={filter_string}")

class TaskDetailView(LoginRequiredMixin, DetailView):
    """view the task detail"""
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

    def get_object(self, queryset=None):
        """get the current task"""
        return get_object_or_404(Task, name=self.kwargs['name'])

    def get_context_data(self, **kwargs):
        """generate the details of current task and show them in task_detail.html"""
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        time_left = context['task'].deadline - now
        if time_left :
            context['time_left'] = 1;
            context['days_left'] = time_left.days
            context['hours_left'] = time_left.seconds // 3600
            context['minutes_left'] = (time_left.seconds % 3600) // 60
        else:
            context['time_left'] = 0;
            context['days_left'] = 0
            context['hours_left'] = 0
            context['minutes_left'] = 0

        return context

class TeamListView(LoginRequiredMixin, ListView):
    """view the team list"""
    model = Team
    template_name = 'team_list.html'
    context_object_name = 'team_list'

    def get_queryset(self):
        """Filter teams based on the logged-in user"""
        return Team.objects.filter(team_members=self.request.user)

class TeamDetailView(LoginRequiredMixin, DetailView):
    """view the task detail"""
    model = Team
    template_name = 'team_detail.html'
    context_object_name = 'team'

    def get_object(self, queryset=None):
        """get the current task"""
        return get_object_or_404(Team, team_name=self.kwargs['team_name'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_users'] = User.objects.all()
        context['invite_form'] = InviteMemberForm()
        return context

    def post(self, request, *args, **kwargs):
        team = self.get_object()
        action = request.POST.get('action')

        if action == 'invite':
            form = InviteMemberForm(request.POST, instance=team)
            users_to_invite = request.POST.getlist('username')
            if form.is_valid():
                # users_to_invite = form.cleaned_data.get('team_members')
                for username in users_to_invite:
                    user = User.objects.get(username=username)
                # check if the user is already in the team
                    if user in team.team_members.all():
                        messages.error(request, f'{user.username} is already in the team.')
                    else:
                        team.team_members.add(user)
                        messages.success(request, f'Successfully invite {user.username}.')

        elif action == 'remove':
            username = request.POST.get('username')
            user_to_remove = get_object_or_404(User, username=username)

            if request.user == team.team_admin:
                team.team_members.remove(user_to_remove)
                messages.success(request, f'{user_to_remove.username} is removed from the team.')
            else:
                messages.error(request, 'You do not have permission to remove member')

        return HttpResponseRedirect(reverse('team_detail', kwargs={'team_name': team.team_name}))

class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


def log_out(request):
    """Log out the current user"""

    logout(request)
    return redirect('home')


class PasswordView(LoginRequiredMixin, FormView):
    """Display password change screen and handle password change requests."""

    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""

        messages.add_message(self.request, messages.SUCCESS, "Password updated!")
        return reverse('dashboard')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


class SignUpView(LoginProhibitedMixin, FormView):
    """Display the sign up screen and handle sign ups."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


class CreateTaskView(LoginRequiredMixin, FormView):
    """Display the create task screen and handle creating tasks."""

    model = CreateTaskForm
    form_class = CreateTaskForm
    template_name = "create_task.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the create task form."""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        # self.object = form.save()
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


class TeamView(LoginRequiredMixin, FormView):
    """Allow logged-in users to create new teams"""

    template_name = 'team.html'
    form_class = TeamCreateForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the team create form."""
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new team."""
        if form.is_valid():
            form.save()
            messages.success(self.request, "Team created!")
            return redirect('dashboard')
        return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Form submission failed. Please check the form for errors.")
        return super().form_invalid(form)
