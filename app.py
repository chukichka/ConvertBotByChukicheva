import telebot
from config import keys, TOKEN
from extensions import ConvertionException, Converter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = "Привет! Я Бот-Конвертер, созданный Натальей Чукичевой в рамках обучения на курсе 'Тестировщик-автоматизатор на Python'.\n" \
           "\nЧто я могу?\n1. Произвести конвертацию валют через команду <имя валюты> <имя валюты, в которую хотите перевести> <количество переводимой валюты>. " \
           "Например, у вас есть 1000 рублей и вы хотите поменять их на доллары. Тогда ваша команда будет выглядеть так: рубль доллар 1000" \
"\n2. Вывести список доступных валют по команде /values.\n3. Вызвать инструкцию по использованию бота по команде /help."
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = "Функционал бота:\n1. Произвести конвертацию валют через команду <имя валюты> <имя валюты, в которую хотите перевести> <количество переводимой валюты>. " \
           "Например, у вас есть 1000 рублей и вы хотите поменять их на доллары. Тогда ваша команда будет выглядеть так: рубль доллар 1000" \
"\n2. Вывести список доступных валют по команде /values."
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    text += "\n\nВнимание! В запросах используйте формулировку из списка."
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise ConvertionException('Введено неверное количество параметров.')

        base, quote, amount = values
        total_quote = Converter.get_price(base, quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \'{e}\'.')
    else:
        text = f'Переводим {base} в {quote}:\n{amount} {base} = {round(float(total_quote) * float(amount), 2)} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling()
