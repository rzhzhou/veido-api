## Getting Started

### All developers

To start development:

```shell
mkdir observer && cd $_
git clone git@192.168.1.101:observer/app.git
pip install -r requirement.txt
```

### Backend developers only

To start development:

```shell
python manage.py runserver 0.0.0.0:8000
```

### Front-end developers only

To start development:

```shell
npm i -g gulp
npm i -d
gulp serve
```

To start build:

```shell
gulp build
```

## Project Structure

```
observer/                  - Main Project Folder
  apps/                    - Contains all django apps
  settings/                - Contains production and development settings files
  ...
static/                    - Contains all static files
  build/                   - Contains all static build files
  js/                      - Contains all js source files
  less/                    - Contains all less source files
templates/                 - Contains all the dynamic template files
manage.py                  - Standard django management file
requirement.txt           - Contains all pip requirements
```