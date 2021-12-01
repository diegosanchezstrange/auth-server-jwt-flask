# JWT Auth
## Intro
This is just a small project for me to learn a couple of concepts regarding:

* The Flask Framework
* JWT
* Restfull API's

I will also use this app in other projects if I need an authentication server that way i don't have to implement authentication on each project I do.

## How to run
Firs we install all the libraries listed on the requierement.txt:
```
pip install -r requirements.txt
```
Then we have to declare the FLASK_ENV and the FLASK_APP varibles like so:
```
export FLASK_ENV=development
export FLASK_APP=src/server
```
Now we can just run the following command to start the app:
```
flask run
```
