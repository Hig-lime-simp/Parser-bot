import telebot
import config
import json

bot = telebot.TeleBot(config.TOKEN)

with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    print(data)
