#!/bin/sh

alias run="uvicorn main:app --host 0.0.0.0 --port 8000"

install() {
	python -m pip install pipenv
	pipenv install
}

run
