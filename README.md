## Getting Started

### All developers

To start development:

```shell
$ mkdir observer && cd $_
$ git clone git@code.dev:observer/api.git
$ python3 -m venv VENV
$ cd api
$ source ../VENV/bin/activate
$ pip install -r requirement.txt 
```

### Backend developers only

To start development:

```shell
$ python manage.py runserver 0.0.0.0:8000
```
