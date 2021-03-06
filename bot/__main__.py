import asyncio
from pyrogram import Client, ContinuePropagation
from pyrogram.types.messages_and_media import Message
from pyrogram.errors import FloodWait

from bot import ( API_HASH, API_ID,
        BOT_TOKEN, DESTINATION_IDS, DOC_EXT, SESSION_STRING )
from bot import logger, Filters

app = None
if SESSION_STRING != '':
    app = Client(
        SESSION_STRING,
        api_id=API_ID,
        api_hash=API_HASH
    )
elif BOT_TOKEN != '':
    app = Client(
        session_name='bot_session',
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )
else:
    logger.critical('Neither SESSION_STRING, nor BOT_TOKEN found!!\nExiting...')
    exit(1)

@app.on_message(filters=Filters.fwd_message)
async def forward_message(client: Client, message: Message):

    if message.chat is None:
        raise ContinuePropagation

    media = None
    if message.audio is not None:
        media = message.audio
    elif message.voice is not None:
        media = message.voice
    elif message.photo is not None:
        media = message.photo
    elif message.document is not None:
        doc = message.document
        if doc.file_name is not None:
            doc_name = doc.file_name.lower()
            if any([
                ((doc_name.endswith(f'.{ext}')) or (f'.{ext}.' in doc_name))
                for ext in DOC_EXT
            ]):
                media = message.document

    if media is None:
        raise ContinuePropagation

    for destination in DESTINATION_IDS:
        try:
            await message.copy(chat_id=destination)
        except FloodWait as fw:
            await asyncio.sleep(fw.x)
        except Exception as ex:
            logger.error(f'Error while forwarding to {destination=}: {ex}')
        await client.send_reaction(
            chat_id=message.chat.id,
            message_id=message.message_id,
            emoji="👍"
        )

    raise ContinuePropagation


@app.on_message(filters=Filters.up_cmd)
async def up_command(_: Client, message: Message):

    while True:
        try:
            await message.reply_text(
                text='Message forwarder is up.',
                quote=True
            )
            break
        except FloodWait as fw:
            await asyncio.sleep(fw.x)
        except Exception as ex:
            logger.error(f'Error while responding to up command: {ex}')

app.run()
