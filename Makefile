build:
	python -m virtualenv venv
	venv/bin/pip install -r requirements.txt

run:
	venv/bin/python -u mailer.py

test:
	venv/bin/python setup.py test
	venv/bin/python -m flake8 . --exclude=venv

test-with-coverage:
	venv/bin/python -m coverage run setup.py test
	venv/bin/python -m coverage xml --omit="venv/*","tests/*","setup.py"
	venv/bin/python -m flake8 . --exclude=venv

clean:
	rm -rf .Python build dist venv* *.egg-info *.egg .coverage htmlcov coverage.* .cache
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

.PHONY: build test clean run
