import telebot
import config
import json

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	res=json.dumps(json.loads(message), indent=2, sort_keys=True)
	print(res)
	bot.send_message(message.chat.id, res)

bot.polling()
