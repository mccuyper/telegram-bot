from extension import Convertor

res  = Convertor.get_price(['shekel', 'dollar', 100])
print(res)

# import requests
# import json

# res = requests.get('https://api.exchangerate.host/convert?from=RUB&to=USD')
# print(json.loads(res.content)['info']['rate'])