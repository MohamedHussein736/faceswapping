# Use the official Python base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR .

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port that Uvicorn will run on
EXPOSE 8000

# Define the command to run your Uvicorn app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
