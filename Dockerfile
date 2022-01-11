FROM python:3.9

COPY . /app
WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y
RUN apt-get install curl -y
RUN pip install -U pip
RUN pip install -r requirements.txt

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "curl", "-f", "localhost:80" ]

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
