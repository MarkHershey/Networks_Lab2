REMOVE = sudo rm -rvf

all:
	docker-compose build --no-cache
clean:
	$(REMOVE) local_db
	$(REMOVE) logs
	$(REMOVE) src/local_db
	$(REMOVE) src/__pycache__
	$(REMOVE) src/**/__pycache__
	$(REMOVE) mongo/data