import discord
from discord.ext import tasks
import datetime
import sqlite3
import os
import asyncio

from rina import Notifications
from rina import Msg

TOKEN = os.environ['UPFG_DISCORD_BOT_TOKEN']
LOG_CHANNEL = 714485018713391205
BROAD_CAST_CHANNEL = 714485018713391205

client = discord.Client()
notifi = Notifications(client)

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

    ret = notifi.execute(message.content, message.channel.id)
    if ret != None:
        await message.channel.send(ret)
    else:
        return
    
    # 「/neko」と発言したら「にゃーん」が返る処理
    # if message.content == '/rina':
    #     await message.channel.send('璃奈ちゃんボード。Hello' + ' >' + message.author.display_name)

async def do_broadcast(i):
    msg     = i[0]
    chan_id = i[1]
    print(f"broadcast: {msg} to {chan_id}")
    chan = client.get_channel(chan_id)
    if chan == None:
        await client.get_channel(LOG_CHANNEL).send(f"メッセージ投稿エラー: id: {chan_id} そんなチャンネルない")
    else:
        await chan.send(f"=== 全体お知らせ === {msg}")

# イベントループ
@tasks.loop(seconds=60)
async def loop():
    seqs = list(filter(lambda x: x.broadcast_or_not() != None, notifi.get_all()))
    print(f"notifications: {seqs}")
    await asyncio.wait([do_broadcast(i) for i in seqs])
    # for n in notifi.get_all():
    #     ret = n.broadcast_or_not()
    #     if ret != None:
    #         msg        = ret[0]
    #         channel_id = ret[1]
    #         print(f"broadcast: {msg} to {channel_id}")
    #         chan = client.get_channel(channel_id)
    #         if chan == None:
    #             print(f"id: {channel_id} そんなチャンネルは存在しません")
    #         else:
    #             await chan.send(f"=== 全体お知らせ === {msg}")

# これがないとtask.loopは60秒ごとにループしてくれない
loop.start()

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
