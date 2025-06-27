#!/bin/sh


# Usage Traffic Generator Script
# This script generates traffic to a specified target URL at a defined interval.
# Usage: ./traffic-generator.sh <target endpoint> <interval in seconds>
if [ "$#" lt 2 ]; then
    echo "Usage: $0 <target> <interval in seconds>"
    exit 1
fi


TARGET=$1
INTERVAL=$2

echo "Starting traffic generator to $TARGET every $INTERVAL seconds..."

while true; do
   REQUEST_TIME=$(date +%Y-%m-%dT%H:%M:%S)
   RESPONSE=$(curl -s "$TARGET")
   HOSTNAME=$(echo "$RESPONSE" | jq -r '.hostname')

   echo "[$REQUEST_TIME] Request to $TARGET: response -> $HOSTNAME"
   sleep "$INTERVAL"

done
