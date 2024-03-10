.PHONY: check-requirements run clean

check-requirements:
	@sh scripts/check-requirements.sh

run: clean check-requirements
	@sh scripts/build.sh

clean:
	@docker-compose -f docker-compose.yml down --remove-orphans