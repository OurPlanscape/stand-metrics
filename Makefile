.PHONY: build deploy test

PROJECT=planscape-23d66
APP_NAME=stand-metrics
ENV=dev
VERSION="$$(date '+%Y.%m.%d')-$$(git log --abbrev=10 --format=%h | head -1)"
APP=$(APP_NAME)-$(ENV)
DOCKER_REPO=planscape-$(APP_NAME)-$(ENV)
DOCKER_TAG=us-central1-docker.pkg.dev/$(PROJECT)/$(DOCKER_REPO)/$(APP_NAME):$(VERSION)
DOCKER_LATEST=us-central1-docker.pkg.dev/$(PROJECT)/$(DOCKER_REPO)/$(APP_NAME):latest
REGION=us-central1

build:
	docker build -t $(DOCKER_TAG) .

deploy: build
	gcloud builds submit --tag $(DOCKER_TAG) --tag $(DOCKER_TAG)
	gcloud run deploy $(APP) --image $(DOCKER_TAG) --platform managed --region $(REGION)

run:
	docker compose up

test: build
	./bin/run.sh uv run pytest .