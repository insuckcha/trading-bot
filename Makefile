# Makefile for trading bot project

# Create virtual environment
venv:
	python -m venv venv
	venv/bin/pip install -r requirements.txt

# Run the trading bot
run-bot:
	python bot.py

# Run the Streamlit UI
run-ui:
	streamlit run ui/visualize.py

# Run Alpaca API test
check-alpaca:
	python utils/check_alpaca_account.py

# Run Polygon API test
check-polygon:
	python utils/check_polygon.py

# Freeze requirements.txt
freeze:
	pip freeze > requirements.txt

# Clean pycache
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
