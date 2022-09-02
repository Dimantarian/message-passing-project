FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY . .
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT ["python", "./app/consumer.py"]