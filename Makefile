.PHONY: all

all: pull deploy

pull: 
	git pull

deploy: 
	docker stack deploy musu-biudzetas --compose-file docker-compose.yml