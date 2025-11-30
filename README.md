<div align=justify>

# TRIBU

A compact and lightweight social network called TRIBU that replace posts with **Echos** and the comments with **Waves**. Similar to Twitter app.

This project was created as homework for Server-side development subject of my Web Application Development formation. 

## :wrench: Technologies

- `pip`
- `Python`
- `Django`
- `HTML`
- `CSS`
- `Bootstrap`
- `JavaScript`
- `JQuery`

## :star: Features

1. **Create an account** and start to upload *Echos*, a lightweight and compact version of a *Tweet*.
2. **Search other users** and answer their *Echos* using the comments system, *Waves*.
3. **Manage your personal profile** with your own bio, profile avatar and keep counting the echos and waves in our tribu.

## :book: What I learned

### Authentication in Django

I learned how Django manage the users authentication and profiles creation, and limit the access to the app using the `@login_required` annotation, redirecting to the login form.

### Organize a more extensive project in different apps

The creation of different apps inside the Django project helps me to understand and keep the code more readable and scalable, following the single-responsability principle.

### Use Django forms to receive data and build models

I learned how use the forms classes provided by Django to speed up the process of create instances in the application, saving the information directly in models using POST requests.

## :eyes: Demostration



## :question: How run this app?

1. Download the latest release or clone the repository.
2. Inside the terminal, install the required dependencies with `apt-get install python3.12 python3-venv python3-pip`.
3. Then, use `python3 -m venv .venv --prompt tribu` to create the virtual environment.
4. Execute `source .venv/bin/activate` to enter in the environment and use `pip install -r requirements.txt` to install all the dependencies.
5. `./manage.py check && ./manage.py migrate` to prepare the app (also `./manage.py createsuperuser` to access into the administrator panel).
6. Execute `./manage.py runserver` to init the app, then access with [localhost:8000](http://localhost:8000).
7. Use `ctrl+c` to power off the server and `deactivate` to leave the virtual environment.

</div>