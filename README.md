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

## Features
- User model with email and phone number fields
- User model manager
- User model serializer
- OAuth2 authentication
- User authentication endpoints
- JWT-Authentication
- Blacklisting of Refresh Tokens
- Twilio integration for phone number verification
- Email link verification

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
DB_NAME="postgres"
DB_USER="postgres"
DB_PASS="postgres"
DB_HOST="localhost"
DB_PORT="5432"

# SMTP settings

SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="user"
SMTP_PASS="email"
SMTP_TLS=True
SMTP_SSL=False

# SMS settings

SEND_SMS_TEXT=True
SMS_CODE_LENGTH=6

SEND_SMS_CALL=True
# Twilio settings

TWILIO_ACCOUNT_SID="ssid"
TWILIO_AUTH_TOKEN="auth"
TWILIO_PHONE_NUMBER="number"

# Social auth settings

GOOGLE_CLIENT_ID="client"
GOOGLE_CLIENT_SECRET="secret"
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
POST /users/register/email/

{
    "email": "email",
    "password": "password",
    "first_name": "first_name",
    "last_name": "last_name"
}

Creates a user with the given email and password.
```

```bash
POST /users/register/phone/

{
    "phone": "phone",
    "email": "email",
    "password": "password",
    "first_name": "first_name",
    "last_name": "last_name",

    "token": "sms_token"
}

Creates a user with the given phone number and password. The phone number is verified using the 6-digit verification code sent to the phone number.
```


### Login

```bash
POST /users/verify/email/
    
{
    "email": "email",
    "password": "password"
}

Returns a JSON Web Token Refresh and Access that can be used to authenticate requests.
```

```bash
POST /users/verify/phone/

{
    "phone": "phone",
    "token": "token"
}
```

### Refresh Access Token

```bash
POST /users/token/refresh/

{
    "refresh": "refresh"
}

Returns a new Access Token.
```

### Verify Phone Number

```bash
POST /users/otp/verify/

{
    "phone": "phone",
    "token": "token"
}

Verifies the phone number using the 6-digit verification code sent to the phone number. This endpoint is protected by the IsAuthenticated permission class, so the user must have a valid Authorization header with a valid Access Token.
```

### Send Phone OTP

```bash
POST /users/otp/send/

{
    "phone": "phone",
}

Sends a 6-digit verification code to the phone number.
```


### Verify Phone OTP

```bash
POST /users/otp/verify/

{
    "phone": "phone",
    "token": "token"
}

Verifies the phone number using the 6-digit verification code sent to the phone number.
```

### Verify Email Address

```bash
POST /users/email/verify/?token=token/

{
    "token": "token",
}

Verifies the email address with the token in the GET request. The token is sent to the user's email address when the user is created. The token is a UUID for added security. This endpoint is not protected by any permission classes because the user will click on the link in the email to verify their email address.
```

### Email exists

```bash
POST /users/email/exists/

{
    "email": "email",
}

Returns True if the email exists in the database, otherwise returns False.
```

### Phone exists

```bash
POST /users/phone/exists/

{
    "phone": "phone",
}

Returns True if the phone number exists in the database, otherwise returns False.
```


## License

[MIT](/LICENSE)

## Acknowledgements

- [Django Rest Framework Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)


## Contact

Brandon Kong
- [LinkedIn](https://www.linkedin.com/in/brandon-kong0/)
- [Github](https://www.github.com/brandon-kong)
- [Email](mailto:kongbrandon0@gmail.com)
