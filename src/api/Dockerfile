FROM python:3.12.6-bookworm

WORKDIR /api

ENV APP_NAME = "OpenHeart-Core-WebAPI"
ENV FASTAPI_HOST = 0.0.0.0
ENV MYSQL_PORT = 3306
ENV FAST_API_PORT = 8000

COPY Pipfile Pipfile
COPY src src

RUN pip install pipenv
RUN pipenv install

EXPOSE 8000
CMD ["fastapi", "run"]
