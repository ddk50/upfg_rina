import discord
from discord.ext import tasks
import datetime
import sqlite3
import os

from rina import Notifications
from rina import Msg

TOKEN = os.environ['UPFG_DISCORD_BOT_TOKEN']
LOG_CHANNEL = 714485018713391205
BROAD_CAST_CHANNEL = 714485018713391205

client = discord.Client()
notifi = Notifications()

# 起動時
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print(f"UPFGチャネルにログインしました")
    dt_now = datetime.datetime.now()
    msg = dt_now.strftime('私、天王寺璃奈。%Y年%m月%d日 %H:%M:%S に再起動したよ')
    await client.get_channel(LOG_CHANNEL).send(msg)
    
    
# メッセージ受信時
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    ret = notifi.execute(message.content)
    if ret != None:
        await message.channel.send(ret)
    else:
        return
    
    # 「/neko」と発言したら「にゃーん」が返る処理
    # if message.content == '/rina':
    #     await message.channel.send('璃奈ちゃんボード。Hello' + ' >' + message.author.display_name)

# イベントループ
@tasks.loop(seconds=60)
async def loop():
    for k, v in notifi.get_all():
        msg = v.broadcast_or_not()
        if msg != None:
            print(f"broadcast: {msg}")
            await client.get_channel(BROAD_CAST_CHANNEL).send(msg)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
