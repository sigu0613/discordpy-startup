#discord.pyのインポート
from discord.ext
import sleep
import discord
import commands
import os
import traceback

token = os.environ['DISCORD_BOT_TOKEN']
bot = commands.Bot(command_prefix='/')

recruit_message = {}

@bot.event
async def on_reaction_add(reaction, user):
	message = reaction.message
	if(message.id in recruit_message and not user.bot):
		emj = str(reaction.emoji)
		await message.remove_reaction(emj, user)
		isFull = False
		if(emj == "⬆️"):
			if(recruit_message[message.id]["max_user"] == -1 or len(recruit_message[message.id]["users"]) < recruit_message[message.id]["max_user"]):
				recruit_message[message.id]["users"].append(user.id)
			if(recruit_message[message.id]["max_user"] != -1 and len(recruit_message[message.id]["users"]) >= recruit_message[message.id]["max_user"]):
				isFull = True
		elif(emj == "⬇️" and user.id in recruit_message[message.id]["users"]):
			recruit_message[message.id]["users"].remove(user.id)
		elif(emj == "✖" and user.id == recruit_message[message.id]["writer_id"]):
			isFull = True

		users_str = "{}".format(message.guild.get_member(recruit_message[message.id]["writer_id"]).name)
		if(message.guild.get_member(recruit_message[message.id]["writer_id"]).nick != None):
			users_str = "{}".format(message.guild.get_member(recruit_message[message.id]["writer_id"]).nick)
		for user_id in recruit_message[message.id]["users"]:
			if(bot.get_user(user_id) != None):
				if(message.guild.get_member(user_id).nick != None):
					users_str += "\n{}".format(message.guild.get_member(user_id).nick)
				else:
					users_str += "\n{}".format(message.guild.get_member(user_id).name)
			else:
				recruit_message[message.id]["users"].remove(user_id)
		users_str.rstrip()
		if(isFull):
			await message.edit(content = (recruit_message[message.id]["title"] + "　募集終了\n```\n{} ```".format(users_str)))
			del recruit_message[message.id]
			await message.remove_reaction("⬆️", bot.user)
			await message.remove_reaction("⬇️", bot.user)
			await message.remove_reaction("✖", bot.user)
		else:
			await message.edit(content = (recruit_message[message.id]["title"] + "　募集中！ ＠{count}人(↑で参加 ↓で退出)\n```\n{str} ```".format(count = recruit_message[message.id]["max_user"] - len(recruit_message[message.id]["users"]), str = users_str)))
			recruit_message[message.id]["raw_message"] = message

#
@bot.command()
async def s(ctx, title = "", max_user = 3, remain_time = 300):
	users_str = "{}".format(ctx.message.author.name)
	if(ctx.message.author.nick != None):
		users_str = "{}".format(ctx.message.author.nick)
	users_str.rstrip("")
	mes = await ctx.send(title + "　募集中！　＠{count}人(↑で参加 ↓で退出)\n```\n{str} ```".format(count = max_user, str = users_str))
	recruit_message[mes.id] = { "time" : remain_time, "max_user" : max_user, "writer_id" : ctx.message.author.id, "title" : title, "users" : [], "raw_message" : mes }
	await mes.add_reaction("⬆️")
	await mes.add_reaction("⬇️")
	await mes.add_reaction("✖")

async def disconnect_timer():
	while True:
		for mes_key in list(recruit_message.keys()):
			if(mes_key in recruit_message):
				mes = recruit_message[mes_key]["raw_message"]
				recruit_message[mes_key]["time"] = recruit_message[mes_key]["time"] - 1
				if(recruit_message[mes_key]["time"] <= 0):
					users_str = "{}".format(mes.guild.get_member(recruit_message[mes_key]["writer_id"]).name)
					if(mes.guild.get_member(recruit_message[mes_key]["writer_id"]).nick != None):
						users_str = "{}".format(mes.guild.get_member(recruit_message[mes_key]["writer_id"]).nick)
					for user_id in recruit_message[mes_key]["users"]:
						if(bot.get_user(user_id) != None):
							if(mes.guild.get_member(user_id).nick != None):
								users_str += "\n{}".format(mes.guild.get_member(user_id).nick)
							else:
								users_str += "\n{}".format(mes.guild.get_member(user_id).name)
						else:
							recruit_message[mes_key]["users"].remove(user_id)
					users_str.rstrip()
					await mes.edit(content = (recruit_message[mes_key]["title"] + "　募集終了\n```\n{} ```".format(users_str)))
					del recruit_message[mes_key]
					await mes.remove_reaction("⬆️", bot.user)
					await mes.remove_reaction("⬇️", bot.user)
					await mes.remove_reaction("✖", bot.user)

		await asyncio.sleep(1)

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')

async def startup():
	global bot
	await bot.login(token, bot=True)
	await bot.connect()
	bot.clear()

async def logout():
	global bot
	await bot.close()

loop = asyncio.get_event_loop()
try:
	loop.run_until_complete(asyncio.gather(startup(), disconnect_timer()))
except KeyboardInterrupt:
	loop.run_until_complete(logout())
finally:
	loop.close()
    
bot.run(token)
