SHELL = /bin/bash
.SHELLFLAGS = -e -c

.PHONY: deploy
.DEFAULT_GOAL := deploy

COMMIT_HASH := $(shell git log -n 1 --pretty=format:"%H" .)

$(info COMMIT_HASH: ${COMMIT_HASH})


test:
	@python manage.py test --keepdb

deploy: test
	@git push heroku --force
	@heroku config:set COMMIT_HASH="${COMMIT_HASH}"
