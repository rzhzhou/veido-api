### Get Started

```shell
mkdir observer && cd $_
git clone git@192.168.1.101:observer/app.git
pip install -r requirements.txt
python manage.py runserver 0.0.0.0:8000
```


### Project Structure

<pre>
observer/                  - Main Project Folder
  apps/                    - Contains all django apps
  settings/                - Contains production and development settings files
  prefixed_storage.py      - For storages plugin, if need be
  ...
static/                    - Contains all static files
templates/                 - Contains all the dynamic template files
tests/                     - Contains all the testing files
tmp/                       - Contains local development environment files (e.g. database files, log files, etc.)
createapp.py               - Run 'python createapp.py [APP_NAME]' to create an app following the file structure
manage.py                  - Standard django management file
runserver.py               - Run 'python runserver.py' to run a local test server. Does relevant checks and updates db first.
requirements.txt           - Contains all pip requirements
</pre>