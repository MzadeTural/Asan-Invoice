document.getElementById('invoiceForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const invoiceInfo = {
        mobile_number: document.getElementById('mobileNumber').value,
        user_id: document.getElementById('userId').value,
        voen: document.getElementById('voen').value,
        service_id: document.getElementById('serviceId').value,
        goods_name: document.getElementById('goodsName').value,
        unit_of_measure: document.getElementById('unitOfMeasure').value,
        price_per_unit: document.getElementById('pricePerUnit').value,
        quantity: document.getElementById('quantity').value,
        value_added_tax: document.getElementById('valueAddedTax').value,
        info_text: document.getElementById('infoText').value
    };

    try {
        const response = await fetch('/submit-invoice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(invoiceInfo)
        });

        const result = await response.json();
        const responseMessage = document.getElementById('responseMessage');
        responseMessage.textContent = result.message;
        responseMessage.style.color = result.status === 'success' ? 'green' : 'red';
    } catch (error) {
        document.getElementById('responseMessage').textContent = "Fatura gönderiminde hata oluştu.";
        document.getElementById('responseMessage').style.color = 'red';
    }
});
