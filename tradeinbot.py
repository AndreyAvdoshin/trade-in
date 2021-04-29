import telebot
from pyzbar.pyzbar import decode
from PIL import Image
import save_db as save
import requests
import get_answer as function

TOKEN = "1736190330:AAE6LV_-VnyzKKvrxKqwixth-vnXjem0Qko"
bot = telebot.TeleBot(TOKEN)

exceptions = ['xbox', 'xbox one', 'switch', '[ps4]', '[xbox one]', '[switch]']

def decod(fil):
    try:
        url = 'https://api.telegram.org/file/bot' + TOKEN + '/' + fil
        img = Image.open(requests.get(url, stream=True).raw)
        dec = decode(img)
        decoded = dec[0].data.decode('utf-8')
        return decoded
    except IndexError:
        answer = 'Не могу распознать штрихкод'
        return answer


@bot.message_handler(commands=['start', 'help'], content_types=['text', 'photo'])
def send_welcome(message):
	bot.reply_to(message, "Привет! Отправь мне фотографию штрихкода видеодиска или напиши назваине игры и я скажу тебе цену закупки")

@bot.message_handler(func=lambda message: True, content_types=["text", "photo"])
def echo_all(message):

    if message.content_type == 'text' and len(message.text) >= 4:
        save.save_user_answer(message.from_user.id, message.from_user.username, 
                          message.from_user.first_name, message.from_user.last_name, message.text)
        if message.text.lower() in exceptions:
            bot.send_message(message.chat.id, 'Введите название игры, а не платформы')
        else:
            query = function.get_title(message.text.lower())
            bot.send_message(message.chat.id, '{}'.format('\n'.join(query)))

    elif message.content_type == 'text' and len(message.text) < 4:
            bot.send_message(message.chat.id, 'Введите минимум 4 символа для поиска по названию')

    elif message.content_type == 'photo':
        raw = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        fil = raw.file_path
        barcode = decod(fil)
        if barcode.isdigit():

            answer = function.get_barcode(int(barcode))
            save.save_user_answer(message.from_user.id, message.from_user.username, 
                          message.from_user.first_name, message.from_user.last_name, function.name)
            bot.send_message(message.chat.id, answer)
        else:
            bot.send_message(message.chat.id, barcode)

        

bot.polling()
