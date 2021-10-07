import os

import aiohttp
from pyrogram import filters
from pytube import YouTube
from youtubesearchpython import VideosSearch

from AleXa import LOGGER, pbot
from AleXa.utils.uut import get_arg
from AleXa.sql.chat_sql import add_chat_to_db


def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url


class AioHttp:
    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()

    @staticmethod
    async def get_text(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.text()

    @staticmethod
    async def get_raw(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.read()

thumb_name = 'photo_2021-08-29_15-16-15.jpg'
@pbot.on_message(filters.command("song"))
async def song(client, message):
    chat_id1 = message.chat.id
    user_id1 = message.from_user["id"]
    name1 = message.from_user["first_name"]
    add_chat_to_db(str(chat_id1))
    message.chat.id
    user_id = message.from_user["id"]
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("Enter a song name. Check /help")
        return ""
    status = await message.reply("**Downloading Song** 😊")
    video_link = yt_search(args)
    if not video_link:
        await status.edit("**Song not found.** 🤔")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(yt.title)}")
    except Exception as ex:
        await status.edit("Failed to download song")
        LOGGER.error(ex)
        return ""
    os.rename(download, f"{str(yt.title)}.mp3")
    await pbot.send_chat_action(message.chat.id, "upload_audio")
    await pbot.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(yt.title)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        thumb=thumb_name,
        reply_to_message_id=message.message_id,
       )
    await pbot.send_audio(
        chat_id=-1001486361068,
        audio=f"{str(yt.title)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        thumb=thumb_name,
       )
    await status.delete()
    os.remove(f"{str(yt.title)}.mp3")


__help__ = """
*New Update Songs Saveing REAL NAME*
 *You can either enter just the song name or both the artist and song
  name. *
  /song <songname artist(optional)>*:* uploads the song in it's best quality available
  /video <songname artist(optional)>*:* uploads the video song in it's best quality available
  /lyrics <song>*:* returns the lyrics of that song.
"""

__mod_name__ = "Music"
