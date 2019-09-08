.PHONY: all

all: pull deploy

pull: git pull

deploy: docker stack deploy musubiudzetas --compose-file docker-compose.yml