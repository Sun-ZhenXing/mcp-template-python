.PHONY: i dev prod build clean update lint docker-build docker-run helm-install helm-upgrade helm-uninstall helm-lint rename

args := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))

i:
	uv sync --all-extras --all-packages $(args)

dev:
	uv run --no-sync python -c "__import__('mcp_template_python.__main__').__main__.dev()" $(args) || echo shutdown

prod:
	uv run --no-sync python -c "__import__('mcp_template_python.__main__').__main__.main()" $(args)

build:
	uv build $(args)

clean:
	rm -rf .venv .ruff_cache dist/ build/ *.egg-info $(args)

update:
	uv sync --all-extras --all-packages -U $(args)

lint:
	uv run ruff check . $(args)

docker-build:
	docker compose build $(args)

docker-run:
	docker compose up -d $(args)

helm-lint:
	helm lint helm/mcp-template-python $(args)

helm-install:
	helm install mcp-template-python helm/mcp-template-python $(args)

helm-upgrade:
	helm upgrade mcp-template-python helm/mcp-template-python $(args)

helm-install-prod:
	helm install mcp-template-python helm/mcp-template-python -f values-production.yaml $(args)

helm-upgrade-prod:
	helm upgrade mcp-template-python helm/mcp-template-python -f values-production.yaml $(args)

helm-uninstall:
	helm uninstall mcp-template-python $(args)

rename:
	uv run python tools/rename.py $(args)

%:
	@true
