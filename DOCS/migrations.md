# Migration information

## Adding new columns from EpiCollect
1. EpiCollect (this walks you through migration changes, so you don't need to modify the model code)
   1. make a hotfix branch on GitHub
   1. test on staging server before changing production server
   1. docker exec -it *wabnet_container_id* /bin/bash
   1. cd /wab-net-website
   1. git checkout master
   1. git pull
   1. git checkout *new_hotfix_branch_name*
   1. /venv/bin/python3 manage.py import_from_epicollect wabnet.ec5_models (this will break at new fields)
   1. /venv/bin/python3 manage.py generate_models wabnet
   1. /venv/bin/python3 manage.py makemigrations wabnet
   1. /venv/bin/python3 manage.py migrate
   1. /venv/bin/python3 manage.py import_from_epicollect wabnet.ec5_models
   1. git commit -a
   1. git push
   1. make pull request for hotfix branch and merge with master branch

## Adding new columns from AirTable
These steps should be tested in a development Git branch on a staging EC2 instance.

1. add variables for new columns to `wabnet/airtable_models.py`
1. `docker exec -it *wabnet_container_id* /bin/bash`
1. `cd wab-net-website`
1. `git checkout master`
1. `git pull`
1. `git checkout *your_dev_branch*`
1. `/venv/bin/python3 manage.py makemigrations wabnet`
1. `/venv/bin/python3 manage.py migrate`
1. if new columns contain files:
  1. add verbose and short variable names for those columns to lists in views.py
  1. add conditions for those variables to `templates/bat.html`
1. test by changing cron sync command time to a few minutes from current time
1. `git commit -m 'added new AT cols to data model' -a`
1. `git push`
1. make pull request for hotfix branch and merge with master branch

If you get a 500 error or a message that the site is down for maintenance and there's no sync running there's a problem with something you added.
You can check the logs by either going to /wabnet-compose and running `docker-compose logs` or by running `docker logs wabnet` and `docker logs wabnet-apache` from anywhere.

## reverting to an earlier migration
1. docker exec -it *wabnet_container_id* /bin/bash
1. cd /wab-net-website
1. delete the migration files you don't want from /wab-net-website/wabnet/migrations
1. then migrate to the latest file in that directory with: /venv/bin/python3 migrate wabnet *migration_file_name*

**NOTE:** You'll also need to remove all migration files after the migration(s) you want to revert.

## show all migrations
1. docker exec -it *wabnet_container_id* /bin/bash
1. cd /wab-net-website
1. /venv/bin/python3 manage.py showmigrations
