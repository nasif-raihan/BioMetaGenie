run:
	python3 main.py

clear-output:
	sudo rm -r ./output/*

clear-logs:
	sudo rm -r ./logs/*

install:
	poetry install --no-root