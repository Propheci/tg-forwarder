# TG Fᴏʀᴡᴀʀᴅᴇʀ
To forward audiobooks and ebooks from one telegram chat to other

## Cᴏɴғɪɢᴜʀᴀᴛɪᴏɴ

* There are two ways of configuring the bot:
    1. Set Environment Variables
    2. Use `config.env` by creating a copy of `config.env.sample` and editing the values (overrides environment variables)
* Don't use both ways at the same time 🥴

### Vᴀʀɪᴀʙʟᴇs

| Nᴀᴍᴇ                | Dᴇsᴄʀɪᴘᴛɪᴏɴ                                                                                                    | Dᴇғᴀᴜʟᴛ                     |
| :-----------------: | ------------------------------------------------------------------------------------------------               | :-------------------------: |
| `API_ID`            | Get from my.telegram.org                                                                                       | -                           |
| `API_HASH`          | Get from my.telegram.org                                                                                       | -                           |
| `SESSION_STRING`    | Use either BOT_TOKEN or SESSION_STRING for login (Given Preference)                                            | -                           |
| `BOT_TOKEN`         | Use either BOT_TOKEN or SESSION_STRING for login                                                               | -                           |
| `SUDO_USERS`        | Space separated user IDs                                                                                       | -                           |
| `SOURCE_IDS`        | Space separated chat IDs of the groups from where to forward                                                   | -                           |
| `DESTINATION_IDS`   | Space separated chat IDs of the groups to forward to                                                           | -                           |
| `HASHTAGS`          | The hashtags separated by space without `#` sign (eg. `hashtag1 hashtag2`)                                     | -                           |
| `CASE_SENSITIVE`    | If the hashtags should be matched case sensitively or not (Uncomment to enable)                                | -                           |

## Aᴠᴀɪʟᴀʙʟᴇ Cᴏᴍᴍᴀɴᴅs

- `start` or `up` : To get confirmation that bot is up
