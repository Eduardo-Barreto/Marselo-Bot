import discord
from discord.ext import commands
import time
from random import randint
import os

import my_token
import recalque
import usuarios
import utils

last_ping = 1000

bot = commands.Bot(command_prefix=">", case_insensitive=True)

@bot.event
async def on_ready():
	print(f'amigo esto aqui, loguei com {bot.user}')

@bot.event
async def on_message(message):

	canal = message.channel

	if message.author == bot.user:
		return

	comando = utils.normalizar(message.content)

	if comando == 'teste' and message.author.id == usuarios.edu:
		print(dir(message.author.roles))
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
			print(f'mensagem "{comando}" de {message.author.name} apagada :)')
			await message.delete()
		return

	if (('te banir' in comando) or ('banir vc' in comando)) and (message.author.id == usuarios.iris):
		await canal.send('ta bom iris.')
		return

	if comando in ['fodasse?', 'fds?', 'fuedasse?', 'fodase?', 'foda-se?']:
		await message.delete()
		await canal.send('https://media1.tenor.com/images/6fcd2c6e282aa6481d98876a93848814/tenor.gif?itemid=17795077')
		return

	if 'o o respeito' in comando:
		await message.delete()
		await canal.send(file=discord.File('images/respeito.png'))
		return

	if ('tu e gay' in comando) or ('tu eh gay' in comando):
		await canal.send('https://i.pinimg.com/736x/ae/29/9c/ae299cf0dae2be30a564fcc00dd4a2a4.jpg')

	if (comando == '>anti_raid') and (message.author.id in usuarios.mods):
		await canal.send('ok')
		@bot.event
		async def on_message(message):
			if (message.content == '>anti_raid_stop') and (message.author.id in usuarios.mods):
				await canal.send('paro')
				os.system('python3 bot.py')
				quit()
			if message.author.id not in usuarios.mods:
				await message.delete()

	if comando.startswith('>dic') or comando.startswith('>dc') or comando.startswith('>dicionario'):
		await canal.send('Opa, é pra já! Saindo no capricho')
		arg = comando.replace('>dic ', '').replace('>dc ', '').replace('>dicionario ', '').replace('>dicio ', '').replace('>dic', '').replace('>dc', '').replace('>nario', '').replace('io', '')
		if(arg == ''):
			await canal.send('ah, pera lá né meu camarada, não é possível pesquisar sobre o nada... eu sinto muito')
			await canal.send('sinto porra nenhuma bip bop fodasse')
			await canal.send('https://i.ytimg.com/vi/kDs_P1ek5cE/hqdefault.jpg')
			return
		await canal.send(embed=utils.dicionario(arg.lower()))
		return

	if 'marselo' in comando:
		if (('te amo' in comando) or ('amo vc' in comando) or ('amo voce' in comando)) and (('te odeio' not in comando) and ('odeio vc' not in comando) and ('odeio voce' not in comando)):
			await canal.send('https://i.pinimg.com/236x/a1/67/08/a167080bf7444b2ce355e5ae17089ee4.jpg')
		elif (('te odeio' in comando) or ('odeio vc' in comando) or ('odeio voce' in comando)) and (('te amo' not in comando) and ('amo vc' not in comando) and ('amo voce' not in comando)):
			frase = recalque.frases[randint(0, len(recalque.frases)-1)]
			await canal.send(f'ah é, <@{message.author.id}>?!\n{frase} <:kissing_heart:790794753780088902>')
			return
		elif (('te amo' in comando) or ('amo vc' in comando) or ('amo voce' in comando)) and (('te odeio' in comando) or ('odeio vc' in comando) or ('odeio voce' in comando)):
			await canal.send('https://pbs.twimg.com/media/EapT8RoWoAAD9M2.jpg')
		else:
			try:
				texto = message.content.replace('marselo', message.author.nick).replace('MARSELO', message.author.nick.upper())
			except:
				texto = message.content.replace('marselo', message.author.name).replace('MARSELO', message.author.name.upper())
			await canal.send(texto)
			await canal.send('...')
			await canal.send('https://cdn.dicionariopopular.com/imagens/homem-aranha-apontando-og.jpg')

		return

	if ('passar pano' in comando) or ('passando pano' in comando) or ('passo pano' in comando):
		await canal.send(file=discord.File('images/panos.png'))

	# if comando.startswith('>avast'):
	# 	await message.delete()
	# 	texto = comando.replace('>avast ', '')
	# 	await message.guild.me.edit(nick=f'iris')
	# 	mensagem = await canal.send(f'As definições de {texto} foram atualizadas...', tts=True)
	# 	await message.guild.me.edit(nick='marselo')
	# 	await mensagem.edit(content='⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
	# 	time.sleep(0.5*len(texto))
	# 	await mensagem.delete()


bot.run(my_token.discord)
