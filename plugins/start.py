from pyrogram import Client, filters
from pyrogram.types import Message

START_TEXT = """👋 **Hey {mention}, welcome!**

I'm your **PixelDrain Bypass Bot** — send me any PixelDrain link and I'll instantly generate a bypassed download URL for you, no rate-limit headaches.

**How to use:**
Just send a link like:
`https://pixeldrain.com/u/xxxxxxxx`

I'll reply with:
```
File name: <file_name>
Bypassed url: <bypassed_link>
```

That's it — fast, simple, no waiting. 🚀
"""


@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await message.reply(
        START_TEXT.format(mention=message.from_user.mention),
        disable_web_page_preview=True,
    )
