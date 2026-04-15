ARGS ?=
MAIN_PACKAGE_CLI = uni-resource-api

.PHONY: install
install:
	uv sync --all-extras --all-packages

.PHONY: dev
dev:
	uv run $(MAIN_PACKAGE_CLI) --dev

.PHONY: prod
prod:
	uv run --no-sync $(MAIN_PACKAGE_CLI)

.PHONY: update
update:
	uv sync --all-extras --all-packages -U

.PHONY: clean
clean:
	rm -rf .venv && rm -rf dist/ && rm -rf build/ && rm -rf .ruff_cache/

.PHONY: test
test:
	uv run pytest tests -v

.PHONY: lint
lint:
	uv run ruff check . && uv run ty check . --ignore invalid-return-type

.PHONY: format
format:
	uv run ruff format .

.PHONY: docker-build
docker-build:
	docker compose build $(ARGS)

.PHONY: docker-run
docker-run:
	docker compose up -d $(ARGS)

.PHONY: docker-stop
docker-stop:
	docker compose down $(ARGS)

.PHONY: helm-lint
helm-lint:
	helm lint helm/mcp-template-python $(ARGS)

.PHONY: helm-install
helm-install:
	helm install mcp-template-python helm/mcp-template-python $(ARGS)

.PHONY: helm-upgrade
helm-upgrade:
	helm upgrade mcp-template-python helm/mcp-template-python $(ARGS)

.PHONY: helm-install-prod
helm-install-prod:
	helm install mcp-template-python helm/mcp-template-python -f values-production.yaml $(ARGS)

.PHONY: helm-upgrade-prod
helm-upgrade-prod:
	helm upgrade mcp-template-python helm/mcp-template-python -f values-production.yaml $(ARGS)

.PHONY: helm-uninstall
helm-uninstall:
	helm uninstall mcp-template-python $(ARGS)

.PHONY: rename
rename:
	uv run python tools/rename.py $(ARGS)
