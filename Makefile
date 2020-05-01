# check targets
check-lint:
	flake8

check-type:
	mypy . --ignore-missing-imports

# aliases
checks: check-lint check-type
check: checks
c: checks
