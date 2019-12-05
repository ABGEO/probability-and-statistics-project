default: run

## run	:	Run application.
.PHONY: run
run:
	@echo 'Running application ...'
	@./venv/bin/python3 app.py
