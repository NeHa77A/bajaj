FROM python:3.11-slim

WORKDIR /app

# Copy project files
COPY . /app

# Install system deps if needed
RUN apt-get update && apt-get install -y build-essential git && rm -rf /var/lib/apt/lists/*

# Install python deps
RUN pip install --no-cache-dir -r requirements.txt

# Install the local package (editable)
RUN pip install --no-cache-dir -e .

# Expose ports
EXPOSE 8000 8501

ENV PYTHONUNBUFFERED=1

# default command (example single-container start)
CMD bash -c "python scripts/ingest_from_folder.py && uvicorn services.fastapi_api.app:app --host 0.0.0.0 --port 8000"
