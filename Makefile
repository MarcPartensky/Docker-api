shell:
	pipenv shell
run:
	uvicorn main:app --host 0.0.0.0 --port 8000
dev:
	uvicorn main:app --host 127.0.0.1 --port 8000 --reload
update:
	pipenv lock --pre --clear
	pipenv lock -r > requirements.txt
build: update
	docker build . -t marcpartensky/docker-api
builddev: update
	docker-compose up -d --build docker-api
push: build
	docker push marcpartensky/docker-api


