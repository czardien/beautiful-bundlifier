FROM python:3.8-alpine

RUN adduser --disabled-password --home /bundlifier bundlifier

COPY src/ /bundlifier/src
COPY lib/ /bundlifier/lib
ENV PYTHONPATH=/bundlifier

USER bundlifier
WORKDIR /bundlifier
CMD ["python", "src/bundlify.py", "data/notifications.csv", ">", "data/bundles.csv"]
