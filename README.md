# Task Manager
**By Team Dingo**

Provides an intuitive task management system which supports teams, intended for use within an organisation.
Built using the Django Web Framework, and a PostgreSQL database.

Deployed using Vercel and Supabase as a database [https://dingo-topaz.vercel.app/](https://dingo-topaz.vercel.app/).
![Home screen](https://github.com/user-attachments/assets/63656ef1-9120-46bc-aafa-2f9d4c24d627)
![Calendar view](https://github.com/user-attachments/assets/6b723be9-77a0-4226-b9c2-3c06e8db6292)
![Create task](https://github.com/user-attachments/assets/4ebd2064-5481-46b0-ad9e-2f306786b9f2)
![Create team](https://github.com/user-attachments/assets/aae72303-2186-42ac-a715-83929d40ffbc)
![Modify task](https://github.com/user-attachments/assets/9370e3b1-902e-46cc-a219-ba5f1b0c9fba)
![Task view](https://github.com/user-attachments/assets/8727f725-0523-4b31-8e1a-746addb3b40d)
![Tasks](https://github.com/user-attachments/assets/7319cd10-5d29-4383-ada5-2a60e87dc3dd)
![Team view](https://github.com/user-attachments/assets/6432d5cf-b320-478b-bc52-8b1214b32d31)

# Developer Instructions
## Installation instructions
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

*The above instructions should work in your version of the application.  If there are deviations, declare those here in bold.  Otherwise, remove this line.*

## Sources
The packages used by this application are specified in `requirements.txt`

*Declare are other sources here, and remove this line*


## Team members
The members of the team are:
- Omer Mohamed Osman Hussain
- Tanvir Singh Sahota 
- George Taylor
- Siqi Li 
- Sujan Naik
