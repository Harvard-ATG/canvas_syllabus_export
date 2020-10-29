[![Build Status](https://travis-ci.org/Harvard-ATG/canvas_syllabus_export.svg?branch=master)](https://travis-ci.org/Harvard-ATG/canvas_syllabus_export)

# Canvas Syllabus Export
Canvas LTI tool for exporting a customized course syllabus as a PDF 
# Installation Notes
 You must configure a secure file containing an oauth authentication key for running the project locally
```sh
# secure.py

SECURE_SETTINGS = {'oauthtoken': "sampleoauthtoken"}
```
 In order for the tool to work for any Canvas course, you must generate a master oauth token.

Ensure redis is running. For example, if using a Mac, do:
```
$ brew install redis
$ redis-server /usr/local/etc/redis.conf
```

From a separate Terminal window, `cd` into the project and activate the local virtual environment:
```
$ pipenv --python 3.6 install -r canvas_syllabus_export/requirements/local.txt
$ pipenv shell
```

Start the Django development server:
```
$ export DJANGO_SETTINGS_MODULE=canvas_syllabus_export.settings.local
$ python manage.py migrate
$ python manage.py runserver
```
