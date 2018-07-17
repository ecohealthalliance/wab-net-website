# Setup

```bash
pip install -r requirements.pip
python manage.py makemigrations wabnet
python manage.py migrate
python manage.py createsuperuser
python manage.py import_from_epicollect
python manage.py runserver
```

# Regenerate Models from EpiCollect5 survey

```
python manage.py generate_models wabnet
python manage.py makemigrations wabnet
python manage.py migrate
python manage.py import_from_epicollect
```
