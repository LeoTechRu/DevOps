# build: docker build -t homework_03 .
# run: docker run -p 8000:8000 homework_03
FROM python:3.12-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Run the application using the module itself as an entrypoint.
# This ensures that ``uvicorn`` is started via the Python interpreter which is
# slightly more robust across different environments.
CMD ["python", "app.py"]
