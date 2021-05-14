import sqlite3
import telebot
from time import sleep

from settings import URL, DB, TELEGRAM_TOKEN, CHAT_ID
from data_loader import DataLoader
from SQL_connector import SQLite_saver


bot = telebot.TeleBot(TELEGRAM_TOKEN)

def main():
    sqlite_conn = sqlite3.connect(DB)
    sqlite_saver = SQLite_saver(sqlite_conn)
    sqlite_saver.create_documents()

    while True:
        dl = DataLoader(URL)
        new_documents = sqlite_saver.add_documents(dl.get_data())
        for doc in new_documents:         
            bot.send_document(CHAT_ID, dl.get_byte_object(doc['href'], doc['name']))

        sleep(10)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Press Ctrl+C')