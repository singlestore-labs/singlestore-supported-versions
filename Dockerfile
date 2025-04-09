FROM python:3.9-slim

# Install necessary dependencies
RUN pip install requests beautifulsoup4

# Copy the Python script into the container
COPY singlestore_supported_versions.py /action/singlestore_supported_versions.py

ENTRYPOINT ["python", "/action/singlestore_supported_versions.py"]
