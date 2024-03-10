.PHONY: check-requirements run clean

check-requirements:
	@chmod +x scripts/check-requirements.sh
	@sh scripts/check-requirements.sh

run: clean check-requirements
	@chmod +x scripts/build.sh
	@sh scripts/build.sh

clean:
	@docker-compose -f docker-compose.yml down --remove-orphans