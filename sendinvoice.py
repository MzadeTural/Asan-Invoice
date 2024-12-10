from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Kullanıcı bilgileri
mobile_number = "512137388"
user_id = "200184"
voen = "2003715341"
service_id="9962022000"
goods_name="Test"
unit_of_measure="ədəd"
price_per_unit="1"
quantity="1"
value_aded_tax="1"
info_text="asd asd"

# ChromeDriver'ı otomatik yüklemek ve başlatmak
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

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

    # Vergi ödeyici seçimi sayfası yükleniyor
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, "//h5[contains(text(), 'İnternet Vergi İdarəsi')]"))
    )
   
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
    print("Fatura sayfası açıldı, 'Təqdim etmə' seçeneği seçiliyor...")
    try:
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
    except Exception as e:
        print("Dropdown açılırken hata oluştu:", str(e))

    voen_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "react-select-2-input"))
    )
    voen_input.send_keys(voen)
    voen_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'css-11jo8p4-menu')]"))
        )
    voen_button.click()
    cont_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Davam et')]"))
        )
    cont_button.click()

    service_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "productGroupCode"))
    )
    service_input.send_keys(service_id) 
    time.sleep(2)   
    service_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'XİDMƏTLƏR')]"))
        )
    service_button.click()
    print("Qaimə doldurulmağa başlanılır:")
    grid_select = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ReactVirtualized__Grid__innerScrollContainer')]"))
    )
    grid_select.click()

    product_name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "productName"))
    )
    product_name_input.send_keys(goods_name) 

    product_name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "productName"))
    )
    product_name_input.send_keys(goods_name) 

    unit_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "unit"))
    )
    unit_input.send_keys(unit_of_measure) 

    price_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "pricePerUnit"))
    )
    price_input.send_keys(price_per_unit)

    quantity_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "quantity"))
    )
    quantity_input.send_keys(quantity)    

    vat_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "vat18"))
    )
    vat_input.send_keys(value_aded_tax) 
   
    time.sleep(1)  
    add_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Əlavə et')]"))
    )
    add_button.click()
    time.sleep(2) 
   
    info_text_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "note1"))
    )
    info_text_input.send_keys(info_text)
    time.sleep(1)
    sign_send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'İmzala və göndər')]"))
        )
    sign_send_button.click()
    time.sleep(1)
    confrm_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Təsdiq et')]"))
        )
    confrm_button.click()


    time.sleep(10)
finally:
         driver.quit()
