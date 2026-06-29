import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestSensoryLabRegression(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Inisialisasi WebDriver dijalankan sekali untuk semua test case
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.base_url = "http://localhost:8000"

    # ==========================================
    # MODUL PANELIS (TC-01 sampai TC-05)
    # ==========================================

    def test_tc_01_login_panelis(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "email").send_keys("panelis@sensorylab.com")
        self.driver.find_element(By.ID, "password").send_keys("password123")
        self.driver.find_element(By.ID, "btn-login").click()
        
        # Ekspektasi: URL berubah ke dashboard
        self.wait.until(EC.url_contains("/panelis/dashboard"))
        self.assertTrue("/panelis/dashboard" in self.driver.current_url)

    def test_tc_02_dashboard_panelis_tampil_daftar_uji(self):
        # Asumsi sudah berada di dashboard
        tabel_uji = self.wait.until(EC.presence_of_element_located((By.ID, "tabel-daftar-uji")))
        self.assertTrue(tabel_uji.is_displayed())

    def test_tc_03_form_sensori_autosave(self):
        self.driver.get(f"{self.base_url}/panelis/form-uji/1")
        self.driver.find_element(By.ID, "skala_rasa").send_keys("8")
        
        # Ekspektasi: Muncul indikator "Menyimpan..." tanpa menekan submit
        indikator_autosave = self.wait.until(EC.visibility_of_element_located((By.ID, "indikator-autosave")))
        self.assertIn("Tersimpan otomatis", indikator_autosave.text)

    def test_tc_04_form_sensori_validasi_kosong(self):
        self.driver.get(f"{self.base_url}/panelis/form-uji/1")
        # Sengaja tidak mengisi apa-apa langsung klik submit
        self.driver.find_element(By.ID, "btn-submit-uji").click()
        
        # Ekspektasi: Muncul error validasi
        pesan_error = self.wait.until(EC.visibility_of_element_located((By.ID, "error-alert"))).text
        self.assertTrue("wajib diisi" in pesan_error.lower())

    def test_tc_05_form_sensori_submit_sukses(self):
        self.driver.get(f"{self.base_url}/panelis/form-uji/1")
        self.driver.find_element(By.ID, "skala_rasa").send_keys("8")
        self.driver.find_element(By.ID, "skala_tekstur").send_keys("7")
        self.driver.find_element(By.ID, "komentar_panelis").send_keys("Tekstur empuk.")
        self.driver.find_element(By.ID, "btn-submit-uji").click()
        
        # Ekspektasi: Muncul notifikasi sukses dan kembali ke dashboard
        notif_sukses = self.wait.until(EC.visibility_of_element_located((By.ID, "notif-sukses"))).text
        self.assertIn("berhasil dikirim", notif_sukses.lower())

    # ==========================================
    # MODUL QC & ALAT (TC-06 sampai TC-08, TC-10)
    # ==========================================

    def test_tc_06_qc_buka_form_input_alat(self):
        self.driver.get(f"{self.base_url}/qc/dashboard")
        # Klik batch pertama yang aktif
        self.driver.find_element(By.CLASS_NAME, "btn-pilih-batch").click()
        
        form_alat = self.wait.until(EC.presence_of_element_located((By.ID, "form-input-alat")))
        self.assertTrue(form_alat.is_displayed())

    def test_tc_07_qc_input_angka_valid(self):
        self.driver.find_element(By.ID, "input_shear_force").send_keys("250.5")
        self.driver.find_element(By.ID, "btn-simpan-alat").click()
        
        notif_sukses = self.wait.until(EC.visibility_of_element_located((By.ID, "notif-simpan"))).text
        self.assertIn("data tersimpan", notif_sukses.lower())

    def test_tc_08_qc_input_format_huruf_ditolak(self):
        self.driver.get(f"{self.base_url}/qc/form-alat/1")
        self.driver.find_element(By.ID, "input_shear_force").send_keys("duaratus") # Sengaja input teks
        self.driver.find_element(By.ID, "btn-simpan-alat").click()
        
        error_format = self.wait.until(EC.visibility_of_element_located((By.ID, "error-format"))).text
        self.assertTrue("harus berupa angka" in error_format.lower())

    def test_tc_10_qc_dashboard_tampil_pass_fail(self):
        self.driver.get(f"{self.base_url}/qc/evaluasi-batch/1")
        # Ekspektasi: Ada elemen badge (label) yang menampilkan teks PASS atau FAIL
        badge_status = self.wait.until(EC.presence_of_element_located((By.ID, "badge-status-batch")))
        teks_status = badge_status.text.upper()
        self.assertTrue(teks_status == "PASS" or teks_status == "FAIL")

    # ==========================================
    # MODUL R&D ANALITIK (TC-09)
    # ==========================================

    def test_tc_09_rnd_compare_batch(self):
        self.driver.get(f"{self.base_url}/rnd/compare")
        # Centang 2 batch untuk dicompare
        checkboxes = self.driver.find_elements(By.CLASS_NAME, "cb-batch")
        checkboxes[0].click()
        checkboxes[1].click()
        self.driver.find_element(By.ID, "btn-compare").click()
        
        # Ekspektasi: Muncul elemen canvas (grafik dari Chart.js/sejenisnya)
        grafik = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "canvas")))
        self.assertTrue(grafik.is_displayed())

    @classmethod
    def tearDownClass(cls):
        # Menutup browser setelah seluruh 10 test case selesai dijalankan
        time.sleep(2)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)
