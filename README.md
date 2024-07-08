# Task Manager  
*An interactive task-management tool by Team Dingo*

View a populated web demo at https://sujannaik.pythonanywhere.com/ 
- Use the account username: '@Sujan' and password '@Sujan123' to avoid signing up. 

## Team members
- Omer Mohamed Osman Hussain
- Tanvir Singh Sahota 
- George Taylor
- Siqi Li 
- Sujan Naik

## What is this ?
> An intuitive and minimalistic web-application for team based project management developed using the [Django Web Framework](https://www.djangoproject.com/)

### Features
> Users can create accounts, log in, and manage their profiles.

> Users can form teams, and invite team members to their team.

> Each user can create tasks, assign tasks to other team members, and set due dates.

> Users provide a dashboard to view and manage assigned tasks, and team tasks.

> Enable users to search, order and filter tasks.  These could be based on name, completion status, priority, due date ranges, assigned developer, or team/project.

> Add a priority system for tasks, allowing users to assign priority levels and filter tasks based on priority.  Include automated reminders for high-priority tasks nearing their due dates.

> Time tracking feature for tasks, allowing users to log time spent on each task.  Provide summary reports of time spent on tasks over different periods.

> Notification system to alert users about task assignments and upcoming due dates.


## Developer instructions


### Project structure
The project is called `task_manager`.  It currently consists of a single app `tasks`.

### Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```

### Sources
The packages used by this application are specified in `requirements.txt`

