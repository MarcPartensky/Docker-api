shell:
	pipenv shell
run:
	uvicorn main:app --host 0.0.0.0 --port 8000
update:
	pipenv lock --pre --clear
	pipenv lock -r > requirements.txt
build: update
	docker build . -t marcpartensky/docker-api
dev: update
	docker-compose up -d --build docker-api
push: build
	docker push marcpartensky/docker-api


