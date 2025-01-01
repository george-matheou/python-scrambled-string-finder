FROM python:3.11-slim

# Set environment variables to reduce interactive prompts during builds
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies including make and Python3
RUN apt-get update && apt-get install -y \
    make \
    python3 \
    python3-pip \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ARG WORK_DIR="/app"
RUN mkdir -p ${WORK_DIR}

# Set the working directory in the container
WORKDIR ${WORK_DIR}

# Copy the application code into the container
COPY . ${WORK_DIR}

# Install dependencies
RUN make install

# Test the code
RUN make tests

# Command to run the application
ENTRYPOINT ["python3", "scrambled_strings.py"]
