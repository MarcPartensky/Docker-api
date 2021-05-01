#!/bin/sh

alias run="uvicorn main:app --reload"

install() {
	python -m pip install pipenv
	pipenv install
}
