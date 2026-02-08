ARGS ?=

.PHONY: i dev prod build clean update lint docker-build docker-run helm-install helm-upgrade helm-uninstall helm-lint rename

i:
	uv sync --all-extras --all-packages $(ARGS)

dev:
	uv run --no-sync python -c "__import__('mcp_template_python.__main__').__main__.dev()" $(ARGS) || echo shutdown

prod:
	uv run --no-sync python -c "__import__('mcp_template_python.__main__').__main__.main()" $(ARGS)

build:
	uv build $(ARGS)

clean:
	rm -rf .venv .ruff_cache dist/ build/ *.egg-info $(ARGS)

update:
	uv sync --all-extras --all-packages -U $(ARGS)

lint:
	uv run ruff check . && uv run ty check .

docker-build:
	docker compose build $(ARGS)

docker-run:
	docker compose up -d $(ARGS)

helm-lint:
	helm lint helm/mcp-template-python $(ARGS)

helm-install:
	helm install mcp-template-python helm/mcp-template-python $(ARGS)

helm-upgrade:
	helm upgrade mcp-template-python helm/mcp-template-python $(ARGS)

helm-install-prod:
	helm install mcp-template-python helm/mcp-template-python -f values-production.yaml $(ARGS)

helm-upgrade-prod:
	helm upgrade mcp-template-python helm/mcp-template-python -f values-production.yaml $(ARGS)

helm-uninstall:
	helm uninstall mcp-template-python $(ARGS)

rename:
	uv run python tools/rename.py $(ARGS)

%:
	@true
