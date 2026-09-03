FROM python:3.12-slim

WORKDIR /app

# Install gettext for msgfmt/Babel
RUN apt-get update && apt-get install -y gettext && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Compile localizations during build
RUN pybabel compile -d src/locales -D messages || true

# We can override the command in docker-compose for bot vs api vs worker
