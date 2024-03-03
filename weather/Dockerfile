FROM debian:12-slim AS build-env

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip setuptools wheel pipenv

COPY ./src/Pipfile .
COPY ./src/Pipfile.lock .
RUN /venv/bin/pipenv requirements > requirements.txt 
RUN /venv/bin/pip install -r requirements.txt

FROM gcr.io/distroless/python3-debian12

WORKDIR /app
COPY ./src /app
COPY --from=build-env /venv /venv

ENTRYPOINT ["/venv/bin/python"]
CMD ["index.py"]