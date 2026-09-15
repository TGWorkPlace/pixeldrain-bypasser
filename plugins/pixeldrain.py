import re

import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message

from config import LOG_CHANNEL

BYPASS_DOMAIN = "pixeldrain.isuru.eu.org"
BYPASS_DOMAIN_2 = "cdn.pixeldrain.eu.cc"

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
    original_url = match.group(0)
    if not original_url.startswith("http"):
        original_url = f"https://{original_url}"

    bypassed_url_1 = f"https://{BYPASS_DOMAIN}/{file_id}"
    bypassed_url_2 = f"https://{BYPASS_DOMAIN_2}/{file_id}?download"
    file_name = await get_file_name(file_id)

    text = (
        f"<b>File name: \n<blockquote>{file_name}</blockquote>\n</b>"
        f"<b>Original url: \n<blockquote>{original_url}</blockquote>\n</b>"
        f"<b>Bypassed url: \n<blockquote>{bypassed_url_1}</blockquote>\n</b>"
        f"<b>Bypassed url: \n<blockquote>{bypassed_url_2}</blockquote></b>"
    )

    await message.reply(text, disable_web_page_preview=True)

    if LOG_CHANNEL:
        try:
            await client.send_message(LOG_CHANNEL, text, disable_web_page_preview=True)
        except Exception:
            pass
