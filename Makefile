install:
	pip install --upgrade pip && \
	pip install -r requirements.txt 
	#python -m textblob.download_corpora

test:
	python -m pytest -vv --cov=report --cov=EMR_core --cov=main test.py

lint:
	pylint --disable=R,C *.py EMR_core/*.py

format:
	black *.py EMR_core	

all: install lint test