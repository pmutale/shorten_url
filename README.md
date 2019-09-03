# API: SHORTEN A URL

## Requirements
Python 3.5.2+

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
http://localhost:7070/urls/ui/
```

Your OpenAPI definition lives here:

```
http://localhost:7070/openapi.json
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
