.PHONY: init install tests

results/bdp_and_ppda_39_2022.html: src/scatter_bdp_and_ppda.py data/pression_index_39_2022.csv
	python src/scatter_bdp_and_ppda.py > results/bdp_and_ppda_39_2022.html

check:
	black --check --line-length 100 src
	flake8 --max-line-length 100 src
	black --check --line-length 100 tests
	flake8 --max-line-length 100 tests

format:
	black --line-length 100 src
	black --line-length 100 tests

init: install tests

install:
	pip install --editable .

mutants:
	mutmut run --paths-to-mutate xg_plots

tests:
	pytest --verbose