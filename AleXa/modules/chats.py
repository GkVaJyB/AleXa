from AleXa import telethn as borg, OWNER_ID
from pyrogram import filters
from AleXa import pbot
from AleXa.alexa import get_arg
from AleXa.modules.sql.chat_sql import load_chats1_list, remove_chat_from_db
from io import BytesIO


@pbot.on_message(filters.user(OWNER_ID) & filters.command("broadcast"))
async def broadcast(client, message):
    to_send = get_arg(message)
    chats1 = load_chats1_list()
    success = 0
    failed = 0
    for chat in chats1:
        try:
            await pbot.send_message(int(chat), to_send)
            success += 1
        except:
            failed += 1
            remove_chat_from_db(str(chat))
            pass
    await message.reply(
        f"Message sent to {success} chat(s). {failed} chat(s) failed recieve message"
    )


@pbot.on_message(filters.user(OWNER_ID) & filters.command("chatlist"))
async def chatlist(client, message):
    chats1 = []
    all_chats = load_chats_list()
    for i in all_chats:
        if str(i).startswith("-"):
            chats1.append(i)
    chatfile = "List of chats.\n0. Chat ID | Members count | Invite Link\n"
    P = 1
    for chat in chats1:
        try:
            link = await pbot.export_chat_invite_link(int(chat))
        except:
            link = "Null"
        try:
            members = await pbot.get_chat_members_count(int(chat))
        except:
            members = "Null"
        try:
            chatfile += "{}. {} | {} | {}\n".format(P, chat, members, link)
            P = P + 1
        except:
            pass
    with BytesIO(str.encode(chatfile)) as output:
        output.name = "chatlist.txt"
        await message.reply_document(document=output, disable_notification=True)
