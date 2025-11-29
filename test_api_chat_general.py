import json
import pytest
import time
import requests

# API Configuration
API_URL = "https://roseai.local.arhamsoft.dev/api/assistant/chat"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI1YjMxMjg2NC0xYTVjLTQzOTItOTFkOS1lNTlmNTdlMjdhN2EiLCJpYXQiOjE3NjMxMTIxNTksImV4cCI6MTc2NTcwNDE1OX0.3skNNXyvvDxQ_EKk3tYnGiK_I17sghSapsy5JpIM4yI"
USER_ID = "5b312864-1a5c-4392-91d9-e59f57e27a7a"
CHAT_ID = "90f21a44-2766-41f8-aeab-3332b5011685"
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
    with open("roseaiGeneralResponses.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    test_api_chat()
