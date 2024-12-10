IMAGE_NAME := fraud_detection
DOCKER_ID_USER := skyea
PORT := 8000

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

docker_build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
docker_run:
	docker run -p  $(PORT):$(PORT) $(IMAGE_NAME)

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

test_health_check:
	curl

test_log_api:
	curl -X POST http://127.0.0.1:$(PORT)/log \
   -H "Content-Type: application/json" \
   -d '{"transaction_id": "1", "amount": 100, "timestamp": "2024-12-09T12:00:00", "merchant": "Amazon"}'
#expect:
#   {
#     "status": "success",
#     "message": "Data ingested successfully.",
#     "data": {
#       "transaction_id": "1",
#       "amount": 100,
#       "timestamp": "2024-12-09T12:00:00",
#       "merchant": "Amazon"
#     }
#   }

test_predict_api:
	curl -X POST http://127.0.0.1:$(PORT)/predict \
   -H "Content-Type: application/json" \
   -d '{"transaction_id": "1", "amount": 100, "timestamp": "2024-12-09T12:00:00", "merchant": "Amazon"}'
#Expected response (example):
#   {
#     "prediction": "not fraud"
#   }
all: install lint test format
