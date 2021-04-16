# Login Example
 this is a login example using flask
## Requirements
 - flask
 - Flask-SQLAlchemy
 - psycopg2-binary
 - flask-admin
 - flask-login
 - Flask-Migrate
## Running the server
 you can run the app for testing purposes using [docker](https://docs.docker.com/engine/install/)
```
$ docker build -t <image-name> .
$ docker run -dp 8000:8000 -v <google-creds-path>:/tmp/google_creds.json <image-name>
```
you can view the app in your browser at ``` localhost:8000```
### Admin
you can view admin page in your browser at ``` localhost:8000/admin```
## Migration
 running database migrations in the production enviroment
```
@TODO
```