# Use an official Python runtime as a parent image.
# The 'slim' version is smaller and good for production.
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the local directory contents into the container at /app
# This will copy the main.py file.
COPY . .

# Install any needed packages specified in requirements.txt
# For this app, we only need fastapi and uvicorn.
RUN pip install --no-cache-dir fastapi uvicorn

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define the command to run your app using uvicorn on port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]