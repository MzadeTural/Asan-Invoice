import requests
import json

# 1. First Service: Verify User Information and Send SMS Code
def check_first_information():
    url = "https://services.tacreocard.com/Api_v1/check_First_Informations"

    payload = {
        "affiliate_id": 3,
        "hash": "DKt9lokl8g9eNQ2nv2zufhUGvgmm4wltXTsaTwSbFIV0wXexEYgueJZl1ylQVv5F4zJXTomEfrSG4t2xKKyTkx654P2LerZHLwflNEUUSToPIADM6SOqizQ7V3gh9tot",
        "amount": 150.50,
        "order_id": 123456789,
        "card_number": 1865030924658074,
        "expiration_month": 8,
        "expiration_year": 27,
        "cvv": 541
    }

    headers = {
        "Content-Type": "application/json"
    }

    print("Sending request to First Service...")
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Yanıt başlıklarını ve içerik türünü yazdır
    print("Response Status Code:", response.status_code)
    print("Response Headers:", response.headers)

    if response.status_code == 403:
        print("Access Denied: Check your credentials and IP restrictions.")
        print("Response Text:", response.text)
    elif response.status_code != 200:
        print("Unexpected Error:", response.text)
    else:
        try:
            response_data = response.json()
            print("Response JSON:", response_data)
            return response_data
        except json.JSONDecodeError:
            print("Error: Response is not JSON.")
            print("Raw Response Text:", response.text)

    return None


# 2. Second Service: Process Payment
def process_payment(order_id, payment_code):
    url = "https://services.tacreocard.com/Api_v1/payment"

    payload = {
        "affiliate_id": 3,
        "hash": "DKt9lokl8g9eNQ2nv2zufhUGvgmm4wltXTsaTwSbFIV0wXexEYgueJZl1ylQVv5F4zJXTomEfrSG4t2xKKyTkx654P2LerZHLwflNEUUSToPIADM6SOqizQ7V3gh9tot",
        "order_id": order_id,
        "payment_code": payment_code  # 6-digit SMS code
    }

    headers = {
        "Content-Type": "application/json"
    }

    print("\nSending request to Second Service...")
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Print response
    print("Response Status Code:", response.status_code)
    print("Response Body:", response.json())

    return response.json()


# 3. Third Service: Check Payment Status (Optional)
def check_payment_status(order_id):
    url = "https://services.tacreocard.com/Api_v1/check_payment"

    payload = {
        "affiliate_id": 3,
        "hash": "DKt9lokl8g9eNQ2nv2zufhUGvgmm4wltXTsaTwSbFIV0wXexEYgueJZl1ylQVv5F4zJXTomEfrSG4t2xKKyTkx654P2LerZHLwflNEUUSToPIADM6SOqizQ7V3gh9tot",
        "order_id": order_id
    }

    headers = {
        "Content-Type": "application/json"
    }

    print("\nSending request to Third Service (Check Payment Status)...")
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Print response
    print("Response Status Code:", response.status_code)
    print("Response Body:", response.json())

    return response.json()


# Main Execution
if __name__ == "__main__":
    # Step 1: Call the first service
    first_response = check_first_information()

    if first_response == 1 or first_response == -5:
        print("\nFirst Service Success: Proceeding to Payment")
        order_id = 123456789  # Same order ID used in the first request
        payment_code = input("Enter the 6-digit SMS code: ")  # Get SMS code from user input

        # Step 2: Process the payment
        second_response = process_payment(order_id, int(payment_code))

        if second_response == 1 or second_response == 2:
            print("\nPayment Successful. Checking Payment Status...")
            # Step 3: Optionally check payment status
            check_payment_status(order_id)
        else:
            print("\nPayment Failed. Response:", second_response)
    else:
        print("\nFirst Service Failed. Response:", first_response)
