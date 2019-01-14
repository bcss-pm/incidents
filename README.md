# Blockchain Incidents Database
## Background
Blockchain Incidents Database is a web application for recording the incidents pertaining to various blockchains types e.g. Ethereum, Bitcoin an other Altcoins blockchain.
This database model is based on [STIX](https://stixproject.github.io/) model, and in particular its [Incident](http://stixproject.github.io/documentation/idioms/simple-incident/) data type model.

## Credits
This web application was based on a blogging application from https://github.com/dmaslov/flask-blog

## Development from GitHub source
Developers can get this repository to your local "incidents" directory via git pull:
```sh
$ mkdir incidents
$ cd incidents
$ git init
$ git remote add origin https://github.com/bcss-pm/incidents.git
$ git fetch --all
$ git pull origin master
```
## Under the hood:
The technology stack used:
- [Python](http://python.org/)
- [Flask](http://flask.pocoo.org/)
- [MongoDB](http://www.mongodb.org/)
- [Bootstrap 3](http://getbootstrap.com/)
- [jQuery](http://jquery.com)
- [Lightbox 2](https://github.com/lokesh/lightbox2)
- [Markdown](http://daringfireball.net/projects/markdown/syntax)
- [Polymer](http://www.polymer-project.org)

## Minimum Requirements:
- Ubuntu 16.04
- Python 3.6.7
- mongoDB >= 2.2

## Install Python 3.6.x.
Follow the steps to install [python 3.6.x](http://ubuntuhandbook.org/index.php/2017/07/install-python-3-6-1-in-ubuntu-16-04-lts/)

If after installing python 3.6, your terminal shell would not start, follow these steps:
- Use xterm, running "gnome-terminal" from xterm shell will show the errors
- Backup /usr/bin/gnome-terminal
- Edit /usr/bin/gnome-terminal, update first line to 3.5, as in
`#!/usr/bin/python3.5`

## Install MongoDB
Follow the installation steps from [Install MongoDB Community Edition on Ubuntu](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)
**Be sure to follow the steps for Ubuntu 16.04** and not other versions.

After installation, `mongod` should be started as a service. Check:
`sudo service mongod status`
`sudo systemctl enable mongod`
`sudo service mongod restart`

If you cannot start mongod, refer to this [post](https://askubuntu.com/questions/921753/failed-to-start-mongod-service-unit-mongod-service-not-found)

Verify that your `mongo` command line client can connect to `mongod`.
```sh
$ mongo
MongoDB shell version v4.0.5
connecting to: mongodb://127.0.0.1:27017/?gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("5d7cf795-4b18-44d3-a356-6616ac6aedbc") }
MongoDB server version: 4.0.5
Server has startup warnings: 
2019-01-13T18:50:28.620-0800 I STORAGE  [initandlisten] 
2019-01-13T18:50:28.620-0800 I STORAGE  [initandlisten] ** WARNING: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine
2019-01-13T18:50:28.620-0800 I STORAGE  [initandlisten] **          See http://dochub.mongodb.org/core/prodnotes-filesystem
2019-01-13T18:50:35.698-0800 I CONTROL  [initandlisten] 
2019-01-13T18:50:35.699-0800 I CONTROL  [initandlisten] ** WARNING: Access control is not enabled for the database.
2019-01-13T18:50:35.699-0800 I CONTROL  [initandlisten] **          Read and write access to data and configuration is unrestricted.
2019-01-13T18:50:35.699-0800 I CONTROL  [initandlisten] 
---
```

## Install Python Packages used by this Web App

Go to incidents directory:
`cd incidents`

Set python virtual environment to use python 3.6.x:
`virtualenv -p python3 --no-site-packages ./env`

Activate python environment:
`source ./env/bin/activate`

Verify python version:
```sh
$ python -V
Python 3.6.7
```
Install this application's python packages
`pip install -r requirements.txt`

To leave python environment:
`deactivate`

## Running the Web App
By default, the Web App uses mongodb from localhost, refer to the file `incidents/config.py`
```
CONNECTION = pymongo.MongoClient(host = '127.0.0.1', 
                                  port = 27017)
```

Go to incidents directory:
`cd incidents`

Activate python environment:
`source ./env/bin/activate`

Run the server app:
(env)... $ python web.py 
![shell run1](screenshots/shell_run1.png?raw=true "Title")
![shell run2](screenshots/shell_run2.png?raw=true "Title")

Note that the server is running on `http://0.0.0.0:5000/`

Copy the URL `http://0.0.0.0:5000/` to your local web browser.

If this is first time you running the web app, your database is empty, you will also need to create a first login user with the details below:
![shell run3](screenshots/shell_run3.png?raw=true "Title")

## Backing-up and Restoring database

![shell run4](screenshots/shell_run4.png?raw=true "Title")








