.PHONY: i dev prod build clean update

i:
	uv sync --all-extras --all-packages $(filter-out i,$(MAKECMDGOALS))

dev:
	uv run --no-sync python -c "__import__('mcp_template_python.__main__').__main__.dev()" $(filter-out dev,$(MAKECMDGOALS))

prod:
	uv run --no-sync python -c "__import__('mcp_template_python.__main__').__main__.main()" $(filter-out prod,$(MAKECMDGOALS))

build:
	uv build $(filter-out build,$(MAKECMDGOALS))

clean:
	rm -rf .venv .ruff_cache dist/ build/ *.egg-info $(filter-out clean,$(MAKECMDGOALS))

update:
	uv sync --all-extras --all-packages -U $(filter-out update,$(MAKECMDGOALS))

%:
	@:
