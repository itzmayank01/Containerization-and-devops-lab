
FROM python:3.9-slim
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .

EXPOSE 5000

CMD ["python", "main.py"]