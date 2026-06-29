from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Inisialisasi Browser
driver = webdriver.Chrome()

try:
    # 1. Buka halaman aplikasi (Asumsi sudah melewati login dan berada di form pengujian)
    print("Membuka form uji sensori SensoryLab...")
    driver.get("http://localhost:8000/panelis/form-uji/batch-123")
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)
    
    # 2. Mengisi parameter rasa (Asumsi input berupa dropdown atau radio button, kita pakai input text/number)
    print("Mengisi nilai rasa (Manis)...")
    input_rasa = wait.until(EC.presence_of_element_located((By.ID, "skala_rasa")))
    input_rasa.send_keys("8") # Skala 1-10 sesuai aturan bisnis

    # 3. SENGAJA MENGOSONGKAN PARAMETER TEKSTUR 
    # (Untuk memicu error validasi sesuai acceptance criteria US 1.4)
    print("Sengaja melewati input tekstur untuk mengetes validasi...")
    # input_tekstur = driver.find_element(By.ID, "skala_tekstur")
    # input_tekstur.send_keys("7") -> Bagian ini tidak dieksekusi

    # 4. Mengisi komentar
    input_komentar = driver.find_element(By.ID, "komentar_panelis")
    input_komentar.send_keys("Rasanya pas, tapi saya lupa ngisi teksturnya.")

    # 5. Klik tombol Submit
    print("Menekan tombol submit...")
    submit_button = driver.find_element(By.ID, "btn-submit-uji")
    submit_button.click()

    # 6. Verifikasi pesan error muncul (Assertion)
    # Ekspektasi: Sistem memunculkan alert/teks error "Semua field wajib diisi!"
    error_message_element = wait.until(EC.visibility_of_element_located((By.ID, "error-alert")))
    pesan_error = error_message_element.text

    if "wajib diisi" in pesan_error.lower() or "tidak boleh kosong" in pesan_error.lower():
        print(f"Test Case PASSED: Sistem berhasil memblokir submit dan menampilkan error: '{pesan_error}'")
    else:
        print("Test Case FAILED: Sistem tidak memunculkan pesan error yang sesuai.")

except Exception as e:
    print(f"Test Case ERROR: Terjadi kegagalan eksekusi -> {e}")

finally:
    # Jeda sejenak agar bisa melihat hasilnya sebelum browser tertutup
    time.sleep(3)
    driver.quit()
