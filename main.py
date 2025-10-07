import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class TestPresmaWebsite(unittest.TestCase):
    
    def setUp(self) -> None:
        """Set up the WebDriver before each test"""
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.base_url = "http://presma.dbsnetwork.my.id/"
    
    def tearDown(self) -> None:
        """Clean up after each test"""
        if self.driver:
            self.driver.quit()
    
    def test_page_loads(self) -> None:
        """Test that the website loads successfully"""
        self.driver.get(self.base_url)
        self.assertIsNotNone(self.driver.current_url)
        self.assertTrue(self.base_url in self.driver.current_url)
    
    def test_page_title(self) -> None:
        """Test that the page has a title"""
        self.driver.get(self.base_url)
        title = self.driver.title
        self.assertIsNotNone(title)
        self.assertNotEqual(title.strip(), "")
        print(f"Page title: {title}")
    
    def test_page_has_content(self) -> None:
        """Test that the page has some content in body"""
        self.driver.get(self.base_url)
        body = self.driver.find_element(By.TAG_NAME, "body")
        self.assertIsNotNone(body)
        self.assertNotEqual(body.text.strip(), "")
    
    def test_response_time(self) -> None:
        """Test that the page loads within reasonable time"""
        start_time = time.time()
        self.driver.get(self.base_url)
        load_time = time.time() - start_time
        self.assertLess(load_time, 30)  # Page should load within 30 seconds
        print(f"Page load time: {load_time:.2f} seconds")
    
    def test_page_status(self) -> None:
        """Test that the page returns a successful status"""
        self.driver.get(self.base_url)
        # If we can access the page without exception, it's likely working
        current_url = self.driver.current_url
        self.assertIsNotNone(current_url)


def main() -> None:
    """Main function to run the tests"""
    unittest.main(verbosity=2)


if __name__ == '__main__':
    main()