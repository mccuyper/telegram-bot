import os
import telebot
from dotenv import load_dotenv
from pathlib import Path
from currency import exchange
from extension import Convertor, ConverterException
# https://finance.yahoo.com/

import yfinance as yfin

# Taking my API_KEY from .env
dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)

API_KEY=os.getenv('API_KEY')


bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['help', 'start', '?'])
def greet(message):
	bot.reply_to(message, "/currency - available currency to excahge \n e.g.: dollar euro 100 \n /stock - for trending tickers last 2 days\nprice (any stock name) - show current price of stock(4 last minutes) - e.g.: price nflx\n Aso works great for cryptocurrency\n /help for this help-message")


@bot.message_handler(commands=['currency'])
def values(message: telebot.types.Message):
	text = 'Available currency:\n'
	text += '\n'.join(str(key) for key in exchange.keys())
	bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def values(message: telebot.types.Message):
	values = message.text.split(' ')
	values = list(map(str.lower, values))

	try:
		result = Convertor.get_price(values)
	except ConverterException as e:
		bot.reply_to(message,e)
	except Exception as e:
		bot.reply_to(message,e)
	else:
		text = f'PRICE {values[0]} {values[1]} in {values[2]} -- {result} {exchange[values[1]]}'
		bot.reply_to(message, text)



@bot.message_handler(commands=['hello'])
def greet(message):
	bot.send_message(message.chat.id, "Hey, What's going on?")


@bot.message_handler(commands=['stock'])
def get_stocks(message):
	response = ""
	stocks = ['amc', 'nok', 'gme', 'aapl', 'tsla', 'amzn', 'fb', 'goog', 'nflx']
	stock_data = []
	for stock in stocks:
		data = yfin.download(tickers=stock, period='2d', interval='1d')
		data = data.reset_index()
		response+=f'======{stock}======\n'
		stock_data.append([stock])
		columns = ['stock']
		for index, row in data.iterrows():
			stock_position = len(stock_data) - 1
			price = round(row['Close'], 2)
			format_date = row['Date'].strftime('%m/%d')
			response += f"{format_date}: {price}\n"
			stock_data[stock_position].append(price)
			columns.append(format_date)
		print("\n")

	response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"


	for row in stock_data:
		response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
	response += "\nStock Data"
	print(response)
	bot.send_message(message.chat.id, response)

def stock_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "price":
    return False
  else:
    return True



@bot.message_handler(func=stock_request)
def send_price(message):
  request = message.text.split()[1]
  data = yfin.download(tickers=request, period='5m', interval='1m')
  if data.size > 0:
    data = data.reset_index()
    data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
    data.set_index('format_date', inplace=True)
    print(data.to_string())
    bot.send_message(message.chat.id, data['Close'].to_string(header=False))
  else:
    bot.send_message(message.chat.id, "No data!")

bot.polling(none_stop=True, interval=0)
