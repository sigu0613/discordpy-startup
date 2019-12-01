#discord.pyのインポート
from asyncio import sleep
import discord
token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()
#BOTログイン処理
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='!delchat *'))
# BOT動作プログラム
@client.event
async def on_message(message):
    # 送り主がBotだった場合反応したくないので
    if client.user != message.author:
        # 削除コマンド
        if message.content.startswith("!delchat "):
            #役職比較
            if discord.utils.get(message.author.roles, name="admin"):
                # メッセージを格納
                delcmd = message.content
                # 入力メッセージのリスト化
                delcmd_ = delcmd.split()
                # 入力メッセージのint化
                delcmd_int = int(delcmd_[1])
                # 入力メッセージの単語数
                delcmd_c = len(delcmd_)
                if delcmd_c == 2 and delcmd_int <= 50 and delcmd_int > 1:
                    # メッセージ取得
                    msgs = [msg async for msg in client.logs_from(message.channel, limit=(delcmd_int+1))]
                    await client.delete_messages(msgs)
                    delmsg = await client.send_message(message.channel, '削除が完了しました')
                    await sleep(5)
                    await client.delete_message(delmsg)
                else:
                    # エラーメッセージを送ります
                    delmsg = await client.send_message(message.channel, "コマンドが間違っています。[!delchat *] *:2～50")
                    await sleep(5)
                    await client.delete_message(delmsg)
                    
            else:
                # エラーメッセージを送ります
                delmsg = await client.send_message(message.channel, "admin権限がありません。")
                await sleep(5)
                await client.delete_message(delmsg)
client.run("***")
