import pytest
import requests
import uuid
from typing import Dict, Any


class TestConfig:
    """Configuration for FAST API tests"""
    BASE_URL = "https://apex.fast-cables.com:8083/ords/fast/fast/asbot"
    USER_ID = "arham_bot_api"
    PASSWORD = "FAST393ASB"
    DEMO_MOBILE = "923331111111"
    DEMO_SERIAL = "1687187415424"  # 13-digit product serial
    GIFT_ID = "1"  # Update with actual gift_id from Bilal
    
    def __init__(self):
        """Initialize TestConfig"""
        pass
    
    @staticmethod
    def generate_trans_id() -> str:
        """Generate unique 36-character transaction ID"""
        return str(uuid.uuid4())


class TestFastTasdeeqAPI:
    """Test cases for Fast Tasdeeq (Product Verification) API"""
    
    def __init__(self):
        """Initialize TestFastTasdeeqAPI"""
        self.config = TestConfig()
    
    def setup_method(self, method):
        """Setup before each test method"""
        self.config = TestConfig()
    
    def test_successful_verification(self):
        """Test successful product verification"""
        trans_id = TestConfig.generate_trans_id()
        url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id}/{TestConfig.DEMO_MOBILE}/{TestConfig.DEMO_SERIAL}"
        
        response = requests.get(url, verify=False)
        
        assert response.status_code == 200
        assert response.text == "1", f"Expected '1' (Successful), got '{response.text}'"
    
    def test_already_verified_product(self):
        """Test verification of already verified product"""
        trans_id = TestConfig.generate_trans_id()
        url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id}/{TestConfig.DEMO_MOBILE}/{TestConfig.DEMO_SERIAL}"
        
        # First verification
        requests.get(url, verify=False)
        
        # Second verification with different trans_id
        trans_id_2 = TestConfig.generate_trans_id()
        url_2 = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id_2}/{TestConfig.DEMO_MOBILE}/{TestConfig.DEMO_SERIAL}"
        response = requests.get(url_2, verify=False)
        
        assert response.status_code == 200
        assert response.text == "2", f"Expected '2' (Already Verified), got '{response.text}'"
    
    def test_invalid_serial_number(self):
        """Test verification with invalid serial number"""
        trans_id = TestConfig.generate_trans_id()
        invalid_serial = "0000000000000"
        url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id}/{TestConfig.DEMO_MOBILE}/{invalid_serial}"
        
        response = requests.get(url, verify=False)
        
        assert response.status_code == 200
        assert response.text == "0", f"Expected '0' (Invalid), got '{response.text}'"
    
    def test_invalid_mobile_number_format(self):
        """Test verification with invalid mobile number format"""
        trans_id = TestConfig.generate_trans_id()
        invalid_mobile = "92331111"  # Less than 12 digits
        url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id}/{invalid_mobile}/{TestConfig.DEMO_SERIAL}"
        
        response = requests.get(url, verify=False)
        
        assert response.status_code in [200, 400, 500]
        # Response should be 0 or error
    
    def test_wrong_credentials(self):
        """Test API with wrong credentials"""
        trans_id = TestConfig.generate_trans_id()
        wrong_user = "wrong_user"
        url = f"{TestConfig.BASE_URL}/{wrong_user}/{TestConfig.PASSWORD}/{trans_id}/{TestConfig.DEMO_MOBILE}/{TestConfig.DEMO_SERIAL}"
        
        response = requests.get(url, verify=False)
        
        assert response.status_code in [401, 403, 404]
    
    def test_duplicate_transaction_id(self):
        """Test API with duplicate transaction ID"""
        trans_id = TestConfig.generate_trans_id()
        url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id}/{TestConfig.DEMO_MOBILE}/{TestConfig.DEMO_SERIAL}"
        
        # First request
        response1 = requests.get(url, verify=False)
        assert response1.status_code == 200
        
        # Second request with same trans_id (should fail or give error)
        response2 = requests.get(url, verify=False)
        assert response2.status_code in [200, 400, 409]


class TestBalancePointsCheckAPI:
    """Test cases for Balance Points Check API"""
    
    def __init__(self):
        """Initialize TestBalancePointsCheckAPI"""
        self.config = TestConfig()
    
    def setup_method(self, method):
        """Setup before each test method"""
        self.config = TestConfig()
    
    def test_check_balance_success(self):
        """Test successful balance check"""
        trans_id = TestConfig.generate_trans_id()
        url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id}/{TestConfig.DEMO_MOBILE}/B"
        
        response = requests.get(url, verify=False)
        
        assert response.status_code == 200
        # Response format: total_point|used_point|rem_point
        points = response.text.split('|')
        assert len(points) == 3, f"Expected 3 values, got {len(points)}"
        assert all(p.isdigit() for p in points), "All values should be numeric"
    
    def test_check_balance_no_points(self):
        """Test balance check for user with no points"""
        trans_id = TestConfig.generate_trans_id()
        new_mobile = "923339999999"  # Mobile with no points
        url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id}/{new_mobile}/B"
        
        response = requests.get(url, verify=False)
        
        assert response.status_code == 200
        assert response.text == "0", f"Expected '0' for no points, got '{response.text}'"
    
    def test_check_balance_invalid_mobile(self):
        """Test balance check with invalid mobile"""
        trans_id = TestConfig.generate_trans_id()
        invalid_mobile = "000000000000"
        url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id}/{invalid_mobile}/B"
        
        response = requests.get(url, verify=False)
        
        assert response.status_code == 200
        assert response.text == "0"
    
    def test_check_balance_wrong_text_parameter(self):
        """Test balance check with wrong text parameter (not 'B')"""
        trans_id = TestConfig.generate_trans_id()
        url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id}/{TestConfig.DEMO_MOBILE}/BALANCE"
        
        response = requests.get(url, verify=False)
        
        assert response.status_code in [200, 400]


