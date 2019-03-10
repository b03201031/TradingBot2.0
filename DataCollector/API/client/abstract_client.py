import hashlib
import hmac
import requests
from abc import ABCMeta, abstractmethod


class AbstractClient(ABCMeta):


	def __init__(self, api_key, api_secret, helper,config, requests_params=None):
		self.helper = helper
		self.CONFIG = config
		self.API_KEY = api_key
		self.API_SECRET = api_secret
		self.session = self._init_session()
		self._request_params = requests_params	


	def load_config(self, path):
		'''
		load config of api
		:param path : path to file with above variables
		'''	

	def load_key(self, path):
		'''
		load key and secet from file
		:param path : path to file with first two line are key, secret respectively	
		'''
		with open(path, 'r') as f:
			self.key = f.readline().strip()
			self.secret = f.readline().strip()


	def _init_session(self, **headers):
		
		'''
		:param **header: global header of session, 
		eg: {'Accept': 'application/json',
             'User-Agent': 'binance/python',
             'X-MBX-APIKEY': self.API_KEY}
		'''
		session = requests.session()
		session.headers.update(headers)

		return session

	@abstractmethod
	def _create_api_uri(self, path, signed=True, version=self.CONFIG['VERSION']['PUBLIC']):
		'''
		:param path: path of api
		:param signed: sign or not
		:version: version of api 
		:return example: self.API_URL + '/' + self.PRIVATE_VERSION/ 
		'''

	@abstractmethod
	def _generate_signature(self, data):
		'''generate signature'''	
		
	@abstractmethod
	def _sign_payload(self, data):
		'''
		convert params to list with signature
		'''

	@abstractmethod
	def _request(self, method, uri, signed, force_params=False, **kwargs):
		'''
		 base method for request
		'''


	def _request_api(self, method, path, version=self.CONFIG['VERSION']['PUBLIC'], signed=False)
		#vesrion is used to control uri
		uri = self._create_api_uri(path, signed, version)

		return self._request(method, uri, signed, **kwargs)

	def _request_withdraw_api(self, method, path, signed=False, **kwargs):
		uri = self._create_withdraw_api_uri(path)

		return self._request(method, uri, signed, **kwargs)

	@abstractmethod
	_handle_response(self, response):
	'''
	Internal helper for handling exception
	raise exception or return response.json()
	'''

	def _get(self, path, version=self.CONFIG['VERSION']['PUBLIC'], signed=False, **kwargs):
		return self._request_api('get', path, version, signed, **kwargs)

	def _post(self, path, version=self.CONFIG['VERSION']['PUBLIC'], signed=False, **kwargs):
		return self._request_api('post', path, version, signed, **kwargs)

	def _put(self, path, version=self.CONFIG['VERSION']['PUBLIC'], signed=False, **kwargs):
		return self._request_api('put', path, version, signed, **kwargs)

	def _delete(self, path, version=self.CONFIG['VERSION']['PUBLIC'], signed=False, **kwargs):
		return self._request_api('put', path, version. signed. **kwargs)

	def get_klines(self, **params):
		'''
		:return: api response
		'''
		return self._get(self.CONFIG['PATH']['KLINE'], data=params)

	@abstractmethod
	def _get_earlist_valid_timestamp(sel, symbol, interval):
		'''
		:param symbol: Name of symbol pair
		:type symbol: str
		:param interval: kline interval
		:type interval: str

		:return: first valid timestamp
		'''
	def get_historical_klines(self, symbol, interval, start_str, end_str, limit=500):
		output_data = []

		interval = self.helper.interval_to_timeframe(interval)

		#convert date string to target timeframe
		if type(start_str) == int:
			start_ts = start_str
		else:
			start_str = self.helper.date_to_timeframe(start_str)

		#establish first available timestamp
		first_valid_ts = self._get_earlist_valid_timestamp(symbol, interval)
		start_ts = max(start_ts, first_valid_ts)

		end_ts = None

		if end_str:
			if type(end_str) == int:
				end_ts = end_str
			else:
				end_ts = self.helper.date_to_timeframe(end_str)

		idx = 0

		while True:
			temp_data = self.get_klines(
				symbol=symbol,
				interval=interval,
				limit=limit,
				startTime=start_ts,
				endTime=end_ts
				)

			# handle the case where exactly the limit amount of data was returned was returned last loop
			if not len(temp_data):
				break

			# append this loop data to output data
			output_data += temp_data
			idx += 1

			# check if we receive less than the required limit and exit the loop
			if len(temp_data) < limit:
				break


			# increment next call by our timeframe
			start_ts += interval

			#sleep after every 3rd call to be kind to the API
			if idx % 3 == 0:
				time.sleep(1)

		return output_data


