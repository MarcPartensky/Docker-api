shell:
	pipenv shell
run:
	uvicorn main:app --host 0.0.0.0 --port 8000
build:
	docker build . -t marcpartensky/docker-api
dev: build
	docker run -d marcpartensky/docker-api

