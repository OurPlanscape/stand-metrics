.PHONY: build deploy test

PROJECT=planscape-23d66
APP=stand-metrics-test
TAG=gcr.io/$(PROJECT)/$(APP)
REGION=us-central1

build:
	docker build -t $(TAG) .

deploy: build
	gcloud builds submit --tag $(TAG)
	gcloud run deploy $(APP) --image $(TAG) --platform managed --region $(REGION) --allow-unauthenticated