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
	* `/lib/models/` which contains class models for our domain (e.g. notification, bundle)
	* `/lib/config.py` which contains configuration for our entrypoints,
	* `/lib/utils.py` which contains utils method e.g. argument parser,
	* `/lib/errors.py` which contains bundlify specific errors,
	* `/lib/hypervisor.py` which contains the bulk of the logic for coming with bundles from notifications defined as an abstract class with different implementations

* `/notebooks` contains all jupyter notebooks which help with visualisation and interpretation:
	* `/notebooks/notifications.ipynb` contains draft of early visualisation of our `notifications.csv` data sample,
	* `/notebooks/bundles.ipynb` contains visualisation and interpretation based on our `bundles.csv` results.

* `/tests` contains all unit tests written in pytest

* `/doc` contains all docs, currently [ADRs](https://github.com/npryce/adr-tools)

* `Makefile` defines targets to ease with development along with utils targets,
* `Dockerfile` defines our application docker image, based on `python:3.8-alpine` image; currently set with `CMD` to `python src/bundlifier.py data/notifications.csv > data/bundles.csv`
* `docker-entrypoint.sh` provides a convenient entrypoint to our application running the main python entrypoint and redirecting output to `data/bundles.csv`.
* `docker-compose.yml` provides a convenient entrypoint to our application based on our Dockerfile.

## Illustrated flow

Below is an illustrated flow of our main `bundlify.py` entrypoint.

* The bundlifier is updating the hypervisor with notifications as it is parsing the file,
* When a day's worth of observation has elapsed the Hypervisor computes and send bundles from notifications to stdout,

## Usage

Binaries for `git`, `make` and `python3` are needed. To use follow below steps:
* Git clone this repo anywhere then `cd <cloned_repo>`
* Install dependencies in a virtual environment e.g.:

```
python3 -m venv beautiful && source $(pwd)/beautiful/bin/activate && pip install -r dev-requirements.txt
```

### Run the tests

To run linting, type checking and unit tests with coverage:

```
make check
```

### Run the `bundlifier`

##### With python

To get all bundles on standard output run, with optional redirection:

```
PYTHONPATH=$(pwd) python src/bundlifier.py <path-to-notifications-csv> [ > <path-to-bundles.csv> ]
```

##### With docker-compose

Needs the extra dependency for `docker-compose`. To create the volume: `./data:/bundlifier/data/` and run the main entrypoint using `data/notifications.csv`:

```
make run
```

Find your results at: `/data/bundles.csv`

## Performances

For any compute-intense algorithms performances can be improved.

Multi-processing seems more fit to our use-case as a way to leverage a multi-core CPU; multi threaded or async programming are usually more fitted to improve IO bounds applications.
