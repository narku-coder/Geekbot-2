worker: python main.py
web: GUNICORN_CMD_ARGS="--workers=1  --timeout=3000 --max-requests=1200 --threads=3" gunicorn bot:app
