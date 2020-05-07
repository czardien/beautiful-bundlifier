# check targets
check-lint:
	flake8

check-type:
	mypy . --ignore-missing-imports

check-tests:
	pytest --cov

# utils target
jupyter:
	PYTHONPATH=$(shell pwd) jupyter-notebook

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.cache' -exec rm -fr {} +
	find . -name '.pytest_cache' -exec rm -fr {} +
	find . -name '.mypy_cache' -exec rm -fr {} +

# aliases
checks: check-lint check-type check-tests
check: checks
c: checks
