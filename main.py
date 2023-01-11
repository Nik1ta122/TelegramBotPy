import telebot

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN


bot = telebot.TeleBot(TOKEN)


def gen_markup(command):
    if command == 'In':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton(text='colored', url='https://blitz.plus/sites/default/files/styles/original_with_watermark/public/image/2022-06/jpg/maykl-dzhekson_3.jpg?itok=68UCKH4B'),
                                   InlineKeyboardButton(text='blacknwhite', url='https://cdn.ananasposter.ru/image/cache/catalog/poster/music/81/19552-1000x830.jpg'))
        return markup
    elif command == 'chats':
        markup = InlineKeyboardMarkup(row_width=2)
        markup.row_width = 2
        markup.add(InlineKeyboardButton(text='Помощь', url='https://t.me/+lKT7PQQgSyRhNDc6'))
        return markup




@bot.message_handler(commands=['chats'])
def chat_message(message):
    bot.send_message(message.chat.id, 'На данный момент доступны следующие чаты', reply_markup=gen_markup('chats'))


@bot.message_handler(commands=['In'])
def send_message_with_in_kb(message):
    bot.send_message(message.chat.id, 'blacknwhite or colored?', reply_markup=gen_markup('In'))


@bot.message_handler(commands=['help'])
def help1(message):
    msg = bot.send_message(message.chat.id, 'Вам чем-то помочь?')
    bot.register_next_step_handler(msg, answer_back)


def answer_back(message):
    bot.send_message(message.chat.id, 'Напишите команду /func и узнайте о функционале бота')


def make_new_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    btn_black = KeyboardButton('black')
    btn_white = KeyboardButton('white')
    markup.add(btn_black, btn_white)
    return markup


@bot.message_handler(commands=['kb'])
def send_message_with_keyboard(message):
    bot.send_message(message.chat.id, 'Black or White?', reply_markup=make_new_keyboard())


@bot.message_handler(commands=["audio"])
def send_audio(message):
    with open(r'C:\Users\Nikita\PycharmProjects\pythonProject\audio\michael_jackson_this_is_it_13 - Billie Jean.mp3', 'rb') as audio:
        bot.send_audio(message.chat.id, audio)


@bot.message_handler(commands=["img"])
def send_picture(message):
    with open(r'C:\Users\Nikita\PycharmProjects\pythonProject\Img\cat.webp', 'rb') as img:
        bot.send_photo(message.chat.id, img)


@bot.message_handler(commands=["start"])
def send_welcom(message):
    bot.reply_to(message, "Добро пожаловать")


@bot.message_handler(func=lambda message:True)
def send_blackorwhite(message):
    if message.text == "black":
        with open(r'C:\Users\Nikita\PycharmProjects\pythonProject\Img\cat.webp', 'rb') as img:
            bot.send_photo(message.chat.id, img)
    elif message.text == "white":
        with open(r'C:\Users\Nikita\PycharmProjects\pythonProject\Img\white.jpg', 'rb') as img:
            bot.send_photo(message.chat.id, img)


@bot.message_handler(func=lambda message:True)
def answer_ques(message):
    if message.text == 'Да':
        bot.send_message(message.chat.id, '1 секунду', reply_markup=gen_markup('In'))
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, 'решайте проблему сами')




bot.infinity_polling()