import os
import logging

from dotenv import load_dotenv


load_dotenv()

URL = 'https://my.oncocentre.ru'
DB = os.path.join('db', 'documents.db')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# cookies
HEALTHID_LANG = os.getenv('HEALTHID_LANG')
LHC_PER = os.getenv('LHC_PER')
_YM_VISORC = os.getenv('_YM_VISORC')
_GA = os.getenv('_GA')
_GID = os.getenv('_GID')
_YM_ISAD = os.getenv('_YM_ISAD')
_YM_D = os.getenv('_YM_D')
_YM_UID = os.getenv('_YM_UID')
HEALTHID = os.getenv('HEALTHID')


logging.basicConfig(
    filename='bot.log',
    format='%(asctime)s: %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
