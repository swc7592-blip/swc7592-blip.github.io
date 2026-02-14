#!/bin/bash

# Collection script for X follower tweets
# Collects 10 tweets from each follower

export AUTH_TOKEN="b37280fd9cca4df70b68feb788d99ea8c3d7bfa8"
export CT0="d5b9d6cc30b6c65184c52838c23379e623d69479076333994b5988b423adb6f69483488c8e8a3d44ec92955752263dc24bfe59e68c126cf8ccfb0f814115b48fe443126a3888ace5660cebf1524615ef"
export BIRD_TIMEOUT_MS="20000"

# List of follower usernames
FOLLOWERS=(
    "sma_ll_wish"
    "LPark57744"
    "Eun_chaeo"
    "m00nmarke"
    "wakapaipo"
    "mooonmarkets"
    "ficnmw"
    "M00nMqrket__"
    "assis_kariny"
    "Richard75437864"
    "MediciMindset"
    "ligibookddak"
    "HSLQNc9LMNHMJCk"
)

# Output file
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="/Users/shin/.openclaw/workspace/agents/x/data/follower_tweets_${TIMESTAMP}.json"

# Start JSON array
echo "[" > "$OUTPUT_FILE"

FIRST=true

for username in "${FOLLOWERS[@]}"; do
    echo "Collecting tweets from @$username..."

    # Get 10 tweets from user timeline (json output)
    TWEETS=$(bird user-tweets --json -n 10 "$username" 2>&1)

    # Check if command succeeded
    if echo "$TWEETS" | grep -q '"tweets"'; then
        # Parse tweets and add to output
        echo "$TWEETS" | jq -c '.tweets[]' >> "$OUTPUT_FILE"

        # Add comma separator (except for last user)
        if [ "$username" != "${FOLLOWERS[-1]}" ]; then
            echo "," >> "$OUTPUT_FILE"
        fi
    else
        echo "Failed to collect from @$username: $TWEETS"
    fi

    # Small delay to avoid rate limiting
    sleep 1
done

# Close JSON array
echo "]" >> "$OUTPUT_FILE"

echo "Collection complete! Saved to: $OUTPUT_FILE"
