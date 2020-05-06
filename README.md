# beautiful-notifications-bundler

This repository hosts codebase and instrumentation for an application to push notifications given an event stream.

## Features

This code features instrumentation for bundling notifications around a ranker algorithm which predicts readiness of a bundle given observed notifications.

Process is happening in real-time as the notifications are streamed.

### Codebase

Below is an overview of the codebase:

* `/data` contains all data, including:
	* `notifications.csv` the input file of observed notifications we're processing,
	* `users.csv` an one-off job output to extract our user base,
	* `bundles.csv` the output file containing the bundles,
	* `stats.csv` an additional file containing statistics and metrics about the ranker performance.

* `/src` contains all entrypoints, including:
	* `bundler.py` the main entrypoint which outputs bundles to stdout given a filepath to notifications,
	* `read-users.py` a secondary entrypoint which outputs user ids given a filepath to notifications.

* `/lib` contains all additional codebase, including:
	* `/lib/models/` which contains class models for our domain (e.g. notification, bundle, user, managers)
	* `/lib/config.py` which contains configuration for our entrypoints.

* `/tests` contains all unit tests written in pytest

* `/doc` contains all docs, currently [ADRs](https://github.com/npryce/adr-tools)

* `Dockerfile` defines our application docker image, based on `python:3.8-alpine` image; currently set with `CMD` to `python src/bundler.py data/notifications.csv > data/bundles.csv`
* `docker-compose.yml` provides a convenient entrypoint to our application based on our Dockerfile.

### Ranker

Given a pending bundle the ranker returns a readiness score between 0 and 1 given a set of variables:
* Elapsed time delta between current timestamp and the bundle's first timestamp,
* Elapsed time delta between current timestamp and the bundle's lasttimestamp,
* Elapsed time delta between bundle's last timestamp and the bundle's first timestamp,
* Current number of tours in the bundle,
* Current number of notifications received by the user on the current day,

## Illustrated flow

Below is an illustrated flow of our main `bundler.py` entrypoint.

* The bundle manager is holding an internal state of all pending bundles,
* A notification is seen by the bundle manager,
* From the new notification the bundle manager will gover all pending bundles and extract the variables:
	* `var_elapsed_since_first_ts` as the elapsed time delta between current timestamp and the bundle's first timestamp,
	* `var_elapsed_since_last_ts` as the elapsed time delta between current timestamp and the bundle's last timestamp,
	* `var_elapsed_span` as the elapsed time delta between the bundle's last timestamp and the bundle's first timestamp,
	* `var_current_tours` as the current bundle's tours count,
	* `var_user_notifications_count` as the user's number of notifications received for the current day.
* Variables are fed into a ranker and a readiness score will be returned,
* All pending bundles with a readiness score higher than a hyper parameter threshold will be moved into a ready state and further be sent

## Usage

Binaries for `git`, `docker` and `docker-compose` are needed. To use follow the below steps:

* Git clone this repository anywhere; then `cd <cloned_repo>`
* Run: `docker-compose up`,
	* This will generate bundles and stats from notifications by running the command:

```
python src/bundler.py data/notifications.csv > data/bundles.csv && \
python src/stats.py data/bundles.csv > data/stats.csv
```

## Limitations

The main limitation we find about this challenge is that we're essentially asked to make informed decisions based on future data. e.g. send a notification at 10am to a given user on a given day given the total number of notifications that day.

If not we're essentially asked to mock a producer / consumer of messages for which I cannot see an easy way to do.
