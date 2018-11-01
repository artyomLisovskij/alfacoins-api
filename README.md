# ALFAcoins.com API library for Python 2/3

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
