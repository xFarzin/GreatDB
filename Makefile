.PHONY: run-api run-bot test compile-locales

run-api:
	uvicorn src.api.main:app --reload

run-bot:
	python -m src.bot.main

compile-locales:
	pybabel compile -d src/locales -D messages

test:
	pytest tests/
