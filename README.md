# hr-web
This is Django based web project for data labeling, validation and verification.



## web architecture

under `app/app`:

1. `urls.py` : to set our web URL and connect to the `views.py`
2. `views.py` : to implement our function in the web and render to our `html` file
3. `setting.py` : to define all of application and connect to our database
4. `modules.py` : to connect to our collection and define the data format

under `app/templates`:

1. `base.html` : the page for setting navigation bar(link to annotation/validation page soical media share button)
2. `index.html` : the page for user to annotate image
3. `validation.html` : the page for user to validate image
