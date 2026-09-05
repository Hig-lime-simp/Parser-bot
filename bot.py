import telebot
import config
import json

# def print_message(data_arr):
#     for i in data_dict.items():
#         print
#     return

def get_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    f.close()
    return data


bot = telebot.TeleBot(config.TOKEN)


