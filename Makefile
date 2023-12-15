IMG = gradja-img
CONT = gradja
APP = Gradja

all:
	printf "Usage:\n\tmake build - builds the Docker image\n\tmake create - creates and runs the Docker container\n\tmake migrations - makes and applies the basic migration\n\tmake remove - removes the running Docker container\n\tmake restart - restarts the running Docker container\n"

build:
	docker build -t $(IMG) .

create:
	docker run --name=$(CONT) -p 8000:8000 -v ./$(APP):/usr/src/app -d $(IMG)

migrations:
	docker exec -d $(CONT) python manage.py makemigrations
	docker exec -d $(CONT) python manage.py migrate

remove:
	docker container rm $(CONT)

restart:
	docker stop $(CONT)
	docker start $(CONT)

.PHONY: all build create remove restart
.SILENT: all
