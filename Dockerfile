FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Run Django app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "inventory_project.wsgi:application"]
