FROM python:3.12-slim
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ARG APP_DIR=/usr/note_book
ENV PATH $APP_DIR:$PATH
WORKDIR $APP_DIR
COPY . ./

ENV VIRTUAL_ENV "${APP_DIR}/venv"
RUN python3.12 -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH"

RUN pip3.12 install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root --only main


RUN apt-get update && \
    apt-get install -y curl \
    traceroute \
    mc \
    tcpdump \
    telnet \
    dnsutils \
    iputils-ping \
    && apt-get clean autoclean && apt-get autoremove --yes && rm -rf /var/lib/{apt,dpkg,cache,log}

ENV APP_HOST="0.0.0.0"
ENV APP_PORT=7001
CMD ["python", "note_book/app.py"]
EXPOSE ${APP_PORT}