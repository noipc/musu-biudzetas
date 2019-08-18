FROM python:3.7

EXPOSE 8080

ENV PYTHONPROJECT 1
RUN mkdir /srv/musubiudzetas
WORKDIR /srv/musubiudzetas

COPY requiremnets.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG GIT_COMMIT
ENV GIT_COMMIT=${GIT_COMMIT}

CMD ["bin/sh", "config/start.sh"]