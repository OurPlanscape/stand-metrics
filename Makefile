.PHONY: build deploy test

PROJECT=planscape-23d66
APP=stand-metrics-test
TAG=gcr.io/$(PROJECT)/$(APP)
REGION=us-central1

build:
	docker build -t $(TAG) .

# not really used as GCP has it's own trigger
deploy: build
	gcloud builds submit --tag $(TAG)
	gcloud run deploy $(APP) --image $(TAG) --platform managed --region $(REGION) --allow-unauthenticated

run:
	docker compose up

test: build
	./bin/run.sh uv run pytest .