# Django Rest Framework JWT-Authentication Template

This is a template for a Django Rest Framework project with JWT-Authentication.
It is readily equipped with a user model and user authentication endpoints. Some other
technologies used in this template are:

- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Django Rest Framework Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [Django Rest Framework CORS Headers](https://pypi.org/project/django-cors-headers/)
- [PostgreSQL](https://www.postgresql.org/)

My goal for this template is to provide a starting point for future projects that require
user authentication. I hope that this template will save me time in the future and I hope
that it will be useful to others as well.

If you have any suggestions or improvements, please feel free to open an issue or submit a pull request.

## Setup

### Clone the repository

```bash
git clone https://github.com/brandon-kong/django-rest-jwt-auth-template.git
```

### Create a virtual environment

```bash
python3 -m venv .venv
```

Once the virtual environment is created, activate it.

On Windows:

```bash
.venv\Scripts\activate.bat
```

On Linux or MacOS:
```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a .env file

If you are using a database other than SQLite, you will need to install the appropriate database driver and add the database connection information to the .env file.

In this template, I am using PostgreSQL as the database. If you want to opt for a different database, you will need to install the appropriate database driver and add the database connection information to the .env file.

Create a .env file in the root directory of the project (/core) and add the following variables:

```bash
DB_HOST='...'
DB_PORT='...'
DB_USER='...'
DB_PASSWORD='...'
DB_NAME='...'
```

**Note:** If you are using SQLite, you do not need to add the above variables to the .env file,
but you will need to edit the DATABASES variable in core/settings.py to the following:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Run migrations

```bash
python manage.py migrate
```

### Create a superuser

```bash
python manage.py createsuperuser
```

### Run the server

```bash
python manage.py runserver
```

## Endpoints

### Register

```bash
POST /users/create/email/

{
    "email": "email",
    "password": "password"
}

Creates a user with the given email and password.
```

```bash
POST /users/create/phone/

{
    "phone": "phone",
}

Creates a user with the given phone number. A 6-digit verification code will be sent to the phone number using Twilio.
```

### Login

```bash

