.PHONY: dependencies-backend dependencies-frontend lint-backend lint-frontend format-backend format-frontend run-task-queue-dev run-api-dev run-client-dev run-services-dev check-requirements run clean

dependencies-backend:
	@sh scripts/backend/dependencies.sh

dependencies-frontend:
	@sh scripts/frontend/dependencies.sh

lint-backend:
	@sh scripts/backend/lint.sh

lint-frontend:
	@sh scripts/frontend/lint.sh

format-backend:
	@sh scripts/backend/format.sh

format-frontend:
	@sh scripts/frontend/format.sh

run-task-queue-dev: lint-backend format-backend dependencies-backend
	@sh scripts/backend/task-queue-dev.sh

run-api-dev: lint-backend format-backend dependencies-backend
	@sh scripts/backend/api-dev.sh

run-client-dev: lint-frontend format-frontend dependencies-frontend
	@sh scripts/frontend/run-dev.sh

run-services-dev:
	@sh scripts/services-dev.sh

check-requirements:
	@sh scripts/check-requirements.sh

run: clean check-requirements
	@sh scripts/run.sh

clean:
	@docker-compose -f docker-compose.yml down --remove-orphans