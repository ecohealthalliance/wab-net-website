# Setup

```bash
pip install -r requirements.pip
python manage.py makemigrations wabnet
python manage.py migrate
python manage.py createsuperuser
python import_from_epicollect.py
python manage.py runserver
```

# Regenerate Models from EpiCollect5 survey

```
python generate_models.py
python manage.py makemigrations wabnet
python manage.py migrate
python import_from_epicollect.py
```
