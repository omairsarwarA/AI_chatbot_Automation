import json
import pytest
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# API Configuration
API_URL = "https://roseai.local.arhamsoft.dev/api/health/chat"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJiNTA0YjQ1NC00NzY4LTQ3OTMtOTA4OC0xMDNiNGQyZTkzNjUiLCJpYXQiOjE3NjI1MTQ1MDAsImV4cCI6MTc2NTEwNjUwMH0.OyvYl0xxrFUJtdj6A5K73RtHQuxXRBv26carkI-"
USER_ID = "b504b454-4768-4793-9088-103b4d2e9365"
CHAT_ID = "d0d80764-dba2-42d9-acd6-9d6d4b6b134a"
TIMEZONE = "Asia/Karachi"

@pytest.fixture(scope="session")
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()


def test_api_chat(browser):
    """Test RoseAI chat API with multiple messages"""
    
    # Step 1: Read input messages from JSON file
    with open("roseaidata.json", "r", encoding="utf-8") as f:
        messages = json.load(f)

    results = []

    # Step 2: Send each message to the API with proper payload structure
    for msg in messages:
        # Construct payload according to API specification
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
            # Try sending as form data instead of JSON
            response = requests.post(
                API_URL, 
                data=payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            print(f"Status Code: {response.status_code}")
            # print(f"Response: {response.text}")
            
            assert response.status_code == 200, f"API call failed with status {response.status_code}: {response.text}"
            
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
        
        # Wait between requests to avoid rate limiting
        time.sleep(10)

    # Step 3: Write results to responses.json
    with open("roseAiresponses.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # print(f"\nTest completed. {len(results)} messages processed.")
    # print(f"Results saved to roseAiresponses.json")


if __name__ == "__main__":
    # Run test directly without pytest
    class MockBrowser:
        pass
    
    test_api_chat(MockBrowser())