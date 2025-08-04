FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libxml2-dev libxslt-dev libz-dev libffi-dev

COPY . .

RUN pip install --no-cache-dir requests beautifulsoup4 httpx

CMD ["python", "run_agent.py"]
