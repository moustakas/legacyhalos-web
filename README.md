# legacyhalos-web
Website for the legacyhalos project(s).

add link if there are any good examples on anything here 
load.py & models explination...
Start by running the manage.py file and declaring the server domain (python manage.py runserver nyx.siena.edu:8888).
This will inturn look through the settings file. Everything in the settings page is loaded, and the BASE_URL is defined (along with the STATIC_URL). The templates directory holds the html setup for the webpages. base.html holds the general style while index.html holds the home webpage (talk about static directory). Each webpage created is created here, and extends to base.html. In our homepage, there is a link that appends list$ to the base url. All of the possible url paths are contained within the urls.py found inside legacyhalos_web. Appending the list$ to the url calls for the list function found in views.py. 
list function calls for list.html with the information we give it; pickle, paginator, filter.py
template tags thing
list.html loads everything loop that goes through each result and puts it on the table that is diplayed
redMaPPer ID contains href that changed the url to the base url + centrals$ 
in the urls.py, this then calls for the centrals function in views.py
takes the current index of the object that was pressed on, and takes the session created form the search result
returns the inforation we are telling it to and calls for the centrals.html page inside of templates
