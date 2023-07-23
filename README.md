# Django Rest Framework JWT-Authentication Template

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
POST /api/auth/register/
```