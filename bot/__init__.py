import os

from dotenv import load_dotenv
import logging

from pyrogram import filters
from pyrogram.types.messages_and_media import Message

logging.basicConfig(
    format='[%(levelname)s] (%(asctime)s) %(message)s',
    level=logging.WARN
)
logger = logging.getLogger()

_config_path = os.path.join('.', 'config.env')
if os.path.exists(_config_path):
    logger.warn(f'Loading config variables from file: {_config_path}')
    load_dotenv(
        dotenv_path=_config_path,
        verbose=True,
        override=True
    )

(
    API_ID, API_HASH,
    BOT_TOKEN, SESSION_STRING,
    SOURCE_IDS, DESTINATION_IDS,
    DOC_EXT, SUDO_USERS
) = [None for _ in range(8)]


try:
    API_ID = os.environ.get('API_ID', '-1').strip()
    API_ID = int(API_ID)
    if API_ID == -1:
        logger.critical(f'Missing value for "API_ID" in config')
except Exception as ex:
    logger.critical(f'Config variable [{API_ID=}] should have been an integer')
    exit(1)

try:
    API_HASH = os.environ.get('API_HASH', '').strip()
    if API_HASH == '':
        logger.critical(f'Missing value for "API_HASH" in config')
except Exception as ex:
    logger.critical(f'Config variable [{API_HASH=}] should have been a string')
    exit(1)

try:
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '').strip()
except Exception as ex:
    logger.critical(f'Config variable [{BOT_TOKEN=}] should have been a string')
    exit(1)

try:
    SESSION_STRING = os.environ.get('SESSION_STRING', '').strip()
except Exception as ex:
    logger.critical(f'Config variable [{SESSION_STRING=}] should have been a string')
    exit(1)

try:
    SOURCE_IDS = os.environ.get('SOURCE_IDS', '').strip()
    SOURCE_IDS = [int(src_id) for src_id in SOURCE_IDS.split()]
    if not SOURCE_IDS:
        logger.critical(f'Missing value for "SOURCE_IDS" in config')
except Exception as ex:
    logger.critical(f'Config variable [{SOURCE_IDS=}] should have been space separated integers')
    exit(1)

try:
    DESTINATION_IDS = os.environ.get('DESTINATION_IDS', '').strip()
    DESTINATION_IDS = [int(dest_id) for dest_id in DESTINATION_IDS.split()]
    if not DESTINATION_IDS:
        logger.critical(f'Missing value for "DESTINATION_IDS" in config')
except Exception as ex:
    logger.critical(f'Config variable [{DESTINATION_IDS=}] should have been space separated integers')
    exit(1)

try:
    SUDO_USERS = os.environ.get('SUDO_USERS', '').strip()
    SUDO_USERS = [int(sudo_id) for sudo_id in SUDO_USERS.split()]
    if not SUDO_USERS:
        logger.critical(f'Missing value for "SUDO_USERS" in config')
except Exception as ex:
    logger.critical(f'Config variable [{SUDO_USERS=}] should have been space separated integers')
    exit(1)

try:
    DOC_EXT = os.environ.get('DOC_EXT', "pdf epub azw3 zip mp3 m4b").strip()
    DOC_EXT = [ext.lower() for ext in DOC_EXT.split()]
    if not DOC_EXT:
        logger.critical(f'Missing value for "DOC_EXT" in config')
except Exception as ex:
    logger.critical(f'Config variable [{DOC_EXT=}] should have been space separated strings')
    exit(1)

# ======================== Pyrogram Filters ================================

async def _is_sudo_user(_, __, update: Message):

    user = update.from_user
    if user is None:
        return False

    return user.id in SUDO_USERS

async def _is_source_chat(_, __, update: Message):

    chat = update.chat
    if chat is None:
        return False

    return chat.id in SOURCE_IDS

sudo_filter = filters.create(_is_sudo_user)
source_chat_filter = filters.create(_is_source_chat)

class Filters:

    fwd_message = (
        source_chat_filter
        & (~filters.edited)
        & (filters.audio | filters.document | filters.voice | filters.photo)
    )

    up_cmd = (
        sudo_filter
        & filters.command(commands=['up', 'start'], prefixes=['!', '/'])
    )
