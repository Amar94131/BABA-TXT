import os
import re
import sys
import json
import time
import aiohttp
import asyncio
import requests
import subprocess
import urllib.parse
import yt_dlp
import cloudscraper
import datetime
import master
import ffmpeg

from yt_dlp import YoutubeDL
import yt_dlp as youtube_dl
from core import download_and_send_video
import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN, FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2, FORCE_SUB_CHANNEL_3, FORCE_SUB_CHANNEL_4
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from flask import Flask
from pyrogram.errors import RPCError
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

# Bot session setup
app = Client("my_bot")

# Flask App Initialization
flask_app = Flask(__name__)

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Force Subscription Message
FORCE_MSG = "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b>"

# Function to check Force Subscription
async def is_subscribed(client, user_id):
    if not (FORCE_SUB_CHANNEL_1 or FORCE_SUB_CHANNEL_2 or FORCE_SUB_CHANNEL_3 or FORCE_SUB_CHANNEL_4):
        return True

    member_status = ["owner", "administrator", "member"]

    for channel_id in [FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2, FORCE_SUB_CHANNEL_3, FORCE_SUB_CHANNEL_4]:
        if not channel_id:
            continue

        try:
            member = await client.get_chat_member(chat_id=channel_id, user_id=user_id)
        except UserNotParticipant:
            return False

        if member.status not in member_status:
            return False

    return True

# Middleware to enforce force subscription
async def force_subscription(client, message: Message):
    is_user_subscribed = await is_subscribed(client, message.from_user.id)
    if not is_user_subscribed:
        await message.reply_text(FORCE_MSG.format(first=message.from_user.first_name))
        return False
    return True

# Start Command Handler with Force Sub Check
@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    is_user_subscribed = await force_subscription(bot, message)
    if not is_user_subscribed:
        return

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="📞 Contact", url="https://t.me/AllCourseADMIN_BOT"),
                InlineKeyboardButton(text="📖 Course Update", url="https://t.me/+VFhUKQvM7PVlYWQ1"),
            ],
            [
                InlineKeyboardButton(text="🪄 Course Deal", url="https://t.me/+h5M1Xp0a7rM5ZDhl"),
            ],
        ]
    )

    random_image_url = "https://envs.sh/8lA.jpg"
    caption = (
        "𝖧𝖾𝗅𝗅𝗈 𝖽𝖾𝖺𝗋 👋!\n\n𝖨 𝖠𝗆 𝖳𝖷𝖳 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽 𝖡𝗈𝗍 𝖴𝗌𝖾 /help\n📖 𝖴𝗌𝖾 /txt 𝗍𝗈 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽 𝖥𝗋𝗈𝗆 𝖳𝖷𝖳 𝖥𝗂𝗅𝖾\n\n<blockquote>𝖬𝖺𝖽𝖾 𝖡𝗒 <a href='https://t.me/AllCourseADMIN_BOT'>🄰🄳🄼🄸🄽</a></blockquote>"
    )

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=random_image_url,
        caption=caption,
        reply_markup=keyboard
    )

