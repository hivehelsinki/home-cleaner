.PHONY: start
start:
	@docker compose up --build

.PHONY: stop
stop:
	@docker compose down --remove-orphans

.PHONY: restart
restart: stop start

.PHONY: test
test:
	@docker compose run --rm --no-deps homecleaner pytest

.PHONY: lint
lint:
	@docker compose run --rm --no-deps homecleaner sh -c "ruff format . ; ruff check ."

.PHONY: update-dependencies
update-dependencies:
	@docker compose run --rm --no-deps homecleaner poetry lock
