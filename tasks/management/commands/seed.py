from django.core.management.base import BaseCommand, CommandError

from tasks.models import User, Team, Task

import pytz
from faker import Faker
from random import randint, random, sample
from datetime import datetime
from django.utils import timezone

user_fixtures = \
    [
        {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe'},
        {'username': '@janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe'},
        {'username': '@charlie', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson'},
    ]


class Command(BaseCommand):
    """Build automation command to seed the database."""

    USER_COUNT = 150
    TEAM_COUNT = 50
    TASKS_PER_TEAM = 300
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    generated_users = []
    generated_teams = []

    def __init__(self):
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        """Executes when seed command is called"""

        User.objects.filter(is_staff=False).delete()

        self.create_users()
        self.users = User.objects.all()

        john = User.objects.get(username="@johndoe")
        jane = User.objects.get(username="@janedoe")
        charlie = User.objects.get(username="@charlie")

        self.generated_users.append(john)
        self.generated_users.append(jane)
        self.generated_users.append(charlie)

        # team_name = self.faker.company()
        team_members = [john, jane, charlie]
        team_admin = john

        new_team = self.create_team(
            {
                "name": "A SPECIAL TEAM",
                "members": team_members,
                "admin": team_admin
            })

        for i in range(400):
            task_member_size = randint(2, 3)
            self.generate_task(john, new_team, task_member_size)
            self.generate_task(jane, new_team, task_member_size)
        # self.try_create_team({'name': team_name, 'members': team_members, 'admin': team_admin})

        length = len(self.generated_users)
        print(f"GEN SIZE: {length}")
        self.generate_random_teams()
        print(f"GEN SIZE: {len(self.generated_teams)}")
        self.generate_random_tasks()

    def create_users(self):
        """Creates pre-defined and random users"""

        self.generate_user_fixtures()
        self.generate_random_users()

    def generate_user_fixtures(self):
        """Loops over each fixture to create users"""

        for data in user_fixtures:
            self.try_create_user(data)

    def generate_random_users(self):
        """Generates random users"""

        user_count = User.objects.count()
        while user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}")
            user = self.generate_user()
            user_count = User.objects.count()
            self.generated_users.append(user)
        print("User seeding complete.      ")

    def generate_random_teams(self):
        """Generates random teams"""

        team_count = Team.objects.count()
        """Prevent charlie from being a team leader"""
        charlie = User.objects.get(username="@charlie")
        self.generated_users.remove(charlie)
        team_leaders = sample(self.generated_users, self.TEAM_COUNT)
        self.generated_users.append(charlie)
        counter = 0
        print("above while")
        while team_count < self.TEAM_COUNT:
            print(f"COUNTER: {counter}      ")
            print(f"Seeding team {team_count}/{self.TEAM_COUNT}")
            new_team = self.generate_team(team_leaders[counter])
            self.generated_teams.append(new_team)
            team_count = Team.objects.count()
            counter += 1
        print("Team seeding complete.      ")

    def generate_random_tasks(self):
        """Creates random tasks for each generated team"""

        for team in self.generated_teams:
            team_leaders = sample(self.generated_users, self.TEAM_COUNT)
            counter = 0
            print("above while")
            while counter < self.TASKS_PER_TEAM:
                print(f"COUNTER: {counter}      ")
                print(f"Seeding task {Task.objects.count()}")
                member_index = randint(0, team.team_members.count() - 1)
                author = team.team_members.all()[member_index]
                self.generate_task(author, team)
                counter += 1

        print("Task seeding complete.      ")

    def generate_user(self):
        """Generates random data for a user"""

        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        user = self.try_create_user(
            {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            })
        return user

    def generate_task(self, author, team, task_members_size=None):
        """Generates random data for a task"""

        name = self.faker.company()
        description = self.faker.last_name()
        end_date = datetime(2025, 12, 12, 23, 59)
        end_date = end_date.replace(tzinfo=timezone.utc)
        deadline = self.faker.future_datetime(end_date=end_date)
        deadline = deadline.replace(tzinfo=timezone.utc)
        # 1 to 5
        priority = randint(1, 5)

        if task_members_size is None:
            task_members_size = randint(10, (team.team_members.count() - 3))

        """Chooses random team members for the task"""
        members = team.team_members.all().order_by("?")[:task_members_size]

        self.try_create_task(
            {
                'name': name,
                'description': description,
                'deadline': deadline,
                'priority': priority,
                'author': author,
                'team': team,
                'members': members
            })

    def generate_team(self, admin):
        name = self.faker.company()
        team_size = randint(25, 50)
        members = sample(self.generated_users, team_size - 1)
        members.append(admin)
        # len(self.generated_users)

        team = self.try_create_team(
            {
                'name': name,
                'members': members,
                'admin': admin,
            })

        return team

    def try_create_user(self, data):
        try:
            user = self.create_user(data)
            return user
        except:
            pass

    def try_create_team(self, data):
        return self.create_team(data)
        # try:
        # self.create_team(data)
        # except:
        # pass

    def try_create_task(self, data):
        self.create_task(data)
        ##try:
        #  #self.create_task(data)
        # except:
        # pass

    def create_user(self, data):
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
        return user

    def create_team(self, data):
        team = Team(
            team_name=data['name'],
            team_admin=data['admin'],
        )
        team.save()
        team.team_members.set(data['members'])
        return team

    def create_task(self, data):
        task = Task(
            name=data['name'],
            description=data['description'],
            deadline=data['deadline'],
            priority=data['priority'],
            author=data['author'],
            team=data['team'],
        )

        task.save()
        task.members.set(data['members'])


def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()


def create_email(first_name, last_name):
    return first_name + '.' + last_name + '@example.org'
