Group 18 ESD group project 2022
===============================

By Arjun Binning, Benedict Ramage-Mangles, Matthew Hill, Michael Duncan, Ross Williams

The UWEFlix website is intended to replace the existing paper system.

Install instrutions - Linux
-----
```
$ git clone git@github.com:bean64/Group-18-ESD-2022.git
$ cd Group-18-ESD-2022/UWEFlix_django/
$ pip install requirements.txt
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver
```
then open a web browser at http://localhost:8000

Install instructions - Windows
-----
set up a venv
```
py -3 -m venv .venv
.venv\scripts\activate
```
and install
```
git clone git@github.com:bean64/Group-18-ESD-2022.git
cd Group-18-ESD-2022/UWEFlix_django/
python -m pip install --upgrade pip
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
then open a web browser at http://localhost:8000
