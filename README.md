# beautiful-notifications-bundler

This repository hosts codebase and instrumentation for an application to push notifications given an event stream.

## I am confused about this product

Any time I am thinking of this product as a service sitting in a backend I am invariably finding it to be either a long lived deploy that either exposes and HTTP API and is being posted events or polls a message queue; or a short term job that processes every minute for example a batch of data.

It is in any case an application that has to reason on a scale as close to real time as possible. It is crucial that this application takes time into account when generating notifications for obvious reasons and it's also part of the requirements.

Hence emulating this context given the current challenge would require crafting components emulating a system responsible both for producing and consuming events and mocking time going by; indeed the data spans about 3 months worth of events.

We're are not going for this type of solution and will instead produce an application that reasons on the entire dataset and tries to minimise an error function to be defined; even though the interest of such an application in a production environment is not obvious.