# Help Command
@bot.on_message(filters.command("help"))
async def help_command(bot: Client, message: Message):
    is_user_subscribed = await force_subscription(bot, message)
    if not is_user_subscribed:
        return

    help_text = (
        "🔑 𝖧𝗈𝗐 𝗍𝗈 𝗀𝖾𝗍 𝗌𝗍𝖺𝗋𝗍𝖾𝖽 𝗐𝗂𝗍𝗁 𝖯𝗋𝖾𝗆𝗂𝗎𝗆\n\n" 
        "1. 𝖥𝗂𝗋𝗌𝗍 𝗈𝖿 𝖺𝗅𝗅, 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 𝗍𝗁𝖾 𝗈𝗐𝗇𝖾𝗋 𝖺𝗇𝖽 𝖻𝗎𝗒 𝖺 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝗉𝗅𝖺𝗇 💰\n"
        "2. 𝖨𝖿 𝗒𝗈𝗎 𝖺𝗋𝖾 𝖺 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝗎𝗌𝖾𝗋 𝗒𝗈𝗎 𝖼𝖺𝗇 𝖼𝗁𝖾𝖼𝗄 𝗒𝗈𝗎𝗋 𝗉𝗅𝖺𝗇 𝖻𝗒 𝗎𝗌𝗂𝗇𝗀 /myplan 🔍\n\n"
        "  📖 𝖴𝗌𝖺𝗀𝖾\n\n"
        "1. /add_channel {𝖼𝗁𝖺𝗇𝗇𝖾𝗅_𝗂𝖽}\n"
        "2. /remove_channel {𝖼𝗁𝖺𝗇𝗇𝖾𝗅_𝗂𝖽}\n"
        "3. /txt 𝖯𝗋𝗈𝖼𝖾𝗌𝗌 𝗍𝗁𝖾 𝗍𝗑𝗍 𝖿𝗂𝗅𝖾\n"
        "4. /stop 𝖲𝗍𝗈𝗉 𝗍𝗁𝖾 𝗍𝖺𝗌𝗄 🚫\n"
        "5. /adduser user id\n"
        "6. /removeuser user id\n"
        "7. /users only admin\n"
        "8. /id \n"
        "9. /remove_all_channels \n"
        "10. /allowed_channels \n\n"
        "A𝗇𝗒 𝗊𝗎𝖾𝗌𝗍𝗂𝗈𝗇𝗌 💬 <a href='https://t.me/AllCourseADMIN_BOT'>🄰🄳🄼🄸🄽</a>"
    )
    
    await message.reply_text(guide_text)

# 1. /adduser
@bot.on_message(filters.command("adduser") & filters.private)
@admin_only
async def add_user(client, message: Message):
    try:
        _, user_id, expiration_date = message.text.split()
        subscription_data = read_subscription_data()
        subscription_data.append([user_id, expiration_date])
        write_subscription_data(subscription_data)
        await message.reply_text(f"User {user_id} added with expiration date {expiration_date}.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /adduser <user_id> <expiration_date>")
   
# 2. /removeuser
@bot.on_message(filters.command("removeuser") & filters.private)
@admin_only
async def remove_user(client, message: Message):
    try:
        _, user_id = message.text.split()
        subscription_data = read_subscription_data()
        subscription_data = [user for user in subscription_data if user[0] != user_id]
        write_subscription_data(subscription_data)
        await message.reply_text(f"User {user_id} removed.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /removeuser <user_id>")

YOUR_ADMIN_ID = 1928404158

# Helper function to check admin privilege
def is_admin(user_id):
    return user_id == YOUR_ADMIN_ID

# Command to show all users (Admin only)
@bot.on_message(filters.command("users") & filters.private)
async def show_users(client, message: Message):
    user_id = message.from_user.id

    if not is_admin(user_id):
        await message.reply_text("❌ You are not authorized to use this command.")
        return

    subscription_data = read_subscription_data()
    
    if subscription_data:
        users_list = "\n".join(
            [f"{idx + 1}. User ID: `{user[0]}`, Expiration Date: `{user[1]}`" for idx, user in enumerate(subscription_data)]
        )
        await message.reply_text(f"👥 Current Subscribed Users:\n\n{users_list}")
    else:
        await message.reply_text("ℹ️ No users found in the subscription data.")

