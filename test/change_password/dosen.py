from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

class TestChangePassword:
    def __init__(self):
        self.driver = None
        self.wait = None
    
    def setup(self):
        """Setup WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # Remove headless mode to see the browser actions
        # chrome_options.add_argument("--headless")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        # self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
    
    def teardown(self):
        """Cleanup WebDriver"""
        if self.driver:
            self.driver.quit()
    
    def login(self, username, password):
        """Complete login flow"""
        try:
            # Step 1: Navigate directly to login page
            print("Step 1: Navigating to login page...")
            self.driver.get("https://presma.dbsnetwork.my.id/login")
            time.sleep(2)
            
            # Step 2: Fill username
            print("Step 2: Filling username...")
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.clear()
            username_field.send_keys(username)
            time.sleep(1)
            
            # Step 3: Fill password
            print("Step 3: Filling password...")
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys(password)
            time.sleep(1)
            
            # Step 4: Click login submit button
            print("Step 4: Clicking login submit button...")
            submit_button = self.driver.find_element(By.ID, "btn-login")
            submit_button.click()
            time.sleep(3)
            
            # Wait for dashboard to load
            self.wait.until(
                EC.url_contains("dashboard")
            )
            print("✅ Login successful!")
            return True
            
        except Exception as e:
            print(f"❌ Error during login: {str(e)}")
            return False
    
    def test_change_password(self, old_password, new_password):
        """Test the complete password change flow"""
        try:
            # Step 6: Ensure we're on dashboard
            print("Step 6: Navigating to dashboard...")
            self.driver.get("https://presma.dbsnetwork.my.id/dashboard")
            time.sleep(2)
            
            # Step 7: Click profile icon
            print("Step 7: Clicking profile icon...")
            profile_icon = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-toggle="dropdown"][aria-haspopup="true"][aria-expanded="false"].p-0.btn'))
            )
            profile_icon.click()
            time.sleep(1)
            
            # Step 8: Click on "Profile Saya" button
            print("Step 8: Clicking Profile Saya button...")
            profile_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="https://presma.dbsnetwork.my.id/profile"].nav-link'))
            )
            profile_button.click()
            time.sleep(2)
            
            # Step 9: Click change password button
            print("Step 9: Clicking change password button...")
            change_password_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-warning[onclick*="modalPassword"]'))
            )
            change_password_btn.click()
            time.sleep(2)
            
            # Step 10: Modal should be visible now
            print("Step 10: Modal opened, waiting for form fields...")
            
            # Step 11: Fill old password field
            print("Step 11: Filling old password...")
            old_password_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"][name="old_password"]'))
            )
            old_password_field.clear()
            old_password_field.send_keys(old_password)
            time.sleep(1)
            
            # Step 12: Fill new password field
            print("Step 12: Filling new password...")
            new_password_field = self.driver.find_element(By.CSS_SELECTOR, 'input[type="password"][name="new_password"]')
            new_password_field.clear()
            new_password_field.send_keys(new_password)
            time.sleep(1)
            
            # Step 13: Click save button
            print("Step 13: Clicking save button...")
            save_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"].btn.btn-primary')
            save_button.click()
            time.sleep(3)
            
            # Check for success message or redirect
            print("✅ Password change process completed!")
            return True
            
        except Exception as e:
            print(f"❌ Error during password change test: {str(e)}")
            return False

def main():
    """Main function to run the test"""
    test = TestChangePassword()
    
    try:
        # Setup
        test.setup()
        
        # Login credentials
        username = "NIDN0003"
        current_password = "dosen123"
        # current_password = "newpwd123"
        
        # Login first
        login_success = test.login(username, current_password)
        
        if not login_success:
            print("❌ Login failed. Cannot proceed with password change test.")
            return
        
        # Test password change
        # old_password = "newpwd123"  # Current password
        # new_password = "dosen123"  # New password - change this as needed
        old_password = "dosen123"
        new_password = "newpwd123"
        
        success = test.test_change_password(old_password, new_password)
        
        if success:
            print("✅ Complete test flow completed successfully!")
            print("Note: If password was actually changed, update your credentials for future tests.")
        else:
            print("❌ Password change test failed!")
            
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        
    finally:
        # Cleanup
        input("Press Enter to close the browser...")  # Pause to see results
        test.teardown()

if __name__ == "__main__":
    main()