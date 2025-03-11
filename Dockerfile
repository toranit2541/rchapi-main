# Use official Python image
FROM python:3.11

# Set working directory inside the container
WORKDIR /app

# Copy the project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run Django with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "rchapi.wsgi:application"]