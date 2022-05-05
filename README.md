Group 18 ESD Group UWEFlix Project 2022
===============================

By Arjun Binning, Benedict Ramage-Mangles, Matthew Hill, Michael Duncan, Ross Williams

The UWEFlix website is intended to replace the existing paper system.

Install instructions - Linux
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
Clone from GitHub:
```
git clone git@github.com:bean64/Group-18-ESD-2022.git
```
Set up a Virtual Environment:
```
py -3 -m venv .venv
.venv\scripts\activate
```
... and Install modules and components:
``` 
cd Group-18-ESD-2022\UWEFlix_django\
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
... then open a web browser at http://localhost:8000.

**Supporting Documents:**
All supporting documents and diagrams can be found in the documents folder.
