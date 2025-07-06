install:
	pip install --upgrade pip && \
	pip install -r requirements.txt && \
	#python -m textblob.download_corpora

test:
	python -m pytest -vv --cov=report --cov=report_core --cov=main test.py

lint:
	pylint --disable=R,C *.py report_core/*.py

format:
	black *.py report_core	

all: install lint test