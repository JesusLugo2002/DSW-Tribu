project := file_stem(justfile_dir())
venv-name := ".venv"
venv-path := join(justfile_dir(), venv-name)

# ==============================================================================
# DJANGO RECIPES
# ==============================================================================

# Launch development server
runserver: check-venv
    ./manage.py runserver

# Launch Django interactive shell
sh: check-venv
    ./manage.py shell

alias mm := makemigrations
# Make Django migrations
makemigrations: check-venv
    ./manage.py makemigrations
    
alias m := migrate
# Apply Django migrations
migrate: check-venv
    ./manage.py migrate

# Check if Django project is correct
check: check-venv
    ./manage.py check

# ==============================================================================
# VIRTUALENV RECIPES
# ==============================================================================

# Create a Python virtualenv
create-venv:
    #!/usr/bin/env bash
    if [ ! -d {{ venv-name }} ]
    then
        python -m venv {{ venv-name }} --prompt {{ project }}
        echo ✔ Created virtualenv at {{ venv-path }}
    fi

# Check if Python virtualenv is activated
[private]
[no-exit-message]
check-venv: create-venv
    #!/usr/bin/env bash
    if [ "$VIRTUAL_ENV" != "{{ venv-path }}" ]; then
        echo You must activate the right virtualenv!
        exit 1
    fi

# Install project requirements
install-reqs: check-venv
    pip install -r requirements.txt

# ==============================================================================
# DJANGO AUX RECIPES
# ==============================================================================

# Setup a Django project
setup: install-reqs && migrate create-su
    django-admin startproject main .

# Generate fake data and populate Django database
[private]
@gen-data *args: check-venv
    #!/usr/bin/env bash
    ./manage.py gen_data {{ args }}

# Dump fixtures
[private]
dump-data: gen-data
    ./manage.py dumpdata --format json --indent 2 auth -o fixtures/auth.json
    ./manage.py dumpdata --format json --indent 2 users -o fixtures/users.json
    ./manage.py dumpdata --format json --indent 2 echos -o fixtures/echos.json
    ./manage.py dumpdata --format json --indent 2 waves -o fixtures/waves.json

# Load fixtures into database
load-data: check-venv
    #!/usr/bin/env bash
    ./manage.py loaddata fixtures/auth.json
    ./manage.py loaddata fixtures/users.json
    ./manage.py loaddata fixtures/echos.json
    ./manage.py loaddata fixtures/waves.json
    echo --------------------------------
    ./manage.py shell -c '
    from django.contrib.auth.models import User
    print("Available users (with password 1234)\n")
    for user in User.objects.exclude(is_superuser=True):
        print(user)
    '

# Create a superuser (or update it if already exists)
create-su username="admin" password="admin" email="admin@example.com":
    #!/usr/bin/env bash
    ./manage.py shell -c '
    from django.contrib.auth.models import User
    user, _ = User.objects.get_or_create(username="{{ username }}")
    user.email = "{{ email }}"
    user.set_password("{{ password }}") 
    user.is_superuser = True
    user.is_staff = True
    user.save()
    ' 
    echo "✔ Created superuser → {{ username }}:{{ password }}"

# https://medium.com/@mustahibmajgaonkar/how-to-reset-django-migrations-6787b2a1e723
# https://stackoverflow.com/a/76300128
# Remove migrations and database. Reset DB artefacts.
[confirm("⚠️ All migrations and database will be removed. Continue? [yN]:")]
reset-db: && create-su
    #!/usr/bin/env bash
    find . -path "*/migrations/*.py" ! -path "./.venv/*" ! -name "__init__.py" -delete
    find . -path "*/migrations/*.pyc" ! -path "./.venv/*" -delete
    rm -f db.sqlite3
    ./manage.py makemigrations
    ./manage.py migrate
    echo
