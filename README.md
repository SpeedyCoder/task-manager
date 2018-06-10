# Task Manager
This is small Django app for managing tasks of multiple users.
You can test the app here [here](https://michals-task-manager.herokuapp.com).
You can login using username `public` and password `qwerty123`.

Each user can see everyone's tasks and can add a task. They can also edit and 
delete their own tasks. Everyone can also mark a task as completed and the system
will record who did it.

There are currently no register or change password views for users, these actions can be
only done in the admin console.

## Implementation
The app uses Django's server side rendered templates for the UI and
[bulma](https://bulma.io) css framework fo styling. The app is fully responsive.

There is very little javascript used. In order to achieve this some of the endpoints
for editing and deleting tasks work using get. The same could be achieved using forms,
but that would pollute the html with lots of them. The next step would be to use more
javascript and change these to use appropriate http methods to make the app more RESTfull. 

To manage permissions the app uses [Django Rules](https://github.com/dfunckt/django-rules)
package and [Sentry](https://sentry.io) for error reporting.

## Development
The app uses `pipenv` to install dependencies and requires `python3.6`.
You can isntall pipenv using `pip install pipenv==2018.5.18`, then you can install 
all the dependencies using `pipenv install`. To activate the virtual environment
pipenv created run `pipenv shell`.

To run the app locally create a `.env` file in the root directory of the project
with the following contents.

```
SECRET_KEY=secret
DEPLOYED=False
DEBUG=True
DB_NAME=task-manager
DB_USER=root
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=15432
```

Then run `docker-compose up -d`, what will start a docker container with
postgres database. And you are ready to go, so you can run
```
python manage.py migrate
python manage.py collectstatic
```
to perform migrations and collect static files.

For this you will need docker compose installed. Alternatively, you can change
database settings in the `.env` file to point to a local instance of a postgres database.


## Deployment
The app is deployed on heroku. To deploy it as a new application you need to 
login to heroku, create a new app and then run the make command.
```
heroku login
heroku create
make
```
The make command will run the tests push the code to heroku and then run
the migrate script.