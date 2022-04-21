import asyncio
from pyrogram import Client, ContinuePropagation
from pyrogram.types.messages_and_media import Message
from pyrogram.errors import FloodWait

from bot import ( API_HASH, API_ID, CASE_SENSITIVE,
        BOT_TOKEN, DESTINATION_IDS, HASHTAGS, SESSION_STRING )
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

    to_forward = False
    if message.entities is not None:
        for entity in message.entities:
            if entity.type == "hashtag":
                hashtag = message.text[entity.offset:entity.offset+entity.length]
                if CASE_SENSITIVE and (hashtag[1:] in HASHTAGS):
                    to_forward = True
                    break
                elif not CASE_SENSITIVE and (hashtag[1:].lower() in HASHTAGS):
                    to_forward = True
                    break
    if message.caption_entities is not None:
        for entity in message.caption_entities:
            if entity.type == "hashtag":
                hashtag = message.caption[entity.offset:entity.offset+entity.length]
                if CASE_SENSITIVE and (hashtag[1:] in HASHTAGS):
                    to_forward = True
                    break
                elif not CASE_SENSITIVE and (hashtag[1:].lower() in HASHTAGS):
                    to_forward = True
                    break

    if not to_forward:
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
