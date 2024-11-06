#!/bin/bash

# Function to check if a service is available
#wait_for_service() {
#  local host=$1
#  local port=$2
#  local retries=30
#  local wait_time=2
#
#  echo "Waiting for $host:$port to be available..."
#
#  # Retry loop to check if service is available
#  for i in $(seq 1 $retries); do
#    # Use nc (Netcat) to check if the port is open
#    nc -z -v -w30 $host $port 2>/dev/null && echo "$host:$port is up!" && return 0
#    echo "Retrying... ($i/$retries)"
#    sleep $wait_time
#  done
#
#  # If we reach here, service is not available
#  echo "$host:$port did not become available in time."
#  return 1
#}
#
## Wait for MongoDB
#wait_for_service "mongodb" "27017" || exit 1
#
## Wait for Redis
#wait_for_service "redis" "6379" || exit 1

# If both services are up, start the application
echo "All services are up, starting FastAPI application..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000
