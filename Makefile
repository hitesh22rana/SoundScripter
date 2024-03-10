.PHONY: dependencies run-task-queue-dev run-api-dev run-frontend-dev format lint lint-fix check-requirements run clean

dependencies:
	@chmod +x scripts/dependencies.sh
	@sh scripts/dependencies.sh

run-task-queue-dev: dependencies
	@chmod +x scripts/task-queue-dev.sh
	@sh scripts/task-queue-dev.sh

run-api-dev: dependencies
	@chmod +x scripts/api-dev.sh
	@sh scripts/api-dev.sh

run-frontend-dev:
	@chmod +x scripts/frontend-dev.sh
	@sh scripts/frontend-dev.sh

format:
	@chmod +x scripts/format.sh
	@sh scripts/format.sh

lint:
	@chmod +x scripts/lint.sh
	@sh scripts/lint.sh

lint-fix:
	@chmod +x scripts/lint.sh
	@sh scripts/lint.sh --fix

check-requirements:
	@chmod +x scripts/check-requirements.sh
	@sh scripts/check-requirements.sh

run: clean check-requirements
	@chmod +x scripts/build.sh
	@sh scripts/build.sh

clean:
	@docker-compose -f docker-compose.yml down --remove-orphans