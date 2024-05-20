def extract_currency_data(data, currencies):
    rates = {}
    for record in data:
        if not record:
            continue
        date = record['date']
        rates[date] = {}
        for currency in currencies:
            currency_data = next((item for item in record['exchangeRate'] if item['currency'] == currency), None)
            if currency_data:
                rates[date][currency] = {
                    'sale': currency_data.get('saleRate', 'N/A'),
                    'purchase': currency_data.get('purchaseRate', 'N/A')
                }
    return rates

