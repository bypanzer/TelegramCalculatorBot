import telebot
from telebot import types
import tornado.web
import cherrypy
import requests
import signal
import calc_classes
import config
import random
import time
import re


bot = telebot.TeleBot(config.token)
#my_id = "121213588"
#nail_id = "196467107"
#victor_id = "204482135"


# bot.send_message(my_id, "test")
# upd = bot.get_updates()
# last_upd = upd[-1]
# message_from_user = last_upd.message
# print(message_from_user)
# @bot.message_handler(content_types=[" "])
# bot.polling(none_stop=True, interval=0)

bot.set_webhook()
print(bot.get_me())
opa = True
min = 0
answer = ""
idd = 0
helpa = """
    Bot can calculate the exception, which you will send.\nJust write /start to show keyboard
write your mathematical exception any length, then send it and tap '/calc'.\nCommands:
Operators: +, -, *, /, %, ^
Functions: sin, cos, tg, atg, lg, sqrt
Others: pi, e

Examples:
"lg(sqrt(5*5)*sqrt(10+15)-15)"
"atg(sqrt(3))"
"sin30+cos-60"
"-(-2)+-(-2)"
"""

def log(message, answerr=""):
    print("\n ------")
    from datetime import datetime
    print(datetime.now())
    print("Message by {0} {1}. (id = {2}) \n Text= {3}".format(message.from_user.first_name,
                                                               message.from_user.last_name,
                                                               str(message.from_user.id),
                                                               answer))
    print(answerr)

@bot.message_handler(commands=['timer'])
def handle_text(message):
    try:
        avg = message.text.split()
        print(avg[1])
        if(len(avg) == 1 or avg[1].find('.')!=-1):
            bot.send_message(message.chat.id, "Time in minutes please")
        else:
            mi = int(avg[1])
            time.sleep(mi*60)
            bot.send_message(message.chat.id, "Time was finished.")
    except:
        bot.send_message(message.chat.id, "Time in minutes please")
    log(message)
@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.chat.id, helpa)


@bot.message_handler(commands=['about'])
def handle_text(message):
    bot.send_message(message.chat.id, """Author K.V.Averyanov(@Kirillzzy)\nEmail for questions and suggestions:
kirillzzy@gmail.com""")

@bot.message_handler(commands=['calc'])
def handle_text(message):
    calc_exc = calc_classes.Calculator(answer)
    answerr = calc_exc.main()
    log(message, answerr)
    bot.send_message(message.chat.id, answerr)
    globals()['answer'] = ''
@bot.message_handler(commands=['cancel'])
def handle_text(message):
    try:
        globals()['answer'] = answer[:-1]
        bot.send_message(message.chat.id, answer)
    except:
        bot.send_message(message.chat.id, "Syntax error")
@bot.message_handler(commands=['start'])
def handle_text(message):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row('/calc', '/cancel')
    user_markup.row('1', '2', '3', '4', '5', ',')
    user_markup.row('6','7','8','9','0', '.')
    user_markup.row('+','-','*','/')
    user_markup.row('%', '^', '(', ')')
    user_markup.row('sin','cos','tg','atg')
    user_markup.row('lg','sqrt','pi','e')
    bot.send_message(message.from_user.id, 'Started', reply_markup=user_markup)

@bot.message_handler(commands=['stopwords'])
def handle_text(message):
    globals()['opa'] = False


@bot.message_handler(commands=['words'])
def handle_text(message):
    try:
        globals()['opa'] = True
        leny = open("words_ru.txt", 'r')
        words = leny.readlines()
        leny.close()
        avg = message.text.split()
        log(message)
        if len(avg) == 1:
            while opa:
                bot.send_message(message.from_user.id, random.choice(words))
        else:
            for i in range(int(avg[1])):
                bot.send_message(message.from_user.id, random.choice(words))
    except:
        bot.send_message(message.from_user.id, "Syntax Error")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    globals()['answer'] += message.text
    bot.send_message(message.chat.id, answer)


"""
@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    calc_exc = calc_classes.Calculator(query.query)
    answer = calc_exc.main()
    ans = types.InlineQueryResultArticle(id='1', title="Answer", description=answer, thumb_height=2, thumb_width=4)
    bot.answer_inline_query(query.id, [ans])
"""
bot.polling(none_stop=True, interval=0)
