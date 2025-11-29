import json
import pytest
import time
import requests

# API Configuration
API_URL = "http://192.168.99.106:9118/api/assistant/chat"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI3M2M2N2U0My01YjY3LTQxZWYtYmNlOS00ODk5YjI1ZDg2YzUiLCJpYXQiOjE3NjI5NTU1OTEsImV4cCI6MTc2MzU2MDM5MX0.1iatPOd6LzRg-RWvnSp3go-bKdBV37O763ImhKIADOI"
USER_ID = "73c67e43-5b67-41ef-bce9-4899b25d86c5"
CHAT_ID = "8fd0a3ca-b81b-4d41-9fe3-f6cf3683e9aa"
TIMEZONE = "Asia/Karachi"


def test_api_chat():
    """Test RoseAI chat API with multiple messages"""

    # Step 1: Read input messages from JSON file
    with open("roseaiGeneralMessage.json", "r", encoding="utf-8") as f:
        messages = json.load(f)

    results = []

    # Step 2: Send each message to the API
    for msg in messages:

        payload = {
            "user_id": USER_ID,
            "message": msg.get("message", ""),
            "chat_id": CHAT_ID,
            "web_access": "true",
            "file_urls": "[]",
            "token": TOKEN,
            "timezone": TIMEZONE
        }

        print(f"Sending message: {payload['message']}")

        try:
            response = requests.post(
                API_URL,
                data=payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            print(f"Status Code: {response.status_code}")

            assert response.status_code == 200, (
                f"API call failed with status {response.status_code}: {response.text}"
            )

            data = response.json()

            results.append({
                "request": payload,
                "response": data,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

            results.append({
                "request": payload,
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })

        # Avoid rate-limits
        time.sleep(10)

    # Step 3: Save results
    with open("roseaiGeneralResponsesLocal.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    test_api_chat()
