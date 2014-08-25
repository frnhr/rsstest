# rsstest


RSS word counter, because we can

## What

A test project that counts words in RSS feeds.

Features:
 * management command that loads the feeds and counts words
 * customized Django-rest-framework API
 * web interface (a.k.a. the console)
 * simple django-admin
 

## Setup


### Create yourself a virtualenv

Your computer says: "pleeease"


### Get the code

Either go a clone:

    git clone git@github.com:frnhr/rsstest.git
    
Or download it manually.


### Install requirements

    $ cd /your/local/path/rsstest
    $ pip install -r requirements.txt
    
This will install Django an a bunch of other packages.


### Bring the database up to speed

Two commands:

    $ python manage.py syncdb --noinput
    $ python manage.py migrate
    
Don't worry, a "demo:demo" account will get created with the migrations. It's a superuser ;)

Also, you'll get two test feeds, for quick start. No entries however, just feed URLs.


### Run the server

    $ python manage.py runserver

Now go to http://localhost:8000 and make sure the site works.


### Run the RSS parser

    $ python manage.py processrss
    
That's all folks!


## Todo

 * some test maybe?
 * clean up API field names (those underscres, and change "url" to "link")
 
