# legacyhalos-web
Website for legacyhalos project(s).

## Creating a Django Project
To start creating a project, after django is installed, run this command:

    >>> django-admin startproject mysite (replace mysite with the name of the website you want to create)

This will create a folder hierarchy that resembles this:

* mysite/
  * manage.py
  * mysite/
    * __init__.py
    * settings.py
    * urls.py
    * wsgi.py


manage.py is the location that the server is executed from when testing the functionality.  
settings.py contains the general settings for the entire website.  
urls.py contains the paths to the site's known pages via url.  
wsgi.py is how the server host interacts with the website created.

## Our File Hierarchy and Dependencies
![alt text](https://docs.google.com/drawings/d/e/2PACX-1vRLhdgoZOds5w9cVZbfOI25HLPWE3lf5-u6W_XQV3KOqfM8crgQpBGdiFFyqCfh_Ryh_CWbQmKawKJR/pub?w=1337&h=691 "Project Structure Diagram")

## Creating the Database from a File
When creating a database for the website to pull from, you must first make the migrations. Making the migrations lets django know of any object specifications that were added or updated.  
A data file is loaded through load.py, which has the specifications on the file format (ours is a .fits file) and creates the database table for the model (in our case Centrals model), then populates the table with the specified fields.  
The order of the commands are:

    >>> rm db.sqlite3
    >>> python manage.py makemigrations legacyhalos_web
    >>> python manage.py migrate
    >>> python load.py

This sequence of commands only have to happen when the user wants to populate or update the database.
The load.py puts all of the objects created within the query set (saved as db.sqlite3). For more information, go to: [Django Query Reference](https://docs.djangoproject.com/en/2.0/topics/db/queries/)

## Setting-Up Website

### Central Model and Filter
Our website uses only one model, called Centrals. This model was created in legacyhalos_web/models.py as a table in the database with the fields listed stored as columns. It is populated by load.py with individual Central objects as rows. See [documentation on models](https://docs.djangoproject.com/en/2.0/topics/db/models/)

filter.py is used to put a filter on the Centrals model, in order to select rows of the Centrals table that fit the given criteria. The filter is applied to a queryset, which is created from the Centrals model. We can then use the filter to create a form in our html page that connects to the database. We used a Django NumberFilter for several fields to allow filtering for min and max values on any of those fields. See more here: [information on Filters](https://django-filter.readthedocs.io/en/master/ref/filters.html)

### Templates

Django uses templates within html code in order to execute code to dynamically generate the webpage html. Templates are denoted by {{ with code inside }} or {% with other code inside %}. Read more on: [Django Template Language](https://docs.djangoproject.com/en/2.0/ref/templates/language/) or [Built in and Custom Templates](https://docs.djangoproject.com/en/2.0/topics/templates/)  
We have created our template tags within centrals/templatetags/my_templatetag.py because Django knows that custom template tags will be located within a folder called templatetags. They were used in order to create and call our own python functions from within a line of html. Tags must be registered and loaded in order to use them: see [Custom template tags](https://docs.djangoproject.com/en/2.1/howto/custom-template-tags/)

### The Webpages

The templates directory at the project root holds the html setup for the webpages in the files base.html, index.html, list.html, and centrals.html. base.html holds the general style we reuse on each individual page. At the top of each page's html we use templates to extend base.html; load static files; and/or load our custom templatetags depending on what that page will use. 

All of the possible url paths are contained within the urls.py found inside legacyhalos_web. Appending the list$ to the base url calls for the list function found in views.py, and the same is true for index and centrals
list function calls for list.html with the information we give it; pickle, paginator,

index.html is the homepage content.(talk about static directory). In our homepage, there is a link that appends list$ to the base url. 

list.html loads everything loop that goes through each result and puts it on the table that is diplayed,  
redMaPPer ID contains href that changed the url to the base url + centrals$,  
in the urls.py, this then calls for the centrals function in views.py,  
takes the current index of the object that was pressed on, and takes the session created form the search result,  
returns the information we are telling it to and calls for the centrals.html page inside of templates

Each html page has a corresponding function within views.py which returns an html response, in our case index() list() and centrals() render the corresponding html page, and can pass values to that page within the return statement. Any extra logic specific to that page goes within the page's view function, such as pagination, serialization, and dealing with sessions.

## Running the Server

Start by running the manage.py file and declaring the server domain

    >>> python manage.py runserver webuser@galaxy.siena.edu

This will inturn look through the settings file. Everything in the settings page is loaded, and the BASE_URL is defined (along with the STATIC_URL). 



## Deploying the Application

During testing, debug in settings.py can be set to true, but in production mode it should be set to false, as any error messages could leak important information

### Setting up Apache