# 3. /myplan
@bot.on_message(filters.command("myplan") & filters.private)
async def my_plan(client, message: Message):
    user_id = str(message.from_user.id)
    subscription_data = read_subscription_data()  # Make sure this function is implemented elsewhere

    # Define YOUR_ADMIN_ID somewhere in your code
    if user_id == str(YOUR_ADMIN_ID):  # YOUR_ADMIN_ID should be an integer
        await message.reply_text("✨ You have permanent access!")
    elif any(user[0] == user_id for user in subscription_data):  # Assuming subscription_data is a list of [user_id, expiration_date]
        expiration_date = next(user[1] for user in subscription_data if user[0] == user_id)
        await message.reply_text(
            f"📅 Your Premium Plan Status\n\n"
            f"🆔 User ID: `{user_id}`\n"
            f"⏳ Expiration Date: `{expiration_date}`\n"
            f"🔒 Status**: Active"
        )
    else:
        await message.reply_text("**❌ You are not a premium user.**")

# 4. /add_channel
@bot.on_message(filters.command("add_channel"))
async def add_channel(client, message: Message):
    user_id = str(message.from_user.id)
    subscription_data = read_subscription_data()

    if not any(user[0] == user_id for user in subscription_data):
        await message.reply_text("You are not a premium user.")
        return

    try:
        _, channel_id = message.text.split()
        channels = read_channels_data()
        if channel_id not in channels:
            channels.append(channel_id)
            write_channels_data(channels)
            await message.reply_text(f"Channel {channel_id} added.")
        else:
            await message.reply_text(f"Channel {channel_id} is already added.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /add_channel <channel_id>")


# 5. /remove_channels
@bot.on_message(filters.command("remove_channel"))
async def remove_channel(client, message: Message):
    user_id = str(message.from_user.id)
    subscription_data = read_subscription_data()

    if not any(user[0] == user_id for user in subscription_data):
        await message.reply_text("You are not a premium user.")
        return

    try:
        _, channel_id = message.text.split()
        channels = read_channels_data()
        if channel_id in channels:
            channels.remove(channel_id)
            write_channels_data(channels)
            await message.reply_text(f"Channel {channel_id} removed.")
        else:
            await message.reply_text(f"Channel {channel_id} is not in the list.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /remove_channels <channel_id>")

# /id Command
@app.on_message(filters.command("id"))
async def id_command(client: Client, message: Message):
    if message.chat.type == "private":
        # For private chats, return the user ID
        user_id = message.from_user.id
        await message.reply_text(
            f"🎉 Success!\n\n"
            f"🆔 Your User ID:\n`{user_id}`\n\n"
            f"📌 Use this ID for further requests."
        )
    else:
        # For groups or channels, return the chat ID
        chat_id = message.chat.id
        await message.reply_text(
            f"✅ Success!\n\n"
            f"🆔 This Group/Channel ID:\n`{chat_id}`\n\n"
            f"📌 Use this ID for further requests.\n\n"
            f"To link this group/channel, use the following command:\n"
            f"`/add_channel {chat_id}`"
        )

YOUR_ADMIN_ID = 1928404158

# Helper function to check admin privilege
def is_admin(user_id):
    return user_id == YOUR_ADMIN_ID

# Command to show all allowed channels (Admin only)
@bot.on_message(filters.command("allowed_channels"))
async def allowed_channels(client, message: Message):
    user_id = message.from_user.id

    if not is_admin(user_id):
        await message.reply_text("❌ You are not authorized to use this command.")
        return

    channels = read_channels_data()
    if channels:
        channels_list = "\n".join([f"- {channel}" for channel in channels])
        await message.reply_text(f"📋 Allowed Channels:\n\n{channels_list}")
    else:
        await message.reply_text("ℹ️ No channels are currently allowed.")

# Command to remove all channels (Admin only)
@bot.on_message(filters.command("remove_all_channels"))
async def remove_all_channels(client, message: Message):
    user_id = message.from_user.id

    if not is_admin(user_id):
        await message.reply_text("❌ You are not authorized to use this command.")
        return

    # Clear the channels data
    write_channels_data([])
    await message.reply_text("✅ All channels have been removed successfully.")


