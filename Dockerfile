# Step 1: Set the Base Image
# Use an official lightweight Python image (python:3.10-slim) as the base.
# This provides a minimal environment with Python 3.10 installed.
FROM python:3.10-slim

# Step 2: Set the Working Directory
# Set the working directory inside the container to '/app'.
# All subsequent commands (like COPY, RUN) will be executed from this directory.
WORKDIR /app

# Step 3: Install Dependencies
# Copy the requirements file first to leverage Docker's build cache.
# This ensures dependencies are only re-installed if requirements.txt changes.
COPY app/requirements.txt .
# Install the Python dependencies listed in requirements.txt.
# --no-cache-dir reduces the image size by not storing the pip cache.
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy Application Code
# Copy the rest of the application code from the local 'app/' directory
# into the container's '/app' working directory.
COPY app/ .

# Step 5: Expose the Application Port
# Inform Docker that the application inside the container will listen on port 8080.
# This is also the port Google Cloud (Vertex AI) will send requests to.
EXPOSE 8080

# Step 6: Define the Entrypoint (Start Command)
# Specify the command to run when the container starts.
# We use 'gunicorn', a production-ready WSGI server.
# --bind 0.0.0.0:8080: Binds the server to all network interfaces on the specified port.
# main:app: Tells Gunicorn to run the 'app' object (Flask instance) from the 'main.py' file.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
