IMAGE_NAME := fraud_detection
DOCKER_ID_USER := skyea

install:
	python3 -m venv venv
	venv/bin/pip3 install --upgrade pip &&\
	venv/bin/pip3 install -r requirements.txt

format:	
	venv/bin/black src/*.py

test:
	venv/bin/python3 -m pytest -vv --cov=src.dotp

lint:
	venv/bin/ruff check src/*.py

build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	docker run -p  8000:80 $(IMAGE_NAME)

# Remove the Docker image
clean:
	docker rmi $(IMAGE_NAME)

image_show:
	docker images

container_show:
	docker ps

push:
	docker login
	docker tag $(IMAGE_NAME) $(DOCKER_ID_USER)/$(IMAGE_NAME)
	docker push $(DOCKER_ID_USER)/$(IMAGE_NAME):latest

login:
	docker login -u ${DOCKER_ID_USER}

all: install lint test format

