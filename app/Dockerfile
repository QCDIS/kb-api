FROM python:3.11.5-alpine
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install gunicorn

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

RUN addgroup --system django
RUN adduser --system --ingroup django django
USER django

COPY --chown=django:django . .
CMD ["/bin/sh", "/app/entrypoint.sh"]
