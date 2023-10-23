# Use the official fastapi uvicorn image as the base image
FROM public.ecr.aws/lambda/python:3.10

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Command to run on container start
CMD [ "api.handler" ]

