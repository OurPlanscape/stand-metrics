.PHONY: build deploy test

PROJECT=planscape-23d66
APP_NAME=stand-metrics
ENV=dev
VERSION="$$(date '+%Y.%m.%d')-$$(git log --abbrev=10 --format=%h | head -1)"
APP=$(APP_NAME)-$(ENV)
DOCKER_REPO=planscape-$(APP_NAME)-$(ENV)
DOCKER_TAG=gcr.io/$(PROJECT)/$(DOCKER_REPO)/$(APP_NAME):$(VERSION)
REGION=us-central1

build:
	docker build -t $(DOCKER_TAG) .

deploy: build
	gcloud builds submit --tag $(DOCKER_TAG)
	gcloud run deploy $(APP) --image $(DOCKER_TAG) --platform managed --region $(REGION) --allow-unauthenticated

run:
	docker compose up

test: build
	./bin/run.sh uv run pytest .