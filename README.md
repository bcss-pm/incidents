# Blockchain Incidents Database
## Background
Blockchain Incidents Database is a web application for recording the incidents pertaining to various blockchains types e.g. Ethereum, Bitcoin an other Altcoins blockchains.
The database model is based on [STIX](https://stixproject.github.io/) model, and in particular, its [Incident](http://stixproject.github.io/documentation/idioms/simple-incident/) data type model.

## Credits
This web application was based on a blogging application from https://github.com/dmaslov/flask-blog

## Development from GitHub source
Developers can get this repository to your local "incidents" directory via git pull:
```sh
$ mkdir incidents
$ cd incidents
$ git init
$ git config user.email "<youremail@somewhere.com>"
$ git config user.name "<github_username>"
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

## Running the Web App for the first time
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


## Running the Web App with populated databse
Once your mongodb is restored, the Blockchain Incidents Database would be populated.
Below is a sample screenshot.

![shell run4](screenshots/shell_run4.png?raw=true "Title")


## Backing-up and Restoring database
Check backup and restore MongoDB
https://stackoverflow.com/questions/31993168/cant-create-backup-mongodump-with-db-authentication-failed
https://stackoverflow.com/questions/28640281/restoring-single-collection-in-an-existing-mongodb#

### Backing up legacy database from AWS instance
The legacy mongo database is stored inside a docker container running in AWS EC2 instance.

Below are command line commands to explore the database inside docker:
```sh
ubuntu@ip-xxx:~$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
544587f50deb        blocktest_web       "gunicorn -b :5000 w…"   6 weeks ago         Up 6 weeks          0.0.0.0:5000->5000/tcp   blocktest_web_1
92259b90790a        mongo:3.6.1         "docker-entrypoint.s…"   5 months ago        Up 4 months         27017/tcp                blocktest_db_1


ubuntu@ip-xxx:~$ docker exec -it blocktest_db_1 /bin/bash

root@xxx:/# mongo admin -u tnoadmin -p '<password>'
MongoDB shell version v3.6.1
connecting to: mongodb://127.0.0.1:27017/admin
MongoDB server version: 3.6.1
Server has startup warnings:
2018-08-28T19:45:14.463+0000 I STORAGE  [initandlisten]
2018-08-28T19:45:14.463+0000 I STORAGE  [initandlisten] ** WARNING: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine
2018-08-28T19:45:14.463+0000 I STORAGE  [initandlisten] **          See http://dochub.mongodb.org/core/prodnotes-filesystem
2018-08-28T19:45:15.276+0000 I CONTROL  [initandlisten]
2018-08-28T19:45:15.276+0000 I CONTROL  [initandlisten] ** WARNING: /sys/kernel/mm/transparent_hugepage/enabled is 'always'.
2018-08-28T19:45:15.276+0000 I CONTROL  [initandlisten] **        We suggest setting it to 'never'
2018-08-28T19:45:15.276+0000 I CONTROL  [initandlisten]
2018-08-28T19:45:15.277+0000 I CONTROL  [initandlisten] ** WARNING: /sys/kernel/mm/transparent_hugepage/defrag is 'always'.
2018-08-28T19:45:15.277+0000 I CONTROL  [initandlisten] **        We suggest setting it to 'never'
2018-08-28T19:45:15.277+0000 I CONTROL  [initandlisten]
> show dbs
admin   0.000GB
blog    0.001GB
config  0.000GB
local   0.000GB
> use blog
switched to db blog
> show collections
posts
settings
users
> db.getCollection('posts').find({}).limit(20)
> exit
bye
root@xxx:/#
root@xxx:/# exit
exit
ubuntu@ip-xxx:~$
```

Here are the steps to backup mongo database `blog` inside docker:
```sh
ubuntu@ip-xxx:~$ docker exec -it blocktest_db_1 mongodump -d blog -u tnoadmin -p '<password>' --authenticationDatabase admin
ubuntu@ip-xxx:~$ pwd
/home/ubuntu
ubuntu@ip-xxx:~$ mkdir dumps
ubuntu@ip-xxx:~$ cd dumps
ubuntu@ip-xxx:~/dumps$ docker cp blocktest_db_1:dump/blog ./
ubuntu@ip-xxx:~/dumps$ ls -l
total 4
drwxr-xr-x 2 ubuntu ubuntu 4096 Dec 28 06:29 blog
```

### Backing up local mongo database
Typically you would want to backup your local development or test database before restoring from another dump.
Here are the steps:
```sh
sebtno@ubuntu:~/dumps/local$ sudo mongodump --db blog --out dump02
[sudo] password for sebtno: 
2019-01-09T22:31:13.749-0800	writing blog.users to 
2019-01-09T22:31:13.749-0800	writing blog.settings to 
2019-01-09T22:31:13.749-0800	writing blog.posts to 
2019-01-09T22:31:13.750-0800	done dumping blog.users (2 documents)
2019-01-09T22:31:13.750-0800	done dumping blog.settings (1 document)
2019-01-09T22:31:13.750-0800	done dumping blog.posts (1 document)
```

### Restoring a mongo database collection 'posts' from to local database
The mongo `blog` database has a `posts` collection that contains all the incidents.
Here are the steps to restore it into your local database, the example below restores from a directory called `aws/dumps`:
```sh
sebtno@ubuntu:~/dumps$ sudo mongorestore --db blog --collection posts aws/dumps/blog/posts.bson 
2019-01-09T22:37:05.861-0800	checking for collection data in aws/dumps/blog/posts.bson
2019-01-09T22:37:05.863-0800	reading metadata for blog.posts from aws/dumps/blog/posts.metadata.json
2019-01-09T22:37:05.864-0800	restoring blog.posts from aws/dumps/blog/posts.bson
2019-01-09T22:37:05.932-0800	restoring indexes for collection blog.posts from metadata
2019-01-09T22:37:05.933-0800	finished restoring blog.posts (110 documents)
2019-01-09T22:37:05.933-0800	done
```





