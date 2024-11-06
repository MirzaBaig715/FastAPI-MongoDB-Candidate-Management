FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY . .

# Copy the custom wait-for-it.sh script and make it executable
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Expose the port that the FastAPI app will run on
EXPOSE 8000

# Use the custom wait-for-it.sh script to wait for MongoDB and Redis before starting the app
CMD ["/wait-for-it.sh"]
