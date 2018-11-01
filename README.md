# ALFAcoins.com API library for Python 2/3

Start accept crypto assets(bitcoin BTC, litecoin LTC, bitcoincash BCH, ethereum ETH, ripple XRP, dash DASH, litecointestnet LTCT) in your python application.

Documentation: https://www.alfacoins.com/developers

Usage example:
```
import ALFAcoins

alfacoins = ALFAcoins('apicontest', '07fc884cf02af307400a9df4f2d15490', 'aIXncDlApUS4nexB', True)
new_order = alfacoins.createOrder({
    'type': 'bitcoin',
    'amount': 1.23412341,
    'order_id': 'Order10001',
    'currency': 'USD',
    'description': 'Payment for t-shirt ALFAcoins size XXL'
})
print(new_order)
print(new_order['address'])
```
# Test notifications
You can test notifications which should be sent to notificationURL without any payments.
```
import ALFAcoins

alfacoins = ALFAcoins('apicontest', '07fc884cf02af307400a9df4f2d15490', 'aIXncDlApUS4nexB', True)
new_order = alfacoins.createTestOrder('https://yoururl.com', 'completed', 'litecointestnet')
print(new_order)
```
# API methods
- createOrder(params_dict)
- orderStatus(order_id)
- createTestOrder(url, status, currency_type)
- bitsend(params_dict)
- bitsendStatus(bitsend_id)
- getStats()
- refundOrder(params_dict)
- getFees()
- rate(from_currency, to_currency)
- getRates()
- convert(from, to, amount)


More information inside of code and on https://www.alfacoins.com/developers. Ask me any questions to issues.

# Donate me
Buy me a coffee(ETH or tokens at 0x502372a32Ff5cf229Db185057f82da57E1DA85e2)

Donate me BTC/ETH/LTC/BCH/XRP/DASH https://www.alfacoins.com/donation/lisovskij
Thank you.
