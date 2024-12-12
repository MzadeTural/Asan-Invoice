from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Chrome seçenekleri
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Headless mod
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")

# Kullanıcı bilgileri
mobile_number = "512137388"
user_id = "200184"

# ChromeDriver'ı otomatik yüklemek ve başlatmak
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    print("ASAN İmza giriş sayfasına gidiliyor...")
    driver.get("https://new.e-taxes.gov.az/eportal/az/login/asan")

    # Mobil numara alanını doldur
    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "phone"))
    )
    phone_input.send_keys(mobile_number)

    # Kullanıcı ID alanını doldur
    user_id_input = driver.find_element(By.NAME, "userId")
    user_id_input.send_keys(user_id)

    # Giriş butonuna tıkla
    login_button = driver.find_element(By.ID, "loginPageSignInButton")
    login_button.click()
    #<h4 class="mr-5" id="asanVerificationCode">6960</h4>
    # Vergi ödeyici seçimi sayfası yükleniyor
    code = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "asanVerificationCode"))
        )
    print(f"Asan Code: {code}")
    # BUTA TECH seçimi için şirket adı bulunuyor
    buta_tech = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'BUTA TECH')]"))
    )
    buta_tech.click()

    # Modal penceresini kapatmayı deneyin
    try:
        modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "modal-content"))
        )
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Qəbul')]"))
        )
        accept_button.click()
    except Exception as e:
        print("Modal açılamadı veya kapatılamadı:", str(e))

    # Fatura sayfasına git
    invoice_url = "https://new.e-taxes.gov.az/eportal/az/invoice?page=1"
    driver.get(invoice_url)

    # Faturaları alma işlemi
    invoice_data = []
    while True:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'table-striped')]"))
        )
        rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'table-striped')]//tbody/tr")

        # Sayfa içerisindeki fatura verilerini çek
        for row in rows:
            voen_ad = row.find_element(By.XPATH, ".//td[2]//div[@class='title']/a/div").text
            imzalanma_tarixi = row.find_element(By.XPATH, ".//td[3]/div").text
            status = row.find_element(By.XPATH, ".//td[4]/span").text
            yekun_mebleg = row.find_element(By.XPATH, ".//div[contains(text(), 'Yekun məbləğ')]/following-sibling::div").text
            edv_mebleg = row.find_element(By.XPATH, ".//div[contains(text(), 'ƏDV məbləği')]/following-sibling::div").text
            series_and_number= row.find_element(By.XPATH, ".//div[contains(text(), 'Seriya və nömrə:')]/following-sibling::div").text
            invoice_data.append({
                "voen_ad": voen_ad,
                "imzalanma_tarixi": imzalanma_tarixi,
                "status": status,
                "yekun_mebleg": yekun_mebleg,
                "edv_mebleg": edv_mebleg,
                "series_and_number": series_and_number
            })

        # Sonraki sayfaya geç
        try:
            next_button = driver.find_element(By.ID, "undefined-next")
            if "disabled" not in next_button.get_attribute("class"):
                next_button.click()
                time.sleep(2)  # Sayfanın yüklenmesini beklemek için
            else:
                break  # Eğer "Sonraki" butonu devre dışıysa çık
        except Exception as e:
            print(f"Sonraki sayfaya geçerken hata: {e}")
            break  # Bir hata oluşursa döngüyü kır

    # JSON çıktısı
    print(json.dumps(invoice_data, ensure_ascii=False, indent=4))

except Exception as e:
    print(f"Bir hata oluştu: {e}")

finally:
    driver.quit()
