import requests
import json
import telebot
from confing import TOKEN, keys
from utils import ConversionException, MoneyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\nКоличество переводимой валюты > \
имя вылюты > в какую валюту перевести.\nПример: доллар рубль 1\n Увидеть весь список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()


        if len(values) != 3:
            raise ConversionException('Слишком много параметров.')

        amount, base, quote = values
        total = MoneyConverter.convert(amount, base, quote)


    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя,\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать комманду\n{e}')
    else:
        url = (f'https://api.apilayer.com/exchangerates_data/convert?to={keys[quote]}&from={keys[base]}&amount={amount}')
        r = requests.request("GET", url, headers={"apikey": "d9bxLmk3jhTHrcMuQtAEiTieVW7U77pf"})
        total = json.loads(r.content)
        result = total['result']
        text = f'Цена {amount} {base} в {quote} - {result}'
        bot.send_message(message.chat.id, text)


bot.polling()
