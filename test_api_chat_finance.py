import json
import pytest
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# API Configuration
API_URL = "https://roseai.local.arhamsoft.dev/api/finance/chat"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI1YjMxMjg2NC0xYTVjLTQzOTItOTFkOS1lNTlmNTdlMjdhN2EiLCJpYXQiOjE3NjI5NDQzNzQsImV4cCI6MTc2NTUzNjM3NH0.Wbm7rZJTHTD6cFSFebKJ3TkBAsUgdeSKN1GzZ_Oz16g"
USER_ID = "5b312864-1a5c-4392-91d9-e59f57e27a7a"
CHAT_ID = "67c133d6-bf60-43f4-9aea-c36f0b9495a7"
TIMEZONE = "Asia/Karachi"
FILETYPE= "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
FILEURL ="http://roseaibackend.architected.solutions/uploads/1762942728947-complex_balance_sheet.xlsx"


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
    with open("roseaiFinanceMessage.json", "r", encoding="utf-8") as f:
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
    with open("roseaiFinanceresponses.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # print(f"\nTest completed. {len(results)} messages processed.")
    # print(f"Results saved to roseAiresponses.json")


if __name__ == "__main__":
    # Run test directly without pytest
    class MockBrowser:
        pass
    
    test_api_chat(MockBrowser())