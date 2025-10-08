from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

class TestCompetitionManagement:
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

    def test_add_competition(self, competition_data):
        """Test the complete add competition flow"""
        try:
            # Step 6: Ensure we're on dashboard
            print("Step 6: Navigating to dashboard...")
            self.driver.get("https://presma.dbsnetwork.my.id/dashboard")
            time.sleep(2)
            
            # Step 7: Navigate to competition list page
            print("Step 7: Clicking Daftar Lomba menu...")
            daftar_lomba_menu = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="https://presma.dbsnetwork.my.id/daftar_lomba"]'))
            )
            daftar_lomba_menu.click()
            time.sleep(2)
            
            # Step 8: Click add new competition button
            print("Step 8: Clicking Ajukan Lomba button...")
            add_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-sm.btn-success.mt-1'))
            )
            add_button.click()
            time.sleep(2)
            
            # Step 9: We should now be on the create page
            print("Step 9: Now on create competition page...")
            self.wait.until(
                EC.url_contains("daftar_lomba/create")
            )
            
            # Step 10: Fill competition name
            print("Step 10: Filling competition name...")
            lomba_nama = self.wait.until(
                EC.presence_of_element_located((By.ID, "lomba_nama"))
            )
            lomba_nama.clear()
            lomba_nama.send_keys(competition_data['nama'])
            time.sleep(1)
            
            # Step 11: Fill competition description
            print("Step 11: Filling competition description...")
            lomba_deskripsi = self.driver.find_element(By.ID, "lomba_deskripsi")
            lomba_deskripsi.clear()
            lomba_deskripsi.send_keys(competition_data['deskripsi'])
            time.sleep(1)
            
            # Step 12: Fill website link
            print("Step 12: Filling website link...")
            link_website = self.driver.find_element(By.ID, "link_website")
            link_website.clear()
            link_website.send_keys(competition_data['link_website'])
            time.sleep(1)
            
            # Step 13: Select expertise field (bidang keahlian)
            print("Step 13: Selecting expertise field...")
            bidang_keahlian_select = Select(self.driver.find_element(By.ID, "bidang_keahlian_id_create"))
            bidang_keahlian_select.select_by_index(competition_data['bidang_keahlian_index'])  # Select by index
            time.sleep(1)
            
            # Step 15: Fill start date
            print("Step 15: Filling start date...")
            tanggal_mulai = self.driver.find_element(By.ID, "tanggal_mulai")
            tanggal_mulai.clear()
            tanggal_mulai.send_keys(competition_data['tanggal_mulai'])
            time.sleep(1)
            
            # Step 16: Select organizer
            print("Step 16: Selecting organizer...")
            penyelenggara_select = Select(self.driver.find_element(By.ID, "penyelenggara_id"))
            penyelenggara_select.select_by_index(competition_data['penyelenggara_index'])  # Select by index
            time.sleep(1)
            
            # Step 17: Select competition level
            print("Step 17: Selecting competition level...")
            tingkat_lomba_select = Select(self.driver.find_element(By.ID, "tingkat_lomba_id"))
            tingkat_lomba_select.select_by_index(competition_data['tingkat_lomba_index'])  # Select by index
            time.sleep(1)
            
            # Step 18: Fill number of members
            print("Step 18: Filling number of members...")
            jumlah_anggota = self.driver.find_element(By.ID, "jumlah_anggota")
            jumlah_anggota.clear()
            jumlah_anggota.send_keys(str(competition_data['jumlah_anggota']))
            time.sleep(1)
            
            # Step 19: Fill end date
            print("Step 19: Filling end date...")
            tanggal_selesai = self.driver.find_element(By.ID, "tanggal_selesai")
            tanggal_selesai.clear()
            tanggal_selesai.send_keys(competition_data['tanggal_selesai'])
            time.sleep(1)
            
            # Step 20: Fill organizer name
            print("Step 19.1: Filling organizer name...")
            penyelenggara_nama = self.driver.find_element(By.ID, "penyelenggara_nama")
            penyelenggara_nama.clear()
            penyelenggara_nama.send_keys(competition_data['penyelenggara_nama'])
            time.sleep(1)
            
            # Step 21: Select city
            print("Step 19.2: Selecting city...")
            kota_select = Select(self.driver.find_element(By.ID, "kota_id"))
            kota_select.select_by_index(competition_data['kota_index'])  # Select by index
            time.sleep(1)
            
            # Step 22: Upload pamphlet image
            print("Step 20: Uploading pamphlet image...")
            if competition_data.get('foto_pamflet_path'):
                # Convert relative path to absolute path
                script_dir = os.path.dirname(os.path.abspath(__file__))
                absolute_path = os.path.abspath(os.path.join(script_dir, competition_data['foto_pamflet_path']))
                
                print(f"Script directory: {script_dir}")
                print(f"Relative path: {competition_data['foto_pamflet_path']}")
                print(f"Absolute path: {absolute_path}")
                
                if os.path.exists(absolute_path):
                    foto_pamflet = self.driver.find_element(By.ID, "foto_pamflet")
                    foto_pamflet.send_keys(absolute_path)
                    time.sleep(2)
                    print(f"✅ Image uploaded successfully: {os.path.basename(absolute_path)}")
                else:
                    print(f"❌ Image file not found: {absolute_path}")
            else:
                print("⚠️ No pamphlet image path provided, skipping...")
            
            # Step 23: Click save button
            print("Step 21: Clicking save button...")
            save_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"].btn.btn-primary.ml-2')
            save_button.click()
            time.sleep(3)
            
            print("✅ Competition creation process completed!")
            return True
            
        except Exception as e:
            print(f"❌ Error during competition creation test: {str(e)}")
            return False

def main():
    """Main function to run the test"""
    test = TestCompetitionManagement()
    
    try:
        # Setup
        test.setup()
        
        # Login credentials
        username = "234172003"
        password = "mahasiswa123"
        
        # Login first
        login_success = test.login(username, password)
        
        if not login_success:
            print("❌ Login failed. Cannot proceed with competition creation test.")
            return
        
        # Competition data to fill in the form
        competition_data = {
            'nama': 'Test Competition 2024',
            'deskripsi': 'This is a test competition for automation testing purposes. It includes various challenges and tasks.',
            'link_website': 'https://example.com/competition',
            'bidang_keahlian_index': 1,  # Select second option (index starts from 0)
            'tanggal_mulai': '01-12-2024',
            'penyelenggara_index': 1,  # Select second option
            'tingkat_lomba_index': 1,  # Select second option
            'jumlah_anggota': 3,
            'tanggal_selesai': '31-12-2024',
            'penyelenggara_nama': 'Test Organizer Name',  # NEW FIELD
            'kota_index': 1,  # NEW FIELD - Select second city option
            'foto_pamflet_path': '../../assets/lomba-nasional.jpg'  # Update this path to your actual image file
        }
        
        success = test.test_add_competition(competition_data)
        
        if success:
            print("✅ Complete competition creation test flow completed successfully!")
        else:
            print("❌ Competition creation test failed!")
            
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        
    finally:
        # Cleanup
        input("Press Enter to close the browser...")  # Pause to see results
        test.teardown()

if __name__ == "__main__":
    main()