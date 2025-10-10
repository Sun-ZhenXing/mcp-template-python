.PHONY: i dev prod build clean update lint docker-build docker-run helm-install helm-upgrade helm-uninstall helm-lint rename

i:
	uv sync --all-extras --all-packages $(filter-out i,$(MAKECMDGOALS))

dev:
	uv run --no-sync python -c "__import__('mcp_template_python.__main__').__main__.dev()" $(filter-out dev,$(MAKECMDGOALS)) || echo shutdown

prod:
	uv run --no-sync python -c "__import__('mcp_template_python.__main__').__main__.main()" $(filter-out prod,$(MAKECMDGOALS))

build:
	uv build $(filter-out build,$(MAKECMDGOALS))

clean:
	rm -rf .venv .ruff_cache dist/ build/ *.egg-info $(filter-out clean,$(MAKECMDGOALS))

update:
	uv sync --all-extras --all-packages -U $(filter-out update,$(MAKECMDGOALS))

lint:
	uv run ruff check . $(filter-out lint,$(MAKECMDGOALS))

docker-build:
	docker compose build $(filter-out docker-build,$(MAKECMDGOALS))

docker-run:
	docker compose up -d $(filter-out docker-run,$(MAKECMDGOALS))

helm-lint:
	helm lint helm/mcp-template-python

helm-install:
	helm install mcp-template-python helm/mcp-template-python

helm-upgrade:
	helm upgrade mcp-template-python helm/mcp-template-python

helm-install-prod:
	helm install mcp-template-python helm/mcp-template-python -f values-production.yaml

helm-upgrade-prod:
	helm upgrade mcp-template-python helm/mcp-template-python -f values-production.yaml

helm-uninstall:
	helm uninstall mcp-template-python

rename:
	uv run python tools/rename.py $(filter-out rename,$(MAKECMDGOALS))

%:
	@:
