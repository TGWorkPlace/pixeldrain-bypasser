import re

import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message

BYPASS_DOMAIN = "pixeldrain.isuru.eu.org"

PIXELDRAIN_URL_RE = re.compile(
    r"pixeldrain\.com/u/(\w+)", re.IGNORECASE
)


async def get_file_name(file_id: str) -> str:
    """Fetch the original file name from PixelDrain's public info API."""
    info_url = f"https://pixeldrain.com/api/file/{file_id}/info"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(info_url, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("name", file_id)
    except Exception:
        pass
    return file_id


@Client.on_message(filters.text & filters.private & ~filters.command(["start"]))
async def pixeldrain_handler(client: Client, message: Message):
    match = PIXELDRAIN_URL_RE.search(message.text)
    if not match:
        return

    file_id = match.group(1)
    bypassed_url = f"https://{BYPASS_DOMAIN}/{file_id}"
    file_name = await get_file_name(file_id)

    await message.reply(
        f"<b>File name: \n<blockquote>{file_name}</blockquote>\n</b>"
        f"<b>Bypassed url: \n<blockquote>{bypassed_url}</blockquote></b>"
    )
