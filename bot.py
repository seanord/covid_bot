"""
@Creator : Grigory Gramenkov
"""

import telebot
import csv
import emoji
import requests
from bs4 import BeautifulSoup

TOKEN = "YOUR TOKEN HERE"
bot = telebot.TeleBot(TOKEN)
with open("countries.csv", newline='') as csvfile:
    data = list(csv.reader(csvfile))
emojis_dict = {}
for d in data:
    if d != []:
        country = d[0], d[1]
        emojis_dict.update({country[0]: country[1]})
url = "https://news.google.com/covid19/map?hl=en-US&gl=US&ceid=US%3Aen&mid="


def check_if_emoji(msg):
    for character in msg:
        if character in emoji.UNICODE_EMOJI:
            return True


@bot.message_handler(func=lambda message: True, content_types=['text'])
def chatting(message):
    m_text = message.text
    if len(m_text) <= 2: # every emoji consists of two symbols
        if check_if_emoji(m_text):
            mes = str(emoji.demojize(m_text))
            no_saints = mes.replace('St.', 'Saint')
            no_diacritics = no_saints.replace('ã', 'a').replace('Å', 'A').replace('ç', 'c').replace('ô', 'o') \
                .replace('í', 'i').replace('è', 'e').replace('é', 'e').replace('’', '\'')
            no_ampersands = no_diacritics.replace('&', 'and')
            no_colons = no_ampersands.replace(':', '')
            no_dashes = no_colons.replace('_', ' ')
            if no_dashes in emojis_dict.keys():
                code = emojis_dict[no_dashes].replace('/', '%2F')
                covid = url + code
                page = requests.get(covid)
                soup = BeautifulSoup(page.text, "html.parser")
                confirmed = soup.find("div", {"aria-describedby": "i3"}).get_text()
                recovered = soup.find("div", {"aria-describedby": "i4"}).get_text()
                deaths = soup.find("div", {"aria-describedby": "i5"}).get_text()
                country_stats = m_text + ' ' + no_dashes + ':\nConfirmed cases: ' + confirmed + '\nRecovered: ' + \
                                recovered + '\nDeaths: ' + deaths
                bot.reply_to(message, country_stats)

            else:
                bot.reply_to(message, "It's not a country")
    else:
        bot.reply_to(message, "Send only one flag")


@bot.message_handler(func=lambda message: True, content_types=['sticker'])
def default_command(message):
    # print(message)
    bot.send_message(message.chat.id, "Nice sticker, but I only accept emoji")


bot.polling()
while True:
    pass
