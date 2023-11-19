FROM python:latest

RUN apt update \
	&& apt install \
	-y --no-install-recommends \
	postgresql-client

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
