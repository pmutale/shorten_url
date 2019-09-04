# API: SHORTEN A URL

## Requirements
Python 3.5.2+

## App Online, Lazy?

To test live server

 visit [Google App Engine AppSpot](https://shorten-url-usecase.appspot.com/urls/ui/)

## Usage
To run the server, please execute the following from the root directory:

```
$ git clone git@github.com:pmutale/shorten-url.git
$ cd shorten-url/
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ python3 -m openapi_server
```

and open your browser to here:

```
http://localhost:8080/urls/ui/
```

To run unit tests:

```
$ python3 -m unittest test_shorten_url_controllers.TestDefaultController 
```

To launch the integration tests, use tox:
```
$ sudo pip install tox
$ tox
```

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
$ docker build -t openapi_server .

# starting up a container
$ docker run -p 8080:8080 openapi_server
```