# 6. /stop
@bot.on_message(filters.command("stop"))
async def stop_handler(client, message: Message):
    if message.chat.type == "private":
        user_id = str(message.from_user.id)
        subscription_data = read_subscription_data()
        if not any(user[0] == user_id for user in subscription_data):
            await message.reply_text("😔 You are not a premium user. Please subscribe to get access! 🔒")
            return
    else:
        channels = read_channels_data()
        if str(message.chat.id) not in channels:
            await message.reply_text("🚫 You are not a premium user. Subscribe to unlock all features! ✨")
            return

    await message.reply_text(" Stopped🚦" , True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("txt"))
async def moni_handler(client: Client, m: Message):
    if m.chat.type == "private":
        user_id = str(m.from_user.id)
        subscription_data = read_subscription_data()
        if not any(user[0] == user_id for user in subscription_data):
            await m.reply_text("❌ You are not a premium user. Please upgrade your subscription! 💎")
            return
    else:
        channels = read_channels_data()
        if str(m.chat.id) not in channels:
            await m.reply_text("❗ You are not a premium user. Subscribe now for exclusive access! 🚀")
            return
            
    editable = await m.reply_text('𝖳𝗈 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽 𝖠 𝖳𝗑𝗍 𝖥𝗂𝗅𝖾 𝖲𝖾𝗇𝖽 𝖧𝖾𝗋𝖾 📑')

    try:
        input: Message = await client.listen(editable.chat.id)
        
        # Check if the message contains a document and is a .txt file
        if not input.document or not input.document.file_name.endswith('.txt'):
            await m.reply_text("Please send a valid .txt file.")
            return

        # Download the file
        x = await input.download()
        await input.delete(True)

        path = f"./downloads/{m.chat.id}"
        file_name = os.path.splitext(os.path.basename(x))[0]

        # Read and process the file
        with open(x, "r") as f:
            content = f.read().strip()

        lines = content.splitlines()
        links = []

        for line in lines:
            line = line.strip()
            if line:
                link = line.split("://", 1)
                if len(link) > 1:
                    links.append(link)

        os.remove(x)
        print(len(links))

    except:
        await m.reply_text("Invalid file input")
        if os.path.exists(x):
            os.remove(x)

    await editable.edit(f"Total Link Found Are 🔗** **{len(links)}**\n\nSend From Where You Want To Download Inital Is**1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)               

    # This is where you would set up your bot and connect the handle_command function      
    await editable.edit("Enter Batch Name or send 1 for grabing from text filename.")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == '1':
        b_name = file_name
    else:
        b_name = raw_text0
        
    await editable.edit("Enter File Quality 🎬\n☞ 144\n☞ 240\n☞ 360\n☞ 480\n☞ 720\n☞ 1080\nPlease Choose Quality")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    

    await editable.edit("Enter Your Name or send `1` for use default")

    # Listen for the user's response
    input3: Message = await bot.listen(editable.chat.id)

    # Get the raw text from the user's message
    raw_text3 = input3.text

    # Delete the user's message after reading it
    await input3.delete(True)

    # Default credit message
    credit = "️ ⁪⁬⁮⁮⁮"
    if raw_text3 == '1':
        CR = "<a href='https://t.me/AllCourseADMIN_BOT'>🄰🄳🄼🄸🄽</a>"
    elif raw_text3:
        CR = raw_text3
    else:
        CR = credit
   
    await editable.edit("🌄 Now send the Thumb url if don't want thumbnail send no ")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        # Assuming links is a list of lists and you want to process the second element of each sublist
        for i in range(count - 1, len(links)):

            # Replace parts of the URL as needed
            V = links[i][1].replace("file/d/","uc?export=download&id=")\
               .replace("www.youtube-nocookie.com/embed", "youtu.be")\
               .replace("?modestbranding=1", "")\
               .replace("/view?usp=sharing","")\
               .replace("youtube.com/embed/", "youtube.com/watch?v=")
            
            url = "https://" + V
            
            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
                

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url or "tencdn.classplusapp" in url or "webvideos.classplusapp.com" in url or "media-cdn-alisg.classplusapp.com" in url or "videos.classplusapp" in url or "videos.classplusapp.com" in url or "media-cdn-a.classplusapp" in url or "media-cdn.classplusapp" in url or "drmcdni" in url:
             url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0'}).json()['url']

            # Handle master.mpd URLs
            elif '/master.mpd' in url:
                id = url.split("/")[-2]
                url = "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"

            # Sanitizing the name
            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            # For master.mpd, handle m3u8 URL download
            if "/master.mpd" in url:
                if "https://sec1.pw.live/" in url:
                    url = url.replace("https://sec1.pw.live/", "https://d1d34p8vz63oiq.cloudfront.net/")

                # Command to download m3u8 file
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
                subprocess.run(cmd, shell=True)
                
            if "edge.api.brightcove.com" in url:
                bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
                url = url.split("bcov_auth")[0]+bcov
       
            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
            
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'

            if "embed" in url:
                ytf = f"bestvideo[height<={raw_text2}]+bestaudio/best[height<={raw_text2}]"
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'
           
            elif "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp --cookies "{COOKIES_FILE_PATH}" -f "{ytf}" "{url}" -o "{name}.mp4"'

            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'
        
                
            try:                
                cc = f'💾 VIDEO ID: {str(count).zfill(3)}.\n\n<pre><code>🅀🅄🄰🄻🄸🅃🅈 - {raw_text2}</code></pre>\n\n📜 🅃🄸🅃🄻🄴: {name1}.mkv\n\n<pre><code>🄱🄰🅃🄲🄷 🄽🄰🄼🄴: {b_name}</code></pre>\n\n🔻 Extracted By : {CR}'
                cc1 = f'📒 FILE ID: {str(count).zfill(3)}.\n\n<pre><code>🅀🅄🄰🄻🄸🅃🅈 - {raw_text2}</code></pre>\n\n📜 🅃🄸🅃🄻🄴: {name1}.pdf\n\n<pre><code>🄱🄰🅃🄲🄷 🄽🄰🄼🄴: {b_name}</code></pre>\n\n🔻 Extracted By : {CR}'
                                                 
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                
                elif ".pdf" in url:
                    try:
                        await asyncio.sleep(4)
                        # Replace spaces with %20 in the URL
                        url = url.replace(" ", "%20")
 
                        # Create a cloudscraper session
                        scraper = cloudscraper.create_scraper()

                        # Send a GET request to download the PDF
                        response = scraper.get(url)

                        # Check if the response status is OK
                        if response.status_code == 200:
                            # Write the PDF content to a file
                            with open(f'{name}.pdf', 'wb') as file:
                                file.write(response.content)

                            # Send the PDF document
                            await asyncio.sleep(4)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1

                            # Remove the PDF file after sending
                            os.remove(f'{name}.pdf')
                        else:
                            await m.reply_text(f"Failed to download PDF: {response.status_code} {response.reason}")

                    except FloodWait as e:
                        await m.reply_text(str(e))
                        await asyncio.sleep(2)  # Use asyncio.sleep for non-blocking sleep
                        return  # Exit the function to avoid continuation

                    except Exception as e:
                        await m.reply_text(f"An error occurred: {str(e)}")
                        await asyncio.sleep(4)  # You can replace this with more specific
                        continue
                        
                          
                else:
                    Show = f"❊⟱ Downloading ⟱❊ »\n\n📄 Title:- `{name}\n\n⌨ Quality » {raw_text2}`\n\n🔗 URL » `{url}`"
                    prog = await m.reply_text(f"Downloading:-\n\n📄 Title:- `{name}\n\nQuality - {raw_text2}`\n\nlink:`{url}`\n\nBot Made By @AllCourseADMIN_BOT")
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"⌘ Downloding Interested\n\n⌘ Name » {name}\n⌘ Link » `{url}`"
                )
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("DONE ✅")



bot.run()
if __name__ == "__main__":
    asyncio.run(main())
