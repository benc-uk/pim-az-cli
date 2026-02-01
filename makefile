build:
	@if [ -z "$$VIRTUAL_ENV" ]; then echo "Error: Virtual environment not active"; exit 1; fi
	azdev extension build pim

lint:
	@if [ -z "$$VIRTUAL_ENV" ]; then echo "Error: Virtual environment not active"; exit 1; fi
	flake8 ./src/pim/azext_pim
	black --check ./src/pim/azext_pim

format:
	@if [ -z "$$VIRTUAL_ENV" ]; then echo "Error: Virtual environment not active"; exit 1; fi
	black ./src/pim/azext_pim

venv:
	python3 -m venv .venv
	. .venv/bin/activate
	@if [ -z "$$VIRTUAL_ENV" ]; then echo "Error: Virtual environment not active"; exit 1; fi
	pip install -r requirements.txt

clean:
	rm -rf ./src/pim/dist
	rm -rf ./src/pim/build
	rm -rf ./src/pim/azext_pim.egg-info