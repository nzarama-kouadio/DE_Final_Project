IMAGE_NAME := fraud_detection
DOCKER_ID_USER := skyea
PORT := 8000
AWS_USER_ID := 381492212823
AWS_REGION := us-east-2
LOCAL_DOMAIN := 127.0.0.1
AWS_DOMAIN := https://4fupzbqtbq.us-east-2.awsapprunner.com

# LOCAL
local: install lint format

install:
	python3 -m venv venv
	venv/bin/pip3 install --upgrade pip &&\
	venv/bin/pip3 install -r requirements.txt

format:	
	venv/bin/black **/*.py
#
# FIXME: fail nabval
#test:
#	venv/bin/python3 -m pytest -vv --cov=src.dotp

lint:
	venv/bin/ruff check **/*.py



# TEST API LOCAL
test_local_all:
	make test_local_health_check
	make test_local_predict_api

test_local_health_check:
	curl http://$(LOCAL_DOMAIN):$(PORT)/health

test_local_predict_api:
	curl -X POST http://$(LOCAL_DOMAIN):$(PORT)/predict \
   -H "Content-Type: application/json" \
   -d '{"transaction_id": "1", "amount": 100, "timestamp": "2024-12-09T12:00:00", "merchant": "Amazon"}'

test_local_predict_api_multiples:
	curl -X POST http://127.0.0.1:8000/predict \
	-H "Content-Type: application/json" \
	-d '[
	{
		"TransactionID": "1",
		"Timestamp": "2024-12-10T12:00:00",
		"MerchantID": "101",
		"Amount": 100.5,
		"CustomerID": "202",
		"TransactionAmount": 150.75,
		"AnomalyScore": 0.5,
		"Category": "Online",
		"CustomerAge": 35,
		"AccountBalance": 5000.25,
		"SuspiciousFlag": 0,
		"LastLogin": "2024-12-09T15:00:00"
	},
	{
		"TransactionID": "2",
		"Timestamp": "2024-12-10T13:00:00",
		"MerchantID": "102",
		"Amount": 200.75,
		"CustomerID": "203",
		"TransactionAmount": 250.50,
		"AnomalyScore": 0.7,
		"Category": "Travel",
		"CustomerAge": 40,
		"AccountBalance": 7000.00,
		"SuspiciousFlag": 1,
		"LastLogin": "2024-12-09T16:00:00"
	}
	]'

# DOCKER
docker_runb:
	make docker_down
	make docker_build
	make docker_run

docker_build:
	docker build -t $(IMAGE_NAME) .

docker_run:
	docker run -p  $(PORT):$(PORT) $(IMAGE_NAME)

docker_down:
	docker image prune -a
	docker container prune
	docker volume prune
	docker network prune

#docker_clean:
#	docker rmi $(IMAGE_NAME)

docker_push:
	docker login -u $(DOCKER_ID_USER)
	docker tag $(IMAGE_NAME) $(DOCKER_ID_USER)/$(IMAGE_NAME)
	docker push $(DOCKER_ID_USER)/$(IMAGE_NAME):latest



# AWS
# must install aws cli and run aws configure.
ecr_auth:
	aws --region $(AWS_REGION) ecr get-login-password | docker login --username AWS --password-stdin $(AWS_USER_ID).dkr.ecr.$(AWS_REGION).amazonaws.com

ecr_push:
	make docker_build
	docker tag $(IMAGE_NAME):latest $(AWS_USER_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(IMAGE_NAME):latest
	docker push $(AWS_USER_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(IMAGE_NAME):latest


#
## TEST API AWS
#test_aws_health_check:
#	curl https://$(AWS_DOMAIN):$(PORT)/health
#
#test_aws_log_api:
#	curl -X POST https://$(AWS_DOMAIN):$(PORT)/log \
#   -H "Content-Type: application/json" \
#   -d '{"transaction_id": "1", "amount": 100, "timestamp": "2024-12-09T12:00:00", "merchant": "Amazon"}'
#
#
test_aws_predict_api:
	curl -X POST https://$(AWS_DOMAIN):$(PORT)/predict \
  -H "Content-Type: application/json" \
  -d '{"transaction_id": "1", "amount": 100, "timestamp": "2024-12-09T12:00:00", "merchant": "Amazon"}'

#test_aws_all:
#	make test_aws_health_check
#	make test_aws_log_api
#	make test_aws_predict_api
