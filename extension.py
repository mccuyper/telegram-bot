import json

import requests

from currency import exchange

class ConverterException(Exception):
	pass


class Convertor:
	@staticmethod
	def get_price(values):
		quote, base, amount = values
		if len(values) != 3:
			raise ConverterException('Error!!!')
		
		if quote == base:
			raise ConverterException(f'You\'ve put the same currency - {base} !')

		try:
			quote_formatted = exchange[quote]
		except KeyError:
			raise ConverterException(f'Unsuccessfully - {quote}')

		try: 
			base_formatted= exchange[base]
		except KeyError:
			raise ConverterException(f'Unsuccessfully - {quote}')   

		try:
			amount = float(amount)
		except ValueError:
			raise ConverterException('too many {amount}')

		r = requests.get(f'https://api.exchangerate.host/convert?from={quote_formatted}&to={base_formatted}')
		result = float(json.loads(r.content)['info']['rate'])*amount
		

		return round(result, 3)