class TestFastRadeemAPI:
    """Test cases for Fast Radeem (Redemption) API"""
    
    def __init__(self):
        """Initialize TestFastRadeemAPI"""
        self.config = TestConfig()
    
    def setup_method(self, method):
        """Setup before each test method"""
        self.config = TestConfig()
    
    def test_successful_redemption(self):
        """Test successful points redemption"""
        trans_id = TestConfig.generate_trans_id()
        url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id}/{TestConfig.DEMO_MOBILE}/AR/{TestConfig.GIFT_ID}"
        
        response = requests.get(url, verify=False)
        
        assert response.status_code == 200
        assert response.text in ["1", "2"], f"Expected '1' or '2', got '{response.text}'"
    
    def test_insufficient_points(self):
        """Test redemption with insufficient points"""
        trans_id = TestConfig.generate_trans_id()
        high_value_gift = "999"  # Assuming this requires many points
        url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id}/{TestConfig.DEMO_MOBILE}/AR/{high_value_gift}"
        
        response = requests.get(url, verify=False)
        
        assert response.status_code == 200
        # Could be "2" (Insufficient Points) or "3" (Invalid Gift)
        assert response.text in ["2", "3"]
    
    def test_invalid_gift_code(self):
        """Test redemption with invalid gift code"""
        trans_id = TestConfig.generate_trans_id()
        invalid_gift = "INVALID123"
        url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id}/{TestConfig.DEMO_MOBILE}/AR/{invalid_gift}"
        
        response = requests.get(url, verify=False)
        
        assert response.status_code == 200
        assert response.text == "3", f"Expected '3' (Invalid Gift Code), got '{response.text}'"
    
    def test_redemption_failed(self):
        """Test failed redemption"""
        trans_id = TestConfig.generate_trans_id()
        url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id}/000000000000/AR/{TestConfig.GIFT_ID}"
        
        response = requests.get(url, verify=False)
        
        assert response.status_code == 200
        assert response.text == "0", f"Expected '0' (Failed), got '{response.text}'"
    
    def test_redemption_wrong_text_parameter(self):
        """Test redemption with wrong text parameter (not 'AR')"""
        trans_id = TestConfig.generate_trans_id()
        url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id}/{TestConfig.DEMO_MOBILE}/REDEEM/{TestConfig.GIFT_ID}"
        
        response = requests.get(url, verify=False)
        
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            assert response.text == "0"


class TestAPIIntegration:
    """Integration tests combining multiple API calls"""
    
    def __init__(self):
        """Initialize TestAPIIntegration"""
        self.config = TestConfig()
    
    def setup_method(self, method):
        """Setup before each test method"""
        self.config = TestConfig()
    
    def test_complete_workflow(self):
        """Test complete workflow: verify product -> check balance -> redeem"""
        # Step 1: Verify product
        trans_id_1 = TestConfig.generate_trans_id()
        verify_url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id_1}/{TestConfig.DEMO_MOBILE}/{TestConfig.DEMO_SERIAL}"
        verify_response = requests.get(verify_url, verify=False)
        assert verify_response.status_code == 200
        
        # Step 2: Check balance
        trans_id_2 = TestConfig.generate_trans_id()
        balance_url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id_2}/{TestConfig.DEMO_MOBILE}/B"
        balance_response = requests.get(balance_url, verify=False)
        assert balance_response.status_code == 200
        
        # Step 3: Redeem if points available
        if balance_response.text != "0":
            trans_id_3 = TestConfig.generate_trans_id()
            redeem_url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id_3}/{TestConfig.DEMO_MOBILE}/AR/{TestConfig.GIFT_ID}"
            redeem_response = requests.get(redeem_url, verify=False)
            assert redeem_response.status_code == 200


class TestEdgeCases:
    """Edge case tests"""
    
    def __init__(self):
        """Initialize TestEdgeCases"""
        self.config = TestConfig()
    
    def setup_method(self, method):
        """Setup before each test method"""
        self.config = TestConfig()
    
    def test_special_characters_in_serial(self):
        """Test with special characters in serial number"""
        trans_id = TestConfig.generate_trans_id()
        special_serial = "1234567@#$%^&"
        url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id}/{TestConfig.DEMO_MOBILE}/{special_serial}"
        
        response = requests.get(url, verify=False)
        assert response.status_code in [200, 400]
    
    def test_empty_parameters(self):
        """Test with empty parameters"""
        trans_id = TestConfig.generate_trans_id()
        url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id}/ /{TestConfig.DEMO_SERIAL}"
        
        response = requests.get(url, verify=False)
        assert response.status_code in [200, 400, 404]
    
    def test_sql_injection_attempt(self):
        """Test SQL injection protection"""
        trans_id = TestConfig.generate_trans_id()
        sql_inject = "1' OR '1'='1"
        url = f"{TestConfig.BASE_URL}/{TestConfig.USER_ID}/{TestConfig.PASSWORD}/{trans_id}/{TestConfig.DEMO_MOBILE}/{sql_inject}"
        
        response = requests.get(url, verify=False)
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            assert response.text == "0"


# Pytest fixtures
@pytest.fixture(scope="session")
def api_config():
    """Fixture to provide API configuration"""
    return TestConfig()


@pytest.fixture
def unique_trans_id():
    """Fixture to generate unique transaction ID for each test"""
    return TestConfig.generate_trans_id()


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "edge_case: mark test as edge case test")


if __name__ == "__main__":
    """Allow running tests directly with python"""
    pytest.main([__file__, "-v", "--tb=short"])