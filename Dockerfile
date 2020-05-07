FROM python:3.8-alpine

RUN adduser --disabled-password --home /bundlifier bundlifier

COPY data/notifications.csv /bundlifier/data/notifications.csv
COPY docker-entrypoint.sh/ /bundlifier/docker-entrypoint.sh
RUN chmod +x /bundlifier/docker-entrypoint.sh

COPY src/ /bundlifier/src
COPY lib/ /bundlifier/lib

ENV PYTHONPATH=/bundlifier

USER bundlifier
WORKDIR /bundlifier
CMD ["sh", "-c", "./docker-entrypoint.sh"]
