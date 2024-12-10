from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
app = Flask(__name__)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Headless mod
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
# Selenium ile Fatura Oluşturma Fonksiyonu
def submit_invoice(invoice_info):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    try:
        messages = []
        print("ASAN İmza giriş sayfasına gidiliyor...")
        driver.get("https://new.e-taxes.gov.az/eportal/az/login/asan")

        # Mobil numara ve kullanıcı ID'sini çekin
        phone_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "phone"))
        )
        phone_input.send_keys(invoice_info["mobile_number"])

        user_id_input = driver.find_element(By.NAME, "userId")
        user_id_input.send_keys(invoice_info["user_id"])

        # Giriş butonuna tıklayın
        login_button = driver.find_element(By.ID, "loginPageSignInButton")
        login_button.click()

        # Vergi ödeyici seçimi sayfası yükleniyor
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h5[contains(text(), 'İnternet Vergi İdarəsi')]"))
        )
        try:
            # Modal açılırsa, doğrulama kodunu al
            verification_code = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "asanVerificationCode"))
            )
            
                          
            print("Doğrulama kodu:", verification_code.text)
            messages.append(verification_code.text)
            # return {"status": "success", "message": "Fatura başarıyla gönderildi", "verification_code": verification_code_text}
           
        except Exception as e:
         print("Modal açılamadı veya kapatılamadı:", str(e))       
        # Şirket seçimi (BUTA TECH)
        buta_tech = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'BUTA TECH')]"))
        )
        buta_tech.click()

        # Modal penceresini kapatma
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

        # Faturayı alma işlemi
        print("Fatura sayfası açıldı, 'Təqdim etmə' seçeneği seçiliyor...")
        dropdown_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'jss28')]"))
        )
        dropdown_button.click()

        # Seçeneği bul ve tıkla
        invoice_option = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(@id, 'defaultInvoice')]"))
        )
        invoice_option.click()
        print("Seçenek başarıyla seçildi.")

        # VOEN bilgilerini gir
        voen_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "react-select-2-input"))
        )
        voen_input.send_keys(invoice_info["voen"])
        time.sleep(1)
        voen_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'css-11jo8p4-menu')]"))
        )
        voen_button.click()

        cont_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Davam et')]"))
        )
        cont_button.click()

        # Diğer bilgileri doldurun
        service_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "productGroupCode"))
        )
        service_input.send_keys(invoice_info["service_id"])
        time.sleep(2)   

        service_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'XİDMƏTLƏR')]"))
        )
        service_button.click()
        print("Qaimə doldurulmaya başlanılıyor...")

        grid_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ReactVirtualized__Grid__innerScrollContainer')]"))
        )
        grid_select.click()

        product_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "productName"))
        )
        product_name_input.send_keys(invoice_info["goods_name"])

        unit_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "unit"))
        )
        unit_input.send_keys(invoice_info["unit_of_measure"])

        price_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "pricePerUnit"))
        )
        price_input.send_keys(invoice_info["price_per_unit"])

        quantity_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "quantity"))
        )
        quantity_input.send_keys(invoice_info["quantity"])

        vat_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "vat18"))
        )
        vat_input.send_keys(invoice_info["value_added_tax"])

        time.sleep(1)
        add_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Əlavə et')]"))
        )
        add_button.click()
        time.sleep(2)

        info_text_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "note1"))
        )
        info_text_input.send_keys(invoice_info["info_text"])
        time.sleep(1)

        sign_send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'İmzala və göndər')]"))
        )
        sign_send_button.click()
        time.sleep(1)

        confrm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Təsdiq et')]"))
        )
        confrm_button.click()

        time.sleep(10)
        print("Fatura başarıyla oluşturuldu ve gönderildi.")
       
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        driver.quit()

# Ana Sayfa - Form Gösterimi
@app.route('/')
def invoice_form():
    return render_template('invoice_form.html')

# Fatura Gönderimi - POST İsteği
@app.route('/submit-invoice', methods=['POST'])
def handle_invoice_submission():
    invoice_info = request.json
    result = submit_invoice(invoice_info) 
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
