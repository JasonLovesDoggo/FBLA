# Stavros

A CMS for schools

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy stavros

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Setup

1. Clone the repo
2. Create a virtual environment with `python3 -m virtualenv venv`
3. Activate the virtual environment with `source venv/bin/activate` on Linux or `.\venv\Scripts\activate` on Windows
4. Install the requirements with `pip install -r requirements/local.txt`
5. Run the migrations with `python manage.py migrate`
6. Create a superuser with `python manage.py createsuperuser`
7. Run the server with `python manage.py runserver`

## Deployment

The following details how to deploy this application.

### Docker

See detailed [Django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
