# syntax=docker/dockerfile:1

# Use the official Python image from the Docker Hub
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip3 install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Install Nginx
RUN apt-get update && apt-get install -y nginx

# Remove the default Nginx configuration file
RUN rm /etc/nginx/sites-enabled/default

# Copy the Nginx configuration file
COPY config/nginx.conf /etc/nginx/sites-available/flask_app
RUN ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled

# Expose the port Nginx will run on
EXPOSE 80

# Start Nginx and the Flask app
CMD service nginx start && python3 -m flask run --host=0.0.0.0