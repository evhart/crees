---
title: "Installation"
permalink: /api/installation/
---


The CREES services can be run inside or outside a [docker](https://docker.com/) container. By default the API will be accessible on port 80 with the documentation accessible on *'/comrades'* and the services exposed under *'/comrades/events'*.

### Requirements
The CREES services need the following libraries installed and Python 2:
* python 2 (tested on 2.7.10)
* [tensorflow (0.12)](https://www.tensorflow.org/versions/r0.12/get_started/os_setup)
* numpy
* flask
* flask-restplus

 You will need to install the [GIT Large File Storage](https://git-lfs.github.com/) extenssion in order to be able to clone the repository since the CRESS models are larger than 150MB.
 {: .notice--success}

### Starting the Server
For starting the CREES server you can simply run the *crees_server.py* file:

```sh
python crees_server.py --help
```

```
Usage: crees_server.py [options]

Options:
  -h, --help            show this help message and exit
  -p PORT, --port=PORT  the API port for serving CREES [default: 80]
  -n API_NAMESPACE, --namespace=API_NAMESPACE
                        the API namespace for CREES [default: comrades]
```


You can also pass the arguments using environment variables:
```
CREES_PORT=8080 CREES_NAMESPACE='crees' python crees_server.py
```

### Docker Usage
You can also run CREES using [docker](https://docker.com/) . First, you need to build the docker image.
```sh
docker build -t evhart/comrades_crees:latest .
```

The CREES service will be automatically started when you start a CREES container. You can run the container interactively (-i):
```sh
docker run -i -p 80:80 --name crees_server evhart/comrades_crees:latest
```
Or as a daemon (-d):
```sh
docker run -d -p 80:80 --name crees_server evhart/comrades_crees:latest
```

You can also pass environment variables to the docker container for modifying the default namespace and port:
```
docker run -i -p 80:8080 --name crees_server  \
-e CREES_PORT=8080 \
-e CREES_NAMESPACE='crees' \
evhart/comrades_crees:latest
```

