from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
import time
from pathlib import Path
from typing import Optional, TypedDict


class CompetitionData(TypedDict):
    nama: str
    deskripsi: str
    link_website: str
    bidang_keahlian_index: int
    tanggal_mulai: str
    penyelenggara_index: int
    tingkat_lomba_index: int
    jumlah_anggota: int
    tanggal_selesai: str
    penyelenggara_nama: str
    kota_index: int
    foto_pamflet_path: str


class TestCompetitionManagement:
    def __init__(self) -> None:
        self.driver: Optional[WebDriver] = None
        self.wait: Optional[WebDriverWait] = None
    
    def setup(self) -> None:
        """Setup WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Remove headless mode to see the browser actions
        # chrome_options.add_argument("--headless")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        # self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
    
    def teardown(self) -> None:
        """Cleanup WebDriver"""
        if self.driver:
            self.driver.quit()
    
    def login(
        self, 
        username: str, 
        password: str
    ) -> bool:
        """Complete login flow"""
        if not self.driver or not self.wait:
            raise RuntimeError("WebDriver not initialized. Call setup() first.")
        
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

    def test_add_competition(
        self, 
        competition_data: CompetitionData
    ) -> bool:
        """Test the complete add competition flow"""
        if not self.driver or not self.wait:
            raise RuntimeError("WebDriver not initialized. Call setup() first.")
        
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
            bidang_keahlian_select.select_by_index(competition_data['bidang_keahlian_index'])
            time.sleep(1)
            
            # Step 14: Fill start date
            print("Step 14: Filling start date...")
            tanggal_mulai = self.driver.find_element(By.ID, "tanggal_mulai")
            tanggal_mulai.clear()
            tanggal_mulai.send_keys(competition_data['tanggal_mulai'])
            time.sleep(1)
            
            # Step 15: Select organizer
            print("Step 15: Selecting organizer...")
            penyelenggara_select = Select(self.driver.find_element(By.ID, "penyelenggara_id"))
            penyelenggara_select.select_by_index(competition_data['penyelenggara_index'])
            time.sleep(1)
            
            
            if competition_data['penyelenggara_index'] == 1:
                # Step 15-a: Fill organizer name
                print("Step 15.a: Filling organizer name...")
                penyelenggara_nama = self.driver.find_element(By.ID, "penyelenggara_nama")
                penyelenggara_nama.clear()
                penyelenggara_nama.send_keys(competition_data['penyelenggara_nama'])
                time.sleep(1)
                
                # Step 15.b: Select city
                print("Step 15.b: Selecting city...")
                kota_select = Select(self.driver.find_element(By.ID, "kota_id"))
                kota_select.select_by_index(competition_data['kota_index'])
                time.sleep(1)
            
            # Step 16: Select competition level
            print("Step 16: Selecting competition level...")
            tingkat_lomba_select = Select(self.driver.find_element(By.ID, "tingkat_lomba_id"))
            tingkat_lomba_select.select_by_index(competition_data['tingkat_lomba_index']) 
            time.sleep(1)
            
            # Step 17: Fill number of members
            print("Step 17: Filling number of members...")
            jumlah_anggota = self.driver.find_element(By.ID, "jumlah_anggota")
            jumlah_anggota.clear()
            jumlah_anggota.send_keys(str(competition_data['jumlah_anggota']))
            time.sleep(1)
            
            # Step 18: Fill end date
            print("Step 18: Filling end date...")
            tanggal_selesai = self.driver.find_element(By.ID, "tanggal_selesai")
            tanggal_selesai.clear()
            tanggal_selesai.send_keys(competition_data['tanggal_selesai'])
            time.sleep(1)
            
            # Step 19: Upload pamphlet image
            print("Step 19: Uploading pamphlet image...")
            if competition_data.get('foto_pamflet_path'):
                # Convert relative path to absolute path
                script_dir = Path(__file__).resolve().parent
                absolute_path = (script_dir / competition_data['foto_pamflet_path']).resolve()
                
                print(f"Script directory: {script_dir}")
                print(f"Relative path: {competition_data['foto_pamflet_path']}")
                print(f"Absolute path: {absolute_path}")
                
                if absolute_path.exists():
                    foto_pamflet = self.driver.find_element(By.ID, "foto_pamflet")
                    foto_pamflet.send_keys(str(absolute_path))
                    time.sleep(2)
                    print(f"✅ Image uploaded successfully: {absolute_path.name}")
                else:
                    print(f"❌ Image file not found: {str(absolute_path)}")
            else:
                print("⚠️ No pamphlet image path provided, skipping...")
            
            # Step 20: Click save button
            print("Step 20: Clicking save button...")
            save_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"].btn.btn-primary.ml-2')
            save_button.click()
            time.sleep(3)
            
            print("✅ Competition creation process completed!")
            return True
            
        except Exception as e:
            print(f"❌ Error during competition creation test: {str(e)}")
            return False

def main() -> None:
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
        competition_data: CompetitionData = {
            'nama': 'Test Competition 2024',
            'deskripsi': 'This is a test competition for automation testing purposes. It includes various challenges and tasks.',
            'link_website': 'https://example.com/competition',
            'bidang_keahlian_index': 1,
            'tanggal_mulai': '01-12-2024',
            'penyelenggara_index': 1,
            'tingkat_lomba_index': 1,
            'jumlah_anggota': 3,
            'tanggal_selesai': '31-12-2024',
            'penyelenggara_nama': 'Test Organizer Name',
            'kota_index': 1,
            'foto_pamflet_path': '../../assets/lomba-nasional.jpg'
        }
        
        success = test.test_add_competition(competition_data)
        
        if success:
            print("✅ Complete competition creation test flow completed successfully!")
        else:
            print("❌ Competition creation test failed!")
            
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
    finally:
        input("Press Enter to close the browser...")
        test.teardown()

if __name__ == "__main__":
    main()