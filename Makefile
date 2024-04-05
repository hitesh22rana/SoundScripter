.PHONY: dependencies run-services-dev run-task-queue-dev run-api-dev run-frontend-dev format lint lint-fix check-requirements run clean

dependencies:
	@sh scripts/dependencies.sh

run-services-dev: check-requirements
	@sh scripts/services-dev.sh

run-task-queue-dev: dependencies
	@sh scripts/task-queue-dev.sh

run-api-dev: dependencies
	@sh scripts/api-dev.sh

run-frontend-dev:
	@sh scripts/frontend-dev.sh

format:
	@sh scripts/format.sh

lint:
	@sh scripts/lint.sh

lint-fix:
	@sh scripts/lint.sh --fix

check-requirements:
	@sh scripts/check-requirements.sh

run: clean check-requirements
	@sh scripts/build.sh

clean:
	@docker-compose -f docker-compose.yml down --remove-orphans