from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

# Function to fetch invoices using Selenium
def fetch_invoices(mobile_number, user_id):
    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    invoice_data = []

    try:
        driver.get("https://new.e-taxes.gov.az/eportal/az/login/asan")

        # Fill in phone and user ID
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "phone"))
        ).send_keys(mobile_number)

        driver.find_element(By.NAME, "userId").send_keys(user_id)
        driver.find_element(By.ID, "loginPageSignInButton").click()

        # Wait for company selection and select 'BUTA TECH'
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'BUTA TECH')]"))
        ).click()

        # Handle modal if it appears
        try:
            modal = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "modal-content"))
            )
            driver.find_element(By.XPATH, "//button[contains(text(), 'Qəbul')]").click()
        except:
            pass  # Modal not present

        # Navigate to invoice page
        driver.get("https://new.e-taxes.gov.az/eportal/az/invoice?page=1")

        # Loop through pages and collect invoices
        while True:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'table-striped')]"))
            )
            rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'table-striped')]//tbody/tr")

            for row in rows:
                voen_ad = row.find_element(By.XPATH, ".//td[2]//div[@class='title']/a/div").text
                imzalanma_tarixi = row.find_element(By.XPATH, ".//td[3]/div").text
                status = row.find_element(By.XPATH, ".//td[4]/span").text
                yekun_mebleg = row.find_element(By.XPATH, ".//div[contains(text(), 'Yekun məbləğ')]/following-sibling::div").text
                edv_mebleg = row.find_element(By.XPATH, ".//div[contains(text(), 'ƏDV məbləği')]/following-sibling::div").text

                invoice_data.append({
                    "voen_ad": voen_ad,
                    "imzalanma_tarixi": imzalanma_tarixi,
                    "status": status,
                    "yekun_mebleg": yekun_mebleg,
                    "edv_mebleg": edv_mebleg
                })

            # Move to the next page
            try:
                next_button = driver.find_element(By.ID, "undefined-next")
                if "disabled" not in next_button.get_attribute("class"):
                    next_button.click()
                    time.sleep(2)  # Wait for the next page to load
                else:
                    break
            except:
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    return invoice_data

# Flask route to create an API endpoint
@app.route('/fetch-invoices', methods=['POST'])
def fetch_invoices_api():
    # Get input data from the API request
    data = request.json
    mobile_number = data.get('mobile_number')
    user_id = data.get('user_id')

    if not mobile_number or not user_id:
        return jsonify({"error": "Please provide 'mobile_number' and 'user_id'"}), 400

    # Fetch invoices
    result = fetch_invoices(mobile_number, user_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
