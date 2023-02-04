import telebot

import parse_school_site as pss

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN


bot = telebot.TeleBot(TOKEN)

commands = {
    '/start': "приветствие",
    '/help': "список доступных команд",
    '/news': "новости школы",
    '/calls': "расписание звонков",
    '/safeness': "безопасность",
    '/In': "Майкл Джексон"
}


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


def make_inline_keyboard(post_url):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('Подробнее', url=post_url))
    kb.row_width = 2
    return kb


def inline_keyboard_google():
    kb11 = InlineKeyboardMarkup()
    kb11.add(InlineKeyboardButton('помощь', url='https://goo.su/rM9e'))
    kb11.row_width = 2
    return kb11


@bot.message_handler(commands=['chats'])
def chat_message(message):
    bot.send_message(message.chat.id, 'На данный момент доступны следующие чаты', reply_markup=gen_markup('chats'))


@bot.message_handler(commands=['In'])
def send_message_with_in_kb(message):
    bot.send_message(message.chat.id, 'blacknwhite or colored?', reply_markup=gen_markup('In'))


@bot.message_handler(commands=['help'])
def send_welcome(message):
    text = '<b>Список доступных команд:</b>\n'
    for cmd, dcr in commands.items():
        text += '\n' + cmd + ' - ' + dcr
    bot.send_message(message.chat.id, text, parse_mode='HTML')

def answer_back(message):
    bot.send_message(message.chat.id, 'Напишите команду /help и узнайте о функционале бота')


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

@bot.message_handler(commands=['safeness'])
def safe_ness(message):
    bot.send_message(message.chat.id, 'Перейдите по ссылке,чтобы заполнить google форму', reply_markup=inline_keyboard_google())


@bot.message_handler(commands=["img"])
def send_picture(message):
    with open(r'C:\Users\Nikita\PycharmProjects\pythonProject\Img\cat.webp', 'rb') as img:
        bot.send_photo(message.chat.id, img)


@bot.message_handler(commands=["calls"])
def send_picture(message):
    with open(r'C:\Users\Nikita\PycharmProjects\pythonProject\Img\calls.2023.jpg', 'rb') as img:
        bot.send_photo(message.chat.id, img)


@bot.message_handler(commands=['news'])
def send_school_news(message):
    news_lst = pss.get_school_news(period=7)

    if not news_lst:
        bot.send_message(message.chat.id, "Не было новостей.")
    else:
        for news in news_lst:
            text = '\n'.join((
                '<i>' + news['date'] + '</i>',
                '<b>' + news['title'] + '</b>' + '\n',
                'Текст новости: ' + (news['text'] if news['text'] else '<i>отсутствует</i>')
            ))

            bot.send_photo(
                message.chat.id,
                news['img_bytes'],
                caption=text,
                parse_mode='HTML',
                reply_markup=make_inline_keyboard(news['post_url'])
            )


@bot.message_handler(commands=["start"])
def send_welcom(message):
    bot.reply_to(message, "Добро пожаловать, напишите команду /help, чтобы узнать функционал бота")


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