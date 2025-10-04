Implementing the Blog's User Authentication System

This authentication system enables users to register, log in, log out, and manage their profile within the Django Blog project.

Project Structure
django_blog/
├── django_blog/
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── blog/
    ├── models.py
    ├── views.py
    ├── forms.py
    ├── urls.py
    ├── templates/
    │   └── blog/
    │       ├── base.html
    │       ├── login.html
    │       ├── register.html
    │       └── profile.html
    └── static/
        └── blog/css/
            ├── styles.css
            ├── login.css
            ├── register.css
            └── profile.css


CSRF Protection
Every form (login, register, profile) includes {% csrf_token %} to prevent Cross-Site Request Forgery (CSRF) attacks.

How it works
Registration:
Users fill the registration form (CustomUserCreationForm).
Upon successful submission, a user is created and automatically logged in.

Login / Logout:
Uses Django’s built-in LoginView and LogoutView.

Profile Management:
Only authenticated users can view/edit their details.

@login_required decorator ensures access control.
Profile updates are saved directly to the User model.


Testing - python manage.py runserver

