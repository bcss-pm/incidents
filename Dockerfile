# Specify python runtime
FROM python:3.6

# Update Container
RUN apt-get update

# Make directory
RUN mkdir -p /app

# Copy over requirements and install to allow for caching
COPY  requirements.txt ./app/requirements.txt 

# Set the working directory to /app 
WORKDIR /app

# Install needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Copy current directory into container at /app
COPY . /app



# Commented for test
# Make port 5000 available to the world outside this container
#EXPOSE 5000

## Define environment variable
#ENV NAME incidentDB
#
## Run gunicorn when the container launches
#ENTRYPOINT ["python", "web.py"]
