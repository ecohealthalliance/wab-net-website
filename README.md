This is the code base for the wabnet.eha.io website.
The website imports data from the wabnet EpiCollect5 survey.
It was built using the Django 2.0 framework.

# Setup

The following commands will install the dependencies, download the EC5 data, and start the app running on your local machine.

```bash
pip install -r requirements.pip
python manage.py makemigrations wabnet
python manage.py migrate
python manage.py createsuperuser
python manage.py import_from_epicollect
python manage.py runserver
```

# Regenerating Models from the EpiCollect5 survey

If the EpiCollect5 survey changes, you will need to update the Django models used to import its data.
The models can be automatically regenerated using the following command:
```
python manage.py generate_models wabnet
```
Updating the models will require migrating the old data from the old models into the new models. You can create a migration using the following command.
```
python manage.py makemigrations wabnet
```
To test the updates, run the migration and try importing new EpiCollect5 data.
```
python manage.py migrate
python manage.py import_from_epicollect wabnet.ec5_models
```
To deploy the updates to wabnet.eha.io, push the regenerated models to this repository along with the new migration in wabnet/migrations, then run the deployment script.

# Adapting this code base for different EpiCollect5 surveys

The model generation and data import features in ec5_tools are very generic and could be applied to other surveys with very little modification. I believe removing the country group creation code [here](https://github.com/ecohealthalliance/wab-net-website/blob/5efcdeb26667d245b47081ababa176fa77d06d99/ec5_tools/import_from_epicollect.py#L181) is the only change that would be required. The wabnet specific code (in the wabnet directory) could be useful for other projects as example code. Some sections could be used as a templates by looking for references to wabnet specific models and such as SiteData, BatData, SecondaryData, and TrappingEvent, and replacing them with models corresponding to the forms of the new survey. There are a few specific field references that will likely need to be modified or removed when using this repository as a template. For instances, the "Bat_family" properties of the BatData model are referenced a few places via [this function](https://github.com/ecohealthalliance/wab-net-website/blob/5efcdeb26667d245b47081ababa176fa77d06d99/wabnet/views.py#L28),  and if that model is changed to something else, like HedgehogData, the properties referenced will also need to change.
