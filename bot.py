import discord
from discord.ext import commands
import time
from random import randint
import os

import my_token
import usuarios
import utils

last_ping = 1000

client = commands.Bot(command_prefix=">", case_insensitive=True)

@client.event
async def on_ready():
	os.system('cls' if os.name=='nt' else 'clear')
	print(f'amigo esto aqui, loguei com {client.user}')
	await client.change_presence(activity=discord.Game(name="pedra na Loritta 👀"))

@client.event
async def on_message(message):

	canal = message.channel
	comando = utils.normalizar(message.content)

	if message.author == client.user:
		return

	if str(canal).startswith('Direct Message'):
		print('--'*len(comando) + f'{message.author.name} enviou uma DM, se liga:\n"{comando}"\n'+'--'*len(comando))

	if comando == 'teste' and message.author.id == usuarios.edu:
		print(message.channel)
		return

	if comando == '>ping':
		global last_ping
		pong = await canal.send('pong?')
		init_time = int(round(time.time() * 1000))
		await pong.edit(content=f'Pong!')
		ping = int(round(time.time() * 1000)) - init_time
		if ping < last_ping:
			await canal.send(f'demorei {ping}ms, mais rapido que da ultima vez :)')
		elif ping > last_ping:
			await canal.send(f'demorei {ping}ms, mais lento que da ultima vez :/')
		else:
			await canal.send(f'demorei {ping}ms, exatamente o mesmo que da ultima vez!')
		last_ping = ping
		return

	if (comando[0:2] in ['-p', '-n', '-q', '-m', '!p']) or (comando[0:3] in ['-rm', '-rf', '-rr', '-rw', '-ff', 'ar!', '-go']):
		if message.channel.id != 714004747509694527:
			try:
				await message.delete()
				print(f'mensagem "{comando}" de {message.author.name} apagada :)')
			except:
				await canal.send('não posso apagar uma mensagem sua na DM grr')
		return

	if comando == '>anti_raid':
		if message.author.id in usuarios.mods:
			print('--'*len(comando) + f'ATENÇÃO: {message.author.name} pediu >anti_raid\n')
			await canal.send('ok')
			@client.event
			async def on_message(message):
				if (message.content == '>anti_raid_stop') and (message.author.id in usuarios.mods):
					await canal.send('ok, fim do anti raid mode')
					print('--'*len(comando) + f'ATENÇÃO: {message.author.name} pediu o fim do anti_raid mode\n')
					os.system('bot.py' if os.name=='nt' else 'python3 bot.py')
					quit()
				if message.author.id not in usuarios.mods:
					await message.delete()
			return
		else:
			await message.send(f'EI <@{message.author.id}>, você não pode usar esse comando! Ele é muito sério e só para <@709927397910249564>.')

	if comando.startswith('>dic') or comando.startswith('>dc') or comando.startswith('>dicionario'):
		await canal.send('Opa, é pra já! Saindo no capricho')
		arg = comando.replace('>dic ', '').replace('>dc ', '').replace('>dicionario ', '').replace('>dicio ', '').replace('>dic', '').replace('>dc', '').replace('>nario', '').replace('io', '')
		if(arg == ''):
			await canal.send('ah, pera lá né meu camarada, não é possível pesquisar sobre o nada... eu sinto muito')
			await canal.send('sinto porra nenhuma bip bop fodasse')
			await canal.send('https://i.ytimg.com/vi/kDs_P1ek5cE/hqdefault.jpg')
			return
		print('--'*len(comando) + f'{message.author.name} pediu >dicio\n')
		await canal.send(embed=utils.dicionario(arg.lower()))
		return

	if (comando == '>cls') and (message.author.id == usuarios.edu):
		try:
			await message.delete()
		except:
			pass
		os.system('cls' if os.name=='nt' else 'clear')
		return

	if (comando.startswith('>status')) and (message.author.id == usuarios.edu):
		status = message.content.replace('>status ', '')
		if status.startswith('jogando'):
			name = message.content.replace('jogando ', '').replace('>status ', '')
			await client.change_presence(activity=discord.Game(name=name))
		if status.startswith('ouvindo'):
			name = message.content.replace('ouvindo ', '').replace('>status ', '')
			await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=name))
		if status.startswith('assistindo'):
			name = message.content.replace('assistindo ', '').replace('>status ', '')
			await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=name))
		os.system('clear')
		print(comando)
		await message.delete()
		return

	if comando.startswith('>clear'):
		if message.author.id in usuarios.mods:
			quantidade = comando.replace('>clear ', '')
			quantidade = int(quantidade)+1

			if quantidade > 1000:
				quantidade = 1000
			elif quantidade < 0:
				quantidade = 1

			print(f'{message.author.name} pediu >clear {quantidade} em {message.channel}')
			await canal.purge(limit=quantidade, check=lambda msg: not msg.pinned)
		else:
			await canal.send(f'ops <@{message.author.id}>, você não pode usar esse comando :(')

	if comando == '>nitro':
		await message.delete()
		await canal.send('https://cdn.discordapp.com/attachments/691240822619766834/722972792219369543/Nitro_free_trial-1-1-1.png')

client.run(my_token.discord)
