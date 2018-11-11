import json
from hashlib import md5
import logging
from inspect import getmembers

try:
    from urllib.request import Request, urlopen  # Python 3
    from urllib.error import HTTPError
    from urllib.parse import urlencode, quote_plus
except ImportError as e:
    from urllib2 import Request, urlopen  # Python 2
    from urllib2 import HTTPError
    from urllib import urlencode, quote_plus


class ALFAcoins():
    '''
        Documentation: https://www.alfacoins.com/developers
        Usage example:
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
    '''

    url = 'https://www.alfacoins.com/api/'

    def __init__(self, name, secret_key, password, logging_params=False):
        '''
        name = (str) Shop Name of API which you assigned when you create the API
        secret_key = (str) Secret key which is given after API was created
        password = (str) raw password from API
        logging = (dict | True for default settings) 
            level = (str) [DEBUG/INFO/WARNING/ERROR] Logging level  (default = 'DEBUG')
            log_to = (dict) 
                type = (str) [file/console] Logging type (default = 'console')
                filename = (str) name of file (default = 'alfacoins.log')
            log_format = (str) output format (default = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        '''
        self.name = name
        self.secret_key = secret_key
        self.password = self.make_md5(password)
        
        if logging_params:
            logging_levels = ['ERROR', 'WARNING', 'INFO', 'DEBUG']

            # set logging handler
            handler = logging.StreamHandler()
            if isinstance(logging_params, dict) and 'log_to' in logging_params:
                if 'type' in logging_params['log_to']:
                    if logging_params['log_to']['type'] == 'file':
                        log_filename = 'alfacoins.log'
                        if 'filename' in logging_params['log_to']:
                            log_filename = logging_params['log_to']['filename']
                        handler = logging.FileHandler(filename=log_filename)

            # set logging formatter
            logging_formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            if isinstance(logging_params, dict) and 'log_format' in logging_params:
                logging_formatter = logging_params['log_format']
            handler.setFormatter(logging.Formatter(logging_formatter))

            self.log = logging.getLogger('alfacoins_api')
            self.log.addHandler(handler)

            # set logging level
            if isinstance(logging_params, dict) and 'level' in logging_params and logging_params['level'] in logging_levels:
                self.log.setLevel(getattr(logging, logging_params['level']))
            else:
                self.log.setLevel(logging.getLevelName('DEBUG'))
            '''
            Logger usage:
            self.log.debug('debug message')
            self.log.info('info message')
            self.log.warn('warn message')
            self.log.error('error message')
            '''
        else:
            self.log = False

    def make_md5(self, s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest().upper()

    def Request(self, request_method, command='', params={}):
        '''
        request_method = (str) [GET/POST] Request method
        command = (str) Request url
        params = (dict) Parameters to request
        '''
        req = False
        if request_method.lower() == 'get':
            if params:
                encoded_params = urlencode(params, quote_via=quote_plus)
                req = Request(self.url + command + '?' + encoded_params, headers={'Content-Type': 'application/json'})
            else:
                req = Request(self.url + command, headers={'Content-Type': 'application/json'})
        elif request_method.lower() == 'post':
            params.update({'name': self.name,
                       'secret_key': self.secret_key,
                       'password': self.password
                       })
            params_json = json.dumps(params).encode("utf-8")
            req = Request(self.url + command, data=params_json, headers={'Content-Type': 'application/json'})

        if req:
            request_info_string = 'Requested: ' + str(request_method).upper() + ' /' + str(command)
            params_string = ''
            if params:
                params_string = '\nParameters(encoded): ' + urlencode(params)
            if self.log:
                self.log.info(request_info_string + params_string)
            try:
                response      = urlopen(req)
                status_code   = response.getcode()
                response_body = response.read()
            except HTTPError as e:
                status_code   = e.getcode()
                response_body = e.read()
            
            response_info_string = '\nResponse code: ' + str(status_code) + '\nResponse body: ' + str(response_body)
            if self.log:
                self.log.debug(response_info_string)
            json_object = False
            try:
                json_object = json.loads(response_body)
            except Exception as e:
                if self.log:
                    self.log.error(request_info_string + params_string + response_info_string)
            if json_object:
                if 'error' in json_object:
                    if self.log:
                        self.log.warn(json_object)
            if self.log:
                self.log.info(json_object)
            return json_object
        else:
            raise ValueError('Wrong request_method')

    '''
    
    API METHODS

    '''

    def createOrder(self, params={}):
        """ Create order for payment """
        return self.Request('post', 'create', params)

    def createTestOrder(self, notificationURL, status='completed', type='litecointestnet'):
        """ You can test notifications which should be sent to notificationURL without any payments.  """
        params = {
          "type": type,
          "amount": 1.23412341,
          "order_id": "Order10001",
          "currency": "USD",
          "description": "Payment for t-shirt ALFAcoins size XXL",
          "options": {
                        "notificationURL": notificationURL,
                        "redirectURL": "https://www.alfacoinshop.com/my/orders/success",
                        "payerName": "Victor",
                        "payerEmail": "no_reply@alfacoins.com",
                        "test": 1,
                        "status": status
                      }
        }
        return self.Request('post', 'create', params)

    def orderStatus(self, order_id):
        """ Get status of created Order """
        params = {
            'txn_id': int(order_id)
        }
        return self.Request('post', 'status', params)

    
    def bitsend(self, params={}):
        """ BitSend primary use to payout salaries for staff or making direct deposits to different cryptocurrency addresses """
        return self.Request('post', 'bitsend', params)


    def bitsendStatus(self, bitsend_id):
        """ BitSend status primary use to get information of bitsend payout """
        params = {
            'bitsend_id': int(bitsend_id)
        }
        return self.Request('post', 'bitsend_status', params)

    def getStats(self):
        """ Merchant's volume and balance statistics """
        return self.Request('post', 'stats')

    def refundOrder(self, params={}):
        """ Refund completed order """
        return self.Request('post', 'refund', params)

    def getFees(self):
        """ Get all gate fees for deposit and withdrawal """
        return self.Request('get', 'fees')

    def rate(self, from_currency, to_currency):
        """ Get rate for pair of symbols """
        return self.Request('get', 'rate/' + from_currency + '_'+ to_currency + '.json')

    def getRates(self):
        """ Get rate for all available pairs """
        return self.Request('get', 'rates')

    def convert(self, from_currency, to_currency, amount=1):
        """ Converts amount from some currency to some currency """
        params = {
            'pair': from_currency + '_'+ to_currency,
            'amount': float(amount)
        }
        return self.Request('get', 'convert', params)

def test_ALFAcoins():
    import random # for random generation of order_id only
    alfacoins = ALFAcoins('apicontest', '07fc884cf02af307400a9df4f2d15490', 'aIXncDlApUS4nexB', True)
    new_order = alfacoins.createOrder({
        'type': 'litecointestnet',
        'amount': 1.23412341,
        'order_id': 'Order' + str(random.randint(1, 1000000)),
        'currency': 'USD',
        'description': 'Payment for t-shirt ALFAcoins size XXL'
    })
    print(new_order)
    alfacoins.orderStatus(new_order['id'])
    
# Test:
# test_ALFAcoins()
