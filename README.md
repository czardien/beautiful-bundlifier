# beautiful-bundlifier

This repository hosts codebase and instrumentation for an application to push bundles given a notification stream.

## Features

This code features instrumentation for bundling notifications around a ranker algorithm which predicts readiness of a bundle given observed notifications.

### Codebase

Below is an overview of the codebase:

* `/data` contains all data, including:
	* `notifications.csv` the input file of observed notifications we're processing,
	* `bundles.csv` the output file containing the bundles,

* `/src` contains all entrypoints, including:
	* `bundlify.py` the main entrypoint which outputs bundles to stdout given a filepath to notifications,

* `/lib` contains all additional codebase, including:
	* `/lib/models/` which contains class models for our domain (e.g. notification, bundle, user, managers)
	* `/lib/config.py` which contains configuration for our entrypoints,
	* `/lib/utils.py` which contains utils method e.g. argument parser,
	* `/lib/errors.py` which contains bundlify specific errors,
	* `/lib/hypervisor.py` which contains the bulk of the logic for coming with bundles from notifications defined as an abstract class with different implementations

* `/tests` contains all unit tests written in pytest

* `/doc` contains all docs, currently [ADRs](https://github.com/npryce/adr-tools)

* `Makefile` defines targets to ease with development along with utils targets,
* `Dockerfile` defines our application docker image, based on `python:3.8-alpine` image; currently set with `CMD` to `python src/bundlifier.py data/notifications.csv > data/bundles.csv`
* `docker-compose.yml` provides a convenient entrypoint to our application based on our Dockerfile.

### Ranker

###### TODO: expand on the ranker

## Illustrated flow

Below is an illustrated flow of our main `bundlify.py` entrypoint.

* The bundlifier is updating the hypervisor with notifications as it is parsing the file,
* When a day's worth of observation has elapsed the Hypervisor computes and send bundles from notifications,

## Usage

### python

Binaries for `python3` are needed. To use follow below steps:
* Git clone this repo anywhere; `cd <cloned>`
* This project doesn't use dependencies so you're good to go without a virtual environment,
* To get all bundles on standard output run, with optional redirection:

```
python src/bundlifier.py <path-to-notifications-csv> [ > <path-to-bundles.csv> ]
```

* To get all users on standard output run, with optional redirection:

```
python src/get_users.py.py <path-to-notifications-csv> [ > <path-to-users-csv> ]
```

* To get performance stats on bundles run, with optional redirection:

```
python src/get_stats.py <path-to-bundles-csv> [ > <path-to-stats-csv> ]
```

### docker-compose

Binaries for `git`, `docker` and `docker-compose` are needed. To use follow the below steps:

* Git clone this repository anywhere; then `cd <cloned_repo>`
* Run: `docker-compose up`,
	* This will generate bundles and stats from notifications by running the command:

```
python src/bundlifier.py data/notifications.csv > data/bundles.csv
```

## Limitations

The main limitation we find about this challenge is that we're essentially asked to make informed decisions based on future data. e.g. send a notification at 10am to a given user on a given day given the total number of notifications that day.

If not we're essentially asked to mock a producer / consumer of messages for which I cannot see an easy way to do.
