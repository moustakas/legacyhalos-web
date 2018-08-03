# legacyhalos-web
Website for legacyhalos project(s).

## Creating a Django Project
To start creating a project, after django is installed, run this command:
django-admin startproject mysite

## Creating the Database from a File
When creating a database for the website to pull from, you must first make the migrations. Making the migrations lets django know of any object specifications that were added or updated. 
The manner in which a file is loaded is through the load.py file. load.py has the specifications on the file format (our file is a .fits file) and creates the objects (in our case Central objects), then stores them in the database that it created.
The order of the commands are:
1. rm db.sqlite3
2. python manage.py makemigrations legacyhalos_web
3. python manage.py migrate
4. python load.py

This sequence of commands only have to happen when the user wants to populate or update the database.

add link if there are any good examples on anything here 

## Central Objects
The object type that is being used are called Centrals. This object type was created in legacyhalos_web/models.py.
models explination...

Start by running the manage.py file and declaring the server domain (python manage.py runserver nyx.siena.edu:8888).
This will inturn look through the settings file. Everything in the settings page is loaded, and the BASE_URL is defined (along with the STATIC_URL). The templates directory holds the html setup for the webpages. base.html holds the general style while index.html holds the home webpage (talk about static directory). Each webpage created is created here, and extends to base.html. In our homepage, there is a link that appends list$ to the base url. All of the possible url paths are contained within the urls.py found inside legacyhalos_web. Appending the list$ to the url calls for the list function found in views.py. 
list function calls for list.html with the information we give it; pickle, paginator, filter.py

template tags thing

list.html loads everything loop that goes through each result and puts it on the table that is diplayed

redMaPPer ID contains href that changed the url to the base url + centrals$ 

in the urls.py, this then calls for the centrals function in views.py

takes the current index of the object that was pressed on, and takes the session created form the search result

returns the inforation we are telling it to and calls for the centrals.html page inside of templates
