# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install libgl1-mesa-glx

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that your FastAPI app will run on
EXPOSE 8000

# Define the command to run your FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]
