# Introduction
**Django-based** Handwritten Text Recognition Project with functionalities of **Annotation** and **Validation**.

# Folder structure
```
README.md
app/  | ------ app/ | ------ settings.py
      |             | ______ urls.py
      |	            | ______ views.py
      |
      |
      | ______ bin/
      |
      | ______ manage.py
      |
      | ______ requirements.txt
      |
      | ______ static/ | ----- admin/
      |	               | _____ annotation/
      |                | _____ css/
      |                | _____ image/
      |                | _____ other_image/
      |                | _____ sample_image/
      |
      | ______ templates/ | ----- base.html
	 		  | _____ index.html
		          | _____ validation.html
			  | _____ check_data.html
```

# How to start the project
First, switch you place to `/app`.

## Packages
You need to install the packages required for the project with following command.
```
pip3 install -r requirements
```

## Database
We used **MongoDB** as our database engine in this project, make sure you install mongodb API for python before you start up the project.
```
# add mongoengine to installed_apps
INSTALLED_APPS = [
	'xxx',
	'mongoengine'
]

# update mongodb databases
MONGODB_DATABASES = {
    "default": {
        'ENGINE' : 'django_mongodb_engine',
        #'ENGINE': 'djongo',
        "name": "examples",
        "host": '127.0.0.1',
        "tz_aware": True,
    },
}
```
# Switch into shell for mongodb and create database

## Install MongoDB on your machine
First, follow the instructions in the [Install MongoDB Community Edition on Ubuntu](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/).  
After installation, start up mongo daemon with the following command
```
sudo systemctl start mongod
```
Then, use command `mongo` to get into the shell of mongodb.  
Create database for our project with following command (Otherwise, annotation won't be saved into database).  
```
use examples
```
This command would help us switch into the database of `examples`.  

Then, create a role with user and password with  following command:
```
db.createUser({
    user: 'theresa', 
    pwd: 'theresa', 
    roles: ["readWrite"]
    })
```
You can find the corresponding setting in `setting.py`:
```
from mongoengine import connect
connect(db = 'examples', 
        host ='127.0.0.1',
        username = 'theresa',
        password = 'theresa'
)
```
Then we would store data in collection of `annotation` and `validation` with following command:  
```
db.createCollection('annotation')
db.createCollection('validation')
```
Now everything in database is ready. Run server up and enjoy it in next section.  

## Some other useful commands
Learning following commands would help you get information from mongo shell.  
To show the collections:  
```
show collections
```
To see all the data
```
db.<collection-name>.find()
```
To remove the data from collection
```
db.<collection-name>.remove({})
```

## Run up the server
```
python3 manage.py runserver 0.0.0.0:<port-you-want-to-open>
```
Attention! The port you chose need to follow the security policy for ec2 instance (We build up the server on ec2 instance).

# Static asset
We stored static asset in `static/` folder just as shown in `Folder structure`.  

## S3 Bucket
Only for the images used for annotation, we stored them in **S3 Bucket** and acees it from EC2 instance. To access S3 bucket, we use the python3 libraries of `boto3` and `django-storages`. Then go to adjust the content of `app/settings.py`:  
```
# add storages to installed_apps
INSTALLED_APPS = [
	'xxx',
	'storages'
]

# S3 configuration
AWS_ACCESS_KEY_ID = '<find-you-key-id>'
AWS_SECRET_ACCESS_KEY = '<find-your-access-key>'
AWS_STORAGE_BUCKET_NAME = '<bucket-name>'

# storages configuration
AWS_S3_FILE_OVERWRITE = True
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# change STATIC_URL
STATIC_URL = 'https://%s/' % ( '<bucket-name>.s3.amazonaws.com' )
````
Now, you can try to access images with `{% static '<path>' %}`.

Attention! You need to set up security policy for your s3 bucket.
