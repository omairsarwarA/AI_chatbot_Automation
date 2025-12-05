import json
import pytest
import time
import requests

API_URL = "https://chat.gethardmoney.com/chat"


def test_api_chat():

    # Step 1: Read input messages
    with open("query.json", "r", encoding="utf-8") as f:
        messages = json.load(f)

    results = []

    # Step 2: Send each message to the API
    for msg in messages:
        print(f"Sending message: {msg['query']}")

        response = requests.post(API_URL, json=msg)

        assert response.status_code == 200, f"API call failed: {response.status_code}"

        data = response.json()
        # print("Response received:", data)

        results.append({
            "request": msg,
            "response": data
        })

        time.sleep(10)   # Keep if the API rate-limits. Remove if unnecessary.

    # Step 3: Save results
    with open("query_answer.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    test_api_chat()

