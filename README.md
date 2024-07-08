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

### Media
## The Home Screen
![Home screen](https://github.com/Sujan-Naik/dingo/assets/125016948/0f86c58b-35d5-4d30-b152-3161ae01aed1)

## The tasks view
![Tasks](https://github.com/Sujan-Naik/dingo/assets/125016948/36c2b4a7-5022-46fa-ba6a-a1cba7b11ca1)

## Viewing an individual task
![Task view](https://github.com/Sujan-Naik/dingo/assets/125016948/3b8e4fe8-520a-40bc-8ed0-9d3fb839fab2)

## Modifying a task
![Modify task](https://github.com/Sujan-Naik/dingo/assets/125016948/190fe861-1ef2-48b4-a2c7-e13b6ef06846)

## Creating a task
![Create task](https://github.com/Sujan-Naik/dingo/assets/125016948/bb48ad94-0094-4d88-bc6b-2a38c0f6a6f1)

## Viewing a team
![Team view](https://github.com/Sujan-Naik/dingo/assets/125016948/2abd5617-9dec-45a6-83f3-4d91b6c32315)

## Creating a team
![Create team](https://github.com/Sujan-Naik/dingo/assets/125016948/d6af72df-1003-401c-85d0-b17827113583)

## A calendar view
![Calendar view](https://github.com/Sujan-Naik/dingo/assets/125016948/0e1f91cf-805f-475e-8361-f6fa7c2b7ae0)






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

