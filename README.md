
callWrapper Front-End 

This is the web-app using Django for the customer service AI
agent for customers to upload their documents to.

Uses django's framework and native authentication along with admin panel already existing. Signals are used to create profiles in a MongoDB database to keep track of the back-end usage.

Content is uploaded again to a MongoDB cluster/database for the back-end to access easily. 

This service does not use djongo, but simple pymongo CRUD.

Check the requirements.txt file for all the requirements.

Very simple framework, the default one that is used for django.

Data flow for those who don't know:

manage.py --> urls --> views --> html/css/javascript

Only one app is used. No models made. Only one addition to the admin panel: adding  a phone number to every user.
