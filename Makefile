ACCOUNT=gaf3
IMAGE=relations-mysql
INSTALL=python:3.8.5-alpine3.12
VERSION?=0.1.0
DEBUG_PORT=5678
TTY=$(shell if tty -s; then echo "-it"; fi)
VOLUMES=-v ${PWD}/lib:/opt/service/lib \
		-v ${PWD}/test:/opt/service/test \
		-v ${PWD}/.pylintrc:/opt/service/.pylintrc \
		-v ${PWD}/setup.py:/opt/service/setup.py
ENVIRONMENT=-e PYTHONDONTWRITEBYTECODE=1 \
			-e PYTHONUNBUFFERED=1 \
			-e test="python -m unittest -v" \
			-e debug="python -m ptvsd --host 0.0.0.0 --port 5678 --wait -m unittest -v"
.PHONY: build shell debug test lint setup tag untag

build:
	docker build . -t $(ACCOUNT)/$(IMAGE):$(VERSION)

shell:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) -p 127.0.0.1:$(DEBUG_PORT):5678 $(ACCOUNT)/$(IMAGE):$(VERSION) sh

debug:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) -p 127.0.0.1:$(DEBUG_PORT):5678 $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "python -m ptvsd --host 0.0.0.0 --port 5678 --wait -m unittest discover -v test"

test:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "coverage run -m unittest discover -v test && coverage report -m --include 'lib/*.py'"

lint:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "pylint --rcfile=.pylintrc lib/"

setup:
	docker run $(TTY) $(VOLUMES) $(INSTALL) sh -c "cp -r /opt/service /opt/install && cd /opt/install/ && \
	apk update && apk add git && \
	pip install git+https://github.com/gaf3/python-relations.git@8b5c841#egg=relations && \
	pip install git+https://github.com/gaf3/python-relations-sql.git@705a7e0#egg=relations-sql && \
	python setup.py install && \
	python -m relations_mysql.sql && \
	python -m relations_mysql.expression && \
	python -m relations_mysql.criterion && \
	python -m relations_mysql.criteria && \
	python -m relations_mysql.clause && \
	python -m relations_mysql.query && \
	python -m relations_mysql.ddl && \
	python -m relations_mysql.column && \
	python -m relations_mysql.index && \
	python -m relations_mysql.table"

tag:
	-git tag -a $(VERSION) -m "Version $(VERSION)"
	git push origin --tags

untag:
	-git tag -d $(VERSION)
	git push origin ":refs/tags/$(VERSION)"